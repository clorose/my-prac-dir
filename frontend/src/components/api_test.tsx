import { useState, useEffect } from 'react';
import axios from 'axios';

interface ApiResponse {
  message: string;
}

const ApiTest = (): JSX.Element => {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<ApiResponse>('http://localhost:8000/api/data');
        setData(response.data);
      } catch (e) {
        if (axios.isAxiosError(e)) {
          setError(e.response?.data?.message || e.message);
        } else {
          setError('An unknown error occurred');
        }
      }
    };

    fetchData();
  }, []);

  return (
    <div className="p-4 bg-gray-100 rounded-lg shadow">
      <h2 className="text-xl font-bold mb-4">FastAPI Connection Test</h2>
      {error && <p className="text-red-500">Error: {error}</p>}
      {data && (
        <div className="bg-white p-3 rounded">
          <p className="font-semibold">Response from FastAPI:</p>
          <p>{data.message}</p>
        </div>
      )}
      {!data && !error && <p>Loading...</p>}
    </div>
  );
};

export default ApiTest;