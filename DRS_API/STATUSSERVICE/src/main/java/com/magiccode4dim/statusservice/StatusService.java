/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.magiccode4dim.statusservice;

import java.util.Date;
import java.util.List;
import java.util.Map;

import javax.websocket.server.PathParam;

import org.apache.catalina.Container;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.annotation.Secured;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.magiccode4dim.statusservice.util.RandomToken;
import com.thoughtworks.xstream.mapper.Mapper.Null;

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
    private final String apiDockerUri;

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
        this.apiDockerUri = "http://localhost:5001";
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
        } else {
            new Object() {
                // SERVIDOR NAO ENCONTRADO
                public int response = 404;
            };
        }
        return new Object() {
            // TUDO BEM
            public int response = 200;
        };
    }

    // delete status by id
    @Secured("USER")
    @DeleteMapping("/delete/{id}")
    public Object delete(@PathVariable String id) {
        this.ss.deleteById(id);
        return new Object() {
                // TUDO BEM
                public Integer response = 200;
            };
    }

    //delete all status
    @Secured("USER")
    @DeleteMapping("/deleteall")
    public Object deleteall() {
        this.ss.deleteAll();
        return new Object() {
                // TUDO BEM
                public Integer response = 200;
            };
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

    // get last status server
    @Secured("USER")
    @GetMapping("/getlaststatus/{serverid}")
    @ResponseBody
    public StatusDocument getLastStatus(@PathVariable String serverid) {
        ServerDocument sr = getServer(serverid);
        List<StatusDocument> sds = null;
        if(sr==null){
            sds = this.ss.findByServerID(serverid);
        }else{
            sds = this.ss.findByServerID(sr.getId());
        }
        if (sds.isEmpty()) {
            return new StatusDocument();
        }
        Object u = sds.get(sds.size() - 1);

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
    public Object createServer(@RequestBody ServerDocument st) {
        String token = RandomToken.generateRandomToken(32) + RandomToken.generateRandomString();
        st.setToken(token);
        st.setId(RandomToken.generateRandomToken(32));
        this.sermongo.save(st);
        return new Object() {
            // TUDO BEM
            public int response = 200;
        };

    }

    // getallservers
    // get all status
    @Secured("USER")
    @GetMapping("/server/getall")
    @ResponseBody
    public List<ServerDocument> geAllServes() {
        return this.sermongo.findAll();
    }

    @Secured("USER")
    @GetMapping("/server/get/{id}")
    @ResponseBody
    public ServerDocument getServer(@PathVariable String id) {
        Object u = this.sermongo.findById(id).orElse(null);
        if (u == null ) {
            if(this.sermongo.findByNome(id).size()>0)
                u = this.sermongo.findByNome(id).get(0);
        }
        return (ServerDocument) u;
    }

    // saber se um server esta down
    @Secured("USER")
    @GetMapping("/server/isdown/{id}")
    @ResponseBody
    public Object getIsDown(@PathVariable String id) {
        List<StatusDocument> sds = this.ss.findByServerID(id);
        if (sds.isEmpty()) {
            return new StatusDocument();
        }
        Object u = sds.get(sds.size() - 1);
        // deve procurar saber se o time stamp da recuperacao enquadra-se com o ultimo
        // time stamp
        if (u == null) {
            return null;
        }
        // se ter mais de 2 milissegundos de diferenca entao o servidor esta down
        Long now = new Date().getTime();
        StatusDocument sta = (StatusDocument) u;
        Long initial = sta.getData_criacao().getTime();
        if (((now - initial) / 1000) > 3) {
            return new Object() {
                // TUDO BEM
                public Boolean response = true;
            };
        } else {
            return new Object() {
                // TUDO BEM
                public Boolean response = false;
            };
        }

    }

    // retorna uma lista de todos os servidores que estao em baixo
    @Secured("USER")
    @GetMapping("/server/whoisdown")
    @ResponseBody
    public List<ServerDocument> whoisdown() {
        List<ServerDocument> servs = this.sermongo.findAll();
        List<ServerDocument> downservrs = this.sermongo.findAll();
        for (ServerDocument s : servs) {
            List<StatusDocument> sds = this.ss.findByServerID(s.getId());
            if (sds.isEmpty()) {
                continue;
            }
            Object u = sds.get(sds.size() - 1);
            // deve procurar saber se o time stamp da recuperacao enquadra-se com o ultimo
            // time stamp
            if (u == null) {
                return null;
            }
            // se ter mais de 2 milissegundos de diferenca entao o servidor esta down
            Long now = new Date().getTime();
            StatusDocument sta = (StatusDocument) u;
            Long initial = sta.getData_criacao().getTime();
            if (((now - initial) / 1000) > 3) {
                continue;
            }else{
                downservrs.remove(servs.indexOf(s));
            }

        }
        return downservrs;

    }

    // como usar recursos avancados do mongodb

}
