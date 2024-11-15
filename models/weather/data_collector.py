"""
Weather data collection module for climate prediction.

This module provides functionality to collect historical weather data
from a public weather API and process it for model training.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import xml.etree.ElementTree as ET

import aiohttp
import pandas as pd

from config import Config

logger = logging.getLogger(__name__)


class WeatherDataCollector:
    """
    A class to collect and process weather data from external API.
    
    This collector handles asynchronous data fetching, parsing XML responses,
    and converting the data into a pandas DataFrame format suitable for
    model training.
    """
    
    def __init__(self):
        """Initialize API settings and connection parameters."""
        self._initialize_api_settings()

    def _initialize_api_settings(self) -> None:
        """Initialize API endpoint configuration and connection settings."""
        self.base_url = Config.API_BASE_URL + Config.API_ENDPOINTS["monthly_summary"]
        self.timeout = aiohttp.ClientTimeout(total=Config.API_TIMEOUT)
        self.max_retries = Config.API_RETRY_ATTEMPTS
        self.retry_delay = Config.API_RETRY_DELAY
        self.semaphore = asyncio.Semaphore(10)

    async def _get_monthly_data_async(
        self, year: int, month: int, session: aiohttp.ClientSession
    ) -> Optional[List[Dict]]:
        """
        Fetch monthly weather data asynchronously from the API.

        Args:
            year: Target year for data collection
            month: Target month for data collection
            session: Aiohttp client session for making requests

        Returns:
            Optional[List[Dict]]: List of weather records or None if failed
        """
        params = {
            "pageNo": "1",
            "numOfRows": "999",
            "dataType": "XML",
            "year": str(year),
            "month": f"{month:02d}",
            "authKey": Config.WEATHER_API_KEY,
        }

        for retry in range(self.max_retries):
            try:
                async with self.semaphore:
                    async with session.get(
                        self.base_url,
                        params=params,
                        timeout=self.timeout
                    ) as response:
                        content = await response.text()

                        if response.status == 200:
                            try:
                                root = ET.fromstring(content)
                                result_code = root.findtext(".//resultCode")
                                result_msg = root.findtext(".//resultMsg")

                                if result_code != "00":
                                    logger.error(
                                        "API Error for %d-%02d: %s - %s",
                                        year,
                                        month,
                                        result_code,
                                        result_msg
                                    )
                                    return None

                                data = self._parse_weather_data(root, year, month)
                                if data:
                                    logger.info(
                                        "Successfully fetched %d records for %d-%02d",
                                        len(data),
                                        year,
                                        month
                                    )
                                    return data
                                logger.warning(
                                    "No data found for %d-%02d",
                                    year,
                                    month
                                )
                            except ET.ParseError as exc:
                                logger.error(
                                    "XML Parse Error for %d-%02d: %s",
                                    year,
                                    month,
                                    str(exc)
                                )
                        else:
                            logger.error(
                                "HTTP %d for %d-%02d",
                                response.status,
                                year,
                                month
                            )

            except asyncio.TimeoutError:
                logger.error(
                    "Timeout for %d-%02d (attempt %d)",
                    year,
                    month,
                    retry + 1
                )
            except Exception as exc:  # pylint: disable=broad-except
                logger.error(
                    "Error for %d-%02d (attempt %d): %s",
                    year,
                    month,
                    retry + 1,
                    str(exc)
                )

            if retry < self.max_retries - 1:
                await asyncio.sleep(self.retry_delay * (retry + 1))

        return None

    def _parse_weather_data(self, root: ET.Element, year: int, month: int) -> List[Dict[str, Any]]:
        """
        Parse weather data from XML response.

        Args:
            root: XML root element
            year: Data year
            month: Data month

        Returns:
            List[Dict[str, Any]]: Parsed weather records
        """
        data = []
        for idx, info in enumerate(root.findall(".//info")):
            try:
                def safe_float(value: Optional[str], field_name: str) -> float:
                    """Convert string value to float safely."""
                    if not value or value == "null":
                        return 0.0
                    try:
                        return float(value)
                    except ValueError:
                        logger.error(
                            "Invalid %s value: %s in %d-%02d",
                            field_name,
                            value,
                            year,
                            month
                        )
                        return 0.0

                row = {
                    "date": f"{year}-{month:02d}",
                    "station": info.findtext("stnko", ""),
                    "avg_temp": safe_float(info.findtext("taavg"), "avg_temp"),
                    "max_temp": safe_float(info.findtext("tamax"), "max_temp"),
                    "min_temp": safe_float(info.findtext("tamin"), "min_temp"),
                    "humidity": safe_float(info.findtext("avghm"), "humidity"),
                }

                if not row["station"]:
                    logger.warning(
                        "Empty station name in record %d for %d-%d",
                        idx,
                        year,
                        month
                    )
                    continue

                data.append(row)

            except Exception as exc:  # pylint: disable=broad-except
                logger.error(
                    "Error parsing record %d for %d-%d: %s",
                    idx,
                    year,
                    month,
                    str(exc)
                )
                continue

        return data

    async def fetch_data_async(self, start_year: int = 2016) -> pd.DataFrame:
        """
        Fetch weather data for multiple years asynchronously.

        Args:
            start_year: Starting year for data collection

        Returns:
            pd.DataFrame: Collected weather data
        """
        current_date = datetime.now()
        end_year = current_date.year
        end_month = current_date.month - 1 if current_date.month > 1 else 12
        end_year = end_year if current_date.month > 1 else end_year - 1

        logger.info(
            "데이터 수집 기간: %d년 1월 ~ %d년 %d월",
            start_year,
            end_year,
            end_month
        )

        async with aiohttp.ClientSession() as session:
            tasks = [
                self._get_monthly_data_async(year, month, session)
                for year in range(start_year, end_year + 1)
                for month in range(1, 13)
                if not (year == end_year and month > end_month)
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            all_data = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error("Error in batch %d: %s", i, str(result))
                elif isinstance(result, list):
                    all_data.extend(result)

        df = pd.DataFrame(all_data)
        if df.empty:
            logger.error("No data collected")
        return df

    def fetch_data(self, start_year: int = 2016) -> pd.DataFrame:
        """
        Synchronous wrapper for fetch_data_async.

        Args:
            start_year: Starting year for data collection

        Returns:
            pd.DataFrame: Collected weather data
        """
        return asyncio.run(self.fetch_data_async(start_year))