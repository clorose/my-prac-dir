package com.gaon.lstm

import org.springframework.web.bind.annotation.CrossOrigin
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.client.RestTemplate

@RestController
@CrossOrigin(origins = ["http://localhost:3000"]) // Next.js 애플리케이션 URL
class WeatherController {

    @GetMapping("/weather")
    fun getWeather(): String {
        val restTemplate = RestTemplate()
        val fastApiUrl = "http://localhost:8000/predict" // FastAPI 엔드포인트

        return try {
            restTemplate.getForObject(fastApiUrl, String::class.java) ?: "Error fetching data"
        } catch (e: Exception) {
            "Failed to connect to FastAPI: ${e.message}"
        }
    }
}