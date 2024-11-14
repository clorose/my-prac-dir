package com.gaon.lstm.controller

import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = ["http://localhost:3000", "https://localhost:8080"])
class PingPongController {
    
    @GetMapping("/ping")
    fun ping(): Map<String, String> {
        return mapOf("message" to "pong! 🏓")
    }
    
    @GetMapping("/hello")
    fun hello(): Map<String, String> {
        return mapOf("message" to "안녕하세요! 👋")
    }
    
    @PostMapping("/echo")
    fun echo(@RequestBody request: EchoRequest): EchoResponse {
        return EchoResponse(
            message = "에코: ${request.message}",
            timestamp = System.currentTimeMillis()
        )
    }
    
    @PostMapping("/reverse")
    fun reverse(@RequestBody request: EchoRequest): EchoResponse {
        return EchoResponse(
            message = "뒤집기: ${request.message.reversed()}",
            timestamp = System.currentTimeMillis()
        )
    }
}

data class EchoRequest(val message: String)
data class EchoResponse(val message: String, val timestamp: Long)
