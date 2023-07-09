/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.magiccode4dim.statusservice;

import java.util.Date;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.annotation.Secured;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

/**
 *
 * @author narci
 */

@RestController
@RequestMapping("/drs/api/status")
public class StatusService {

    // private final StatusCRUD ss;
    private final StatusMongo ss;

    /*
     * @Autowired
     * public StatusService(StatusCRUD ss) {
     * this.ss = ss;
     * }
     */
    @Autowired
    public StatusService(StatusMongo ss) {
        this.ss = ss;
    }

    // http://localhost:8086/drs/api/status/create
    // criate status
    @Secured("USER")
    @PostMapping("/create")
    public String teste(@RequestBody StatusDocument st) {
        st.setData_criacao(new Date());
        this.ss.save(st);
        return "Salvo Com Sucesso";
    }

    // delete status by id
    @Secured("USER")
    @DeleteMapping("/delete/{id}")
    public String delete(@PathVariable Integer id) {
        this.ss.deleteById(id);
        return "Salvo Com Sucesso";
    }

    // get status by id
    @Secured("USER")
    @GetMapping("/get/{id}")
    @ResponseBody
    public StatusDocument geStatus(@PathVariable Integer id) {
        Object u = this.ss.findById(id).orElse(null);;
        if (u == null) {
            return null;
        }
        return (StatusDocument)u;
    }

    //get all status
    @Secured("USER")
    @GetMapping("/getall")
    @ResponseBody
    public List<StatusDocument> geAllStatus() {
        return this.ss.findAll();
    }

    //como usar recursos avancados do mongodb

}
