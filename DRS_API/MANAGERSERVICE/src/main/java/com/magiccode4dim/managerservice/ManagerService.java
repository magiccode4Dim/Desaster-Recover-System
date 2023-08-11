/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.magiccode4dim.managerservice;

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

import com.magiccode4dim.managerservice.requests.Request;
import com.magiccode4dim.managerservice.requests.Objects.Network;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.magiccode4dim.managerservice.util.RandomToken;
import java.util.List;

/**
 *
 * @author narci
 */
@RestController
@RequestMapping("/drs/api/manager")
public class ManagerService {

    // private final StatusCRUD ss;
    private final String apiDockerUri;
    private final ServiceMongo serviceCRUD;

    @Autowired
    public ManagerService(ServiceMongo serviceCRUD) {
        this.apiDockerUri = "http://localhost:5002";
        this.serviceCRUD = serviceCRUD;
    }

    @Secured("USER")
    @PostMapping("/networks/create")
    @ResponseBody
    public ResponseEntity<String> createNet(@RequestBody Network cont) {
        // cria um container
        String url = this.apiDockerUri + "/network/create"; // URL de destino
        // Enviar a requisição POST
        ResponseEntity<String> responseEntity = Request.sendPostRequest(cont, null, null, url);
        return responseEntity;
    }

     @Secured("USER")
     @GetMapping("/networks/getall")
     @ResponseBody
     public ResponseEntity<String> geNets() {
         String url = this.apiDockerUri + "/networks/list"; // URL de destino
         // Enviar a requisição POST
         ResponseEntity<String> responseEntity = Request.sendGetRequest(null, null, url);
         return responseEntity;
 
     }

    @Secured("USER")
    @PostMapping("/service/create")
    @ResponseBody
    public ResponseEntity<String> createService(@RequestBody Object cont) {

        String url = this.apiDockerUri + "/service/create"; // URL de destino

        ResponseEntity<String> responseEntity = Request.sendPostRequest(cont, null, null, url);


        String responseBody = responseEntity.getBody(); // Corpo da resposta JSON

        // Parse do JSON
        JSONObject jsonObject = new JSONObject(responseBody);

        // Obtém o valor da chave "response"
        int responseValue = jsonObject.getInt("response");

        if(responseValue==201){
            ServiceDocument s = new ServiceDocument();
            s.setId(RandomToken.generateRandomString() + RandomToken.generateRandomToken(15));
            s.setService(cont);

            this.serviceCRUD.save(s);
        }
  
        return responseEntity;
    }

    //get services

     @Secured("USER")
     @GetMapping("/services/getall")
     @ResponseBody
     public ResponseEntity<String> geServices() {
         String url = this.apiDockerUri + "/services/list"; // URL de destino
         // Enviar a requisição POST
         ResponseEntity<String> responseEntity = Request.sendGetRequest(null, null, url);
         return responseEntity;
 
     }

     //get service by id
     @Secured("USER")
     @GetMapping("/services/get/{id}")
     @ResponseBody
     public ResponseEntity<String> geService(@PathVariable String id) {
         String url = this.apiDockerUri + "/services/get/"+id; // URL de destino
         // Enviar a requisição POST
         ResponseEntity<String> responseEntity = Request.sendGetRequest(null, null, url);
         return responseEntity;
 
     }


     //delete service
     @Secured("USER")
     @DeleteMapping("/services/delete/{id}")
     @ResponseBody
     public ResponseEntity<String> deleteService(@PathVariable String id) {
        //antes, precisa saber o nome do servico
        String responseBody = geService(id).getBody();
        JSONObject jsonObject = new JSONObject(responseBody);
        //s.Spec.Name
        String nome = jsonObject.getJSONObject("Spec").getString("Name");

         String url = this.apiDockerUri + "/services/delete/"+id; // URL de destino
         // Enviar a requisição POST
         ResponseEntity<String> responseEntity = Request.sendGetRequest(null, null, url);

         //apaga na base de dados

         List<ServiceDocument> allser = this.serviceCRUD.findAll();
         for(ServiceDocument s : allser){
                Object service = s.getService();
                if (service instanceof Map) {
                    Map<String, Object> serviceMap = (Map<String, Object>) service;
                    if (serviceMap.containsKey("Name")) {
                        String n = (String)serviceMap.get("Name");
                        if(n.equals(nome)){
                            this.serviceCRUD.deleteById(s.getId());
                            break;
                        }
                    }
                }
         }

         

         return responseEntity;
 
     }


     //scale service
     /*
     @Secured("USER")
     @PostMapping("/services/scale/{id}/{rep}/{v}")
     @ResponseBody
     public ResponseEntity<String> serviceScale(@PathVariable String id, @PathVariable Integer rep,@PathVariable Integer v) {
         String url = this.apiDockerUri + "/service/scale/"+id+"/"+String.valueOf(rep)+"/"+String.valueOf(v); // URL de destino
         // Enviar a requisição POST
         ResponseEntity<String> responseEntity = Request.sendPostRequest(null,null, null, url);
         return responseEntity;
 
     }*/

   
    // como usar recursos avancados do mongodb

}
