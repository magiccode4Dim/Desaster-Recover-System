/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.magiccode4dim.failoverservice;

import java.util.Date;
import java.util.List;
import java.util.Map;
import org.json.JSONObject;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.annotation.Secured;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.magiccode4dim.failoverservice.requests.Request;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.magiccode4dim.failoverservice.util.RandomToken;
import java.util.List;

/**
 *
 * @author narci
 */
@RestController
@RequestMapping("/drs/api/failover")
public class FailoverService {

    // private final StatusCRUD ss;

    private final FailoverMongo foCRUD;

    @Autowired
    public FailoverService(FailoverMongo foCRUD) {
        this.foCRUD = foCRUD;
    }

    // create new failover
    @Secured("USER")
    @PostMapping("/create")
    public Object create(@RequestBody FailoverDocument st) {
        st.setId(RandomToken.generateRandomString() + RandomToken.generateRandomToken(16));
        try {
            this.foCRUD.save(st);
        } catch (Exception e) {
            return new Object() {
                // TUDO BEM
                public int response = 500;
            };
        }
        return new Object() {
            // TUDO BEM
            public int response = 200;
        };

    }

    @Secured("USER")
    @GetMapping("/get/{id}")
    @ResponseBody
    public FailoverDocument geFailover(@PathVariable String id) {
        Object u = this.foCRUD.findById(id).orElse(null);
        if (u == null) {
            return null;
        }
        return (FailoverDocument) u;
    }

    //get failover by server id
    @Secured("USER")
    @GetMapping("/getbyserid/{id}")
    @ResponseBody
    public FailoverDocument getFailoverByserverId(@PathVariable String id) {
        List<FailoverDocument> sds = this.foCRUD.findByServerID(id);
        if(sds.isEmpty()){
             return null;
        }
        
        return sds.get(0);
    }


    // get all status
    @Secured("USER")
    @GetMapping("/getall")
    @ResponseBody
    public List<FailoverDocument> geAllFailover() {
        return this.foCRUD.findAll();
    }

    // delete failover
    @Secured("USER")
    @DeleteMapping("/delete/{id}")
    @ResponseBody
    public Object delete(@PathVariable String id) {
        this.foCRUD.deleteById(id);
        return new Object() {
            // TUDO BEM
            public int response = 200;
        };
    }

    // verifica se nao existe nenhum failover que possui aquele nome de servico
    @Secured("USER")
    @GetMapping("/exists/{name}")
    @ResponseBody
    public Object serviceNameExists(@PathVariable String name) {
        List<FailoverDocument> fod = this.foCRUD.findAll();
        for (FailoverDocument f : fod) {
            List<Object> services = f.getServices();
            for (Object o : services) {
                if (o instanceof Map) {
                    Map<String, Object> serviceMap = (Map<String, Object>) o;
                    if (serviceMap.containsKey("Name")) {
                        String n = (String) serviceMap.get("Name");
                        if (n.equals(name)) {
                            return new Object() {
                                // TUDO BEM
                                public boolean res = true;
                            };
                        }

                    }
                }
            }
        }
        return new Object() {
            // TUDO BEM
            public boolean res = false;
        };
    }

    // como usar recursos avancados do mongodb

}
