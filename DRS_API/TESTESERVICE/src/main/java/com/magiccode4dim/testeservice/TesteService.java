/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.magiccode4dim.testeservice;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
/**
 *
 * @author narci
 */
@RestController
public class TesteService {
    
    @GetMapping("/test")
    public String teste() {
        return "TESTE";
    }
    
}
