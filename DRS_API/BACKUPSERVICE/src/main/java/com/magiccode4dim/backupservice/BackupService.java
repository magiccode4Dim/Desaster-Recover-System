/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.magiccode4dim.backupservice;

import java.util.Date;
import java.util.List;
import java.util.Map;

import com.magiccode4dim.backupservice.requests.Objects.Container;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.annotation.Secured;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.magiccode4dim.backupservice.requests.Request;
import com.magiccode4dim.backupservice.requests.Objects.Volume;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

/**
 *
 * @author narci
 */

@RestController
@RequestMapping("/drs/api/backup")
public class BackupService {

    // private final StatusCRUD ss;
    private final String apiDockerUri;

    @Autowired
    public BackupService() {
        this.apiDockerUri = "http://localhost:5001";
    }

    // volumes
    // criar volume
    @Secured("USER")
    @PostMapping("/volumes/create")
    @ResponseBody
    public ResponseEntity<String> createContainer(@RequestBody Volume cont) {
        // cria um container
        String url = this.apiDockerUri + "/volumes/create"; // URL de destino
        // Enviar a requisição POST
        ResponseEntity<String> responseEntity = Request.sendPostRequest(cont, null, null, url);
        return responseEntity;
    }

    // get all volumes
    @Secured("USER")
    @GetMapping("/volumes/getall")
    @ResponseBody
    public ResponseEntity<String> geVolumes() {
        String url = this.apiDockerUri + "/volumes/list"; // URL de destino
        // Enviar a requisição POST
        ResponseEntity<String> responseEntity = Request.sendGetRequest(null, null, url);
        return responseEntity;

    }

    // get volume
    @Secured("USER")
    @GetMapping("/volumes/get/{volumename}")
    @ResponseBody
    public ResponseEntity<String> getVolume(@PathVariable String volumename) {
        String url = this.apiDockerUri + "/volumes/get/" + volumename; // URL de destino
        // Enviar a requisição POST
        ResponseEntity<String> responseEntity = Request.sendGetRequest(null, null, url);
        return responseEntity;

    }

    //create rysnc container
    @Secured("USER")
    @PostMapping("/containerrsync/create")
    @ResponseBody
    public ResponseEntity<String> createContainer(@RequestBody Container cont) {
        // cria um container
        
        String url = this.apiDockerUri + "/container/create"; // URL de destino
        // Enviar a requisição POST
        ResponseEntity<String> responseEntity = Request.sendPostRequest(cont, null,null, url);

         return responseEntity;
    }

    // como usar recursos avancados do mongodb

}
