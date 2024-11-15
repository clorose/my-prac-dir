

'use client'
import { useState } from 'react'

export default function Home() {
  const [responses, setResponses] = useState<{[key: string]: string}>({})
  const [inputMessage, setInputMessage] = useState('')

  // GET 요청들
  const testPing = async () => {
    const res = await fetch('http://localhost:8080/api/ping')
    const data = await res.json()
    setResponses(prev => ({ ...prev, ping: data.message }))
  }

  const testHello = async () => {
    const res = await fetch('http://localhost:8080/api/hello')
    const data = await res.json()
    setResponses(prev => ({ ...prev, hello: data.message }))
  }

  // POST 요청들
  const testEcho = async () => {
    const res = await fetch('http://localhost:8080/api/echo', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: inputMessage })
    })
    const data = await res.json()
    setResponses(prev => ({ ...prev, echo: data.message }))
  }

  const testReverse = async () => {
    const res = await fetch('http://localhost:8080/api/reverse', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: inputMessage })
    })
    const data = await res.json()
    setResponses(prev => ({ ...prev, reverse: data.message }))
  }

  return (
      <div className="p-6 max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold mb-6">API 테스트 놀이터 🎮</h1>

        {/* GET 요청 버튼들 */}
        <div className="space-x-2 mb-6">
          <button
              onClick={testPing}
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            핑퐁 테스트
          </button>
          <button
              onClick={testHello}
              className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          >
            안녕 테스트
          </button>
        </div>

        {/* POST 요청 섹션 */}
        <div className="mb-6">
          <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              className="border p-2 rounded w-full mb-2"
              placeholder="메시지를 입력하세요"
          />
          <div className="space-x-2">
            <button
                onClick={testEcho}
                className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600"
            >
              에코 테스트
            </button>
            <button
                onClick={testReverse}
                className="bg-pink-500 text-white px-4 py-2 rounded hover:bg-pink-600"
            >
              뒤집기 테스트
            </button>
          </div>
        </div>

        {/* 응답 결과들 */}
        <div className="bg-gray-100 p-4 rounded">
          <h2 className="font-bold mb-2">응답 결과:</h2>
          {Object.entries(responses).map(([key, value]) => (
              <div key={key} className="mb-2">
                <span className="font-semibold">{key}: </span>
                {value}
              </div>
          ))}
        </div>
      </div>
  )
}