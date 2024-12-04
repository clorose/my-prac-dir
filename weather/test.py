import os
import requests
import xml.etree.ElementTree as ET
from collections import defaultdict
from dotenv import load_dotenv
import statistics

# .env 파일 로드
load_dotenv()

# API 관련 환경 변수 로드
API_KEY = os.getenv("WEATHER_API_KEY")
YEAR = "2016"
MONTH = "09"

# API 요청 URL 생성
url = f"https://apihub.kma.go.kr/api/typ02/openApi/SfcMtlyInfoService/getMmSumry"
params = {
    "pageNo": 1,
    "numOfRows": 10,
    "dataType": "XML",
    "year": YEAR,
    "month": MONTH,
    "authKey": API_KEY,
}


# API 요청 함수
def get_weather_data(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.content
    return None


# XML 데이터 파싱 함수
def parse_weather_data(xml_data):
    root = ET.fromstring(xml_data)
    return root


# 1. 가장 더웠던 도시와 가장 덜 더웠던 도시의 기온 차이
def find_hottest_and_coldest_cities(root):
    hottest_city = None
    coldest_city = None
    max_temp = float("-inf")
    min_temp = float("inf")

    for info in root.iter("info"):
        city_name = info.findtext("stnko")
        max_city_temp = info.findtext("tamax")
        min_city_temp = info.findtext("tamin")

        if max_city_temp and float(max_city_temp) > max_temp:
            hottest_city = city_name
            max_temp = float(max_city_temp)

        if min_city_temp and float(min_city_temp) < min_temp:
            coldest_city = city_name
            min_temp = float(min_city_temp)

    return hottest_city, max_temp, coldest_city, min_temp


# 2. 가장 평범한 도시 찾기 (중앙값 기온)
def find_most_average_temp_city(root):
    temps = []
    city_temps = {}

    # 각 도시의 평균 기온 기록
    for info in root.iter("info"):
        city_name = info.findtext("stnko")
        avg_temp = info.findtext("taavg")

        if avg_temp is not None:
            temp = float(avg_temp)
            temps.append(temp)
            city_temps[city_name] = temp

    # 중앙값에 가장 가까운 도시 찾기
    median_temp = statistics.median(temps)
    closest_city = min(city_temps, key=lambda x: abs(city_temps[x] - median_temp))

    return closest_city, median_temp


# 3. 최고 기온과 최저 기온이 같은 도시 찾기
def find_cities_with_same_max_and_min_temp(root):
    same_temp_cities = []

    for info in root.iter("info"):
        city_name = info.findtext("stnko")
        max_temp = info.findtext("tamax")
        min_temp = info.findtext("tamin")

        if max_temp and min_temp and max_temp == min_temp:
            same_temp_cities.append(city_name)

    return same_temp_cities


# 데이터 가져오기
weather_data = get_weather_data(url, params)

# 데이터가 성공적으로 가져와졌다면 분석 수행
if weather_data:
    root = parse_weather_data(weather_data)

    # 1. 가장 더웠던 도시와 가장 덜 더웠던 도시의 기온 차이 계산
    hottest_city, hottest_temp, coldest_city, coldest_temp = (
        find_hottest_and_coldest_cities(root)
    )
    if hottest_city and coldest_city:
        temp_diff = hottest_temp - coldest_temp
        print(
            f"The hottest city is {hottest_city} with a max temperature of {hottest_temp}°C."
        )
        print(
            f"The coldest city is {coldest_city} with a min temperature of {coldest_temp}°C."
        )
        print(
            f"The temperature difference between {hottest_city} and {coldest_city} is {temp_diff}°C."
        )

    # 2. 가장 평범한 도시 찾기
    city, median_temp = find_most_average_temp_city(root)
    print(
        f"The city with the most average temperature is {city} with a temperature of {median_temp}°C."
    )

    # 3. 최고 기온과 최저 기온이 같은 도시 찾기
    cities_with_same_temps = find_cities_with_same_max_and_min_temp(root)
    if cities_with_same_temps:
        print(
            f"Cities where both max and min temperatures are the same: {', '.join(cities_with_same_temps)}."
        )
    else:
        print("There are no cities where both max and min temperatures are the same.")
else:
    print("Failed to retrieve data from API.")
