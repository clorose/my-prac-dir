// path : src/app/weather/page.tsx
// description : 날씨 예측 페이지

"use client";
import { useState } from "react";

export default function WeatherPage() {
  const [weatherData, setWeatherData] = useState<
    {
      date: string;
      avg_temp: number;
      max_temp: number;
      min_temp: number;
      humidity: number;
    }[]
  >([]);
  const [error, setError] = useState<string | null>(null);

  const fetchWeatherData = async () => {
    try {
      const res = await fetch("http://localhost:8080/weather");
      if (!res.ok) {
        throw new Error("Failed to fetch weather data");
      }
      const data = await res.json();
      const parsedData = data.predictions || [];
      setWeatherData(parsedData);
      setError(null);
    } catch (e: unknown) {
      const errorMessage =
        e instanceof Error ? e.message : "Unknown error occurred";
      setError(errorMessage);
    }
  };

  // 최고/최저 온도 계산
  const maxTemp = Math.max(...weatherData.map((item) => item.max_temp));
  const minTemp = Math.min(...weatherData.map((item) => item.min_temp));

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">📊 날씨 예측 데이터</h1>
      <button
        onClick={fetchWeatherData}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 mb-6"
      >
        날씨 데이터 불러오기
      </button>

      {error && <div className="text-red-500 mb-4">❌ 에러: {error}</div>}

      {weatherData.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="table-auto border-collapse border border-gray-300 w-full">
            <thead>
              <tr>
                <th className="border border-gray-300 px-4 py-2">📅 날짜</th>
                <th className="border border-gray-300 px-4 py-2">
                  🌡️ 평균 온도 (°C)
                </th>
                <th className="border border-gray-300 px-4 py-2">
                  🔥 최고 온도 (°C)
                </th>
                <th className="border border-gray-300 px-4 py-2">
                  ❄️ 최저 온도 (°C)
                </th>
                <th className="border border-gray-300 px-4 py-2">
                  💧 습도 (%)
                </th>
              </tr>
            </thead>
            <tbody>
              {weatherData.map((item) => (
                <tr key={item.date} className="text-center">
                  <td className="border border-gray-300 px-4 py-2">
                    {item.date}
                  </td>
                  <td className="border border-gray-300 px-4 py-2">
                    {item.avg_temp.toFixed(2)}
                  </td>
                  <td
                    className={`border border-gray-300 px-4 py-2 ${
                      item.max_temp === maxTemp ? "text-red-500 font-bold" : ""
                    }`}
                  >
                    {item.max_temp.toFixed(2)}
                  </td>
                  <td
                    className={`border border-gray-300 px-4 py-2 ${
                      item.min_temp === minTemp ? "text-blue-500 font-bold" : ""
                    }`}
                  >
                    {item.min_temp.toFixed(2)}
                  </td>
                  <td className="border border-gray-300 px-4 py-2">
                    {item.humidity.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>날씨 데이터를 불러오려면 버튼을 클릭하세요.</p>
      )}
    </div>
  );
}
