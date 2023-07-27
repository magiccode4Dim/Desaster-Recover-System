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

import com.magiccode4dim.statusservice.util.RandomToken;

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
    private final ServerMongo sermongo;

    /*
     * @Autowired
     * public StatusService(StatusCRUD ss) {
     * this.ss = ss;
     * }
     */
    @Autowired
    public StatusService(StatusMongo ss, ServerMongo sm) {
        this.ss = ss;
        this.sermongo = sm;
    }

    // http://localhost:8086/drs/api/status/create
    // criate status
    @Secured("USER")
    @PostMapping("/create")
    public Object create(@RequestBody StatusDocument st) {
        String token = st.getToken();
        List<ServerDocument> servers = this.sermongo.findByToken(token);
        if (servers.size() > 0) {
            ServerDocument ser = servers.get(0);
            st.setId(ser.getId());
            st.setServerID(ser.getId());
            st.setId(RandomToken.generateRandomString() + RandomToken.generateRandomToken(15));
            st.setData_criacao(new Date());
            this.ss.save(st);
        }else{
            new Object() {
            //SERVIDOR NAO ENCONTRADO
                public int response = 404;
            };
        }
        return  new Object() {
            //TUDO BEM
                public int response = 200;
            };
        }

    // delete status by id
    @Secured("USER")
    @DeleteMapping("/delete/{id}")
    public String delete(@PathVariable String id) {
        this.ss.deleteById(id);
        return "Salvo Com Sucesso";
    }

    // get status by id
    @Secured("USER")
    @GetMapping("/get/{id}")
    @ResponseBody
    public StatusDocument geStatus(@PathVariable String id) {
        Object u = this.ss.findById(id).orElse(null);
        ;
        if (u == null) {
            return null;
        }
        return (StatusDocument) u;
    }

    // get all status
    @Secured("USER")
    @GetMapping("/getall")
    @ResponseBody
    public List<StatusDocument> geAllStatus() {
        return this.ss.findAll();
    }

    // criar um servidor
    @Secured("USER")
    @PostMapping("/server/create")
    public String createServer(@RequestBody ServerDocument st) {
        String token = RandomToken.generateRandomToken(32) + RandomToken.generateRandomString();
        st.setToken(token);
        st.setId(RandomToken.generateRandomToken(32));
        this.sermongo.save(st);
        return token;
    }

    // como usar recursos avancados do mongodb

}
