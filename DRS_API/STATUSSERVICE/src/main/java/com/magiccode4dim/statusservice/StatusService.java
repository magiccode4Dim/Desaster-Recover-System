/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.magiccode4dim.statusservice;
import java.sql.Date;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
/**
 *
 * @author narci
 */

@RestController
@RequestMapping("/drs/api/status")
public class StatusService {
    
    private final StatusCRUD ss;

    @Autowired
    public StatusService(StatusCRUD ss) {
        this.ss = ss;
    }
    //http://localhost:8086/drs/api/status/create
    @GetMapping("/create")
    public String teste() {
       
        Status newStatus =  new Status();
        newStatus.setData_criacao(new Date(2023,7,7));
        newStatus.setId_service(1);
        newStatus.setServerAdress("narciso.com");
        newStatus.setValue(true);
        ss.save(newStatus);

        return "TESTE";
    }
    
}
