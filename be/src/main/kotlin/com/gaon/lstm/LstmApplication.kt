package com.gaon.lstm

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.context.annotation.Bean
import org.springframework.security.config.annotation.web.builders.HttpSecurity
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity
import org.springframework.security.web.SecurityFilterChain

@SpringBootApplication
@EnableWebSecurity
class LstmApplication {
	@Bean
	fun filterChain(http: HttpSecurity): SecurityFilterChain {
		return http
			.csrf { it.disable() }
			.authorizeHttpRequests { it.anyRequest().permitAll() }
			.build()
	}
}

fun main(args: Array<String>) {
	runApplication<LstmApplication>(*args)
}