/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.magiccode4dim.backupservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;

/**
 *
 * @author narci
 */
@SpringBootApplication
@EnableDiscoveryClient

// security
@EnableWebSecurity
public class ServiceStarter {
    public static void main(String[] args) {
        SpringApplication.run(ServiceStarter.class, args);
    }
     //todas as urls que inciam com API devem ser autenticadas

    @EnableWebSecurity
    public static class SecurityConfig extends WebSecurityConfigurerAdapter {
        String username = System.getenv("USERNAME");
        String password = System.getenv("PASSWORD");
        @Override
        protected void configure(HttpSecurity http) throws Exception {
            http
                    .authorizeRequests()
                    .anyRequest().authenticated()
                    .and()
                    .httpBasic()
                    .and()
                    .csrf()
                    //.csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse());
                    .disable();
        }

        @Override
        protected void configure(AuthenticationManagerBuilder auth) throws Exception {
            auth.inMemoryAuthentication()
                    .withUser(username)
                    .password("{noop}"+password)
                    .roles("USER");
        }
    }
}
