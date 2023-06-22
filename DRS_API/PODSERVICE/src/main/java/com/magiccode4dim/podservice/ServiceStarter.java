/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.magiccode4dim.podservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

/**
 *
 * @author narci
 */
@SpringBootApplication
@EnableDiscoveryClient
public class ServiceStarter {
    public static void main(String[] args) {
        SpringApplication.run(ServiceStarter.class, args);
    } 
}