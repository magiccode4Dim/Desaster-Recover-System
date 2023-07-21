/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.magiccode4dim.statusservice;

import java.io.IOException;
import java.util.Date;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.annotation.Secured;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import com.magiccode4dim.statusservice.resquests.*;
import com.magiccode4dim.statusservice.resquests.Objects.Container;
import com.magiccode4dim.statusservice.resquests.Objects.Image;

import org.springframework.http.*;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

//docker

/**
 *
 * @author narci
 */

@RestController
@RequestMapping("/drs/api/image")
public class ImageService {

    private final ImageMongo imageCRUD;
    private String apiDockerUri;

    @Autowired
    public ImageService(ImageMongo ss) {
        this.imageCRUD = ss;
        this.apiDockerUri = "http://localhost:5000";

    }

    @Secured("USER")
    @PostMapping("/download")
    public String downloadImage(@RequestBody ImageDocument ido) {
        // fazer o download da imagem no docker hub e guarda no runner
        String url = this.apiDockerUri + "/images/pull"; // URL de destino
        Image data = new Image(ido.getNome(), ido.getTag()); // Objeto a ser enviado
        Map<String, String> params = null; // Parâmetros opcionais
        HttpHeaders headers = null; // Cabeçalhos opcionais
        // Enviar a requisição POST
        ResponseEntity<String> responseEntity = Request.sendPostRequest(data, params, headers, url);
        // Exibir a resposta
        if (responseEntity != null) {
            String responseBody = responseEntity.getBody();
            System.out.println("Response Body: " + responseBody);
            return responseBody;
        }
        return "NUll";
    }

    // o adiministrador cria uma imagem
    @Secured("USER")
    @PostMapping("/container/create")
    public String createContainer(@RequestBody Container cont) {
        // cria um container
        String url = this.apiDockerUri + "/container/create"; // URL de destino
        Map<String, String> params = null; // Parâmetros opcionais
        HttpHeaders headers = null; // Cabeçalhos opcionais
        // Enviar a requisição POST
        ResponseEntity<String> responseEntity = Request.sendPostRequest(cont, params, headers, url);

        // Exibir a resposta
        if (responseEntity != null) {
            String responseBody = responseEntity.getBody();
            System.out.println("Response Body: " + responseBody);
            return responseBody;
        }

        return "Salvo Com Sucesso";
    }

    @Secured("USER")
    @PostMapping("/container/start/{id}")
    public String startContainer(@PathVariable String id) {
        // cria um container
        String url = this.apiDockerUri + "/container/start/" + id; // URL de destino
        Map<String, String> params = null; // Parâmetros opcionais
        HttpHeaders headers = null; // Cabeçalhos opcionais
        // Enviar a requisição POST
        ResponseEntity<String> responseEntity = Request.sendPostRequest(null, params, headers, url);
        // Exibir a resposta
        if (responseEntity != null) {
            String responseBody = responseEntity.getBody();
            System.out.println("Response Body: " + responseBody);
            return responseBody;
        }

        return "Salvo Com Sucesso";
    }

    @Secured("USER")
    @PostMapping("/createnewimage")
    public String createImage(@RequestBody ImageDocument cont) {
        this.imageCRUD.save(cont);
        return "Salvo Com Sucesso";
    }

    // apagar imagem
    @Secured("USER")
    @DeleteMapping("/delete/{id}")
    public String delete(@PathVariable Integer id) {
        this.imageCRUD.deleteById(id);
        return "Salvo Com Sucesso";
    }

    // pegar a imagem com id
    @Secured("USER")
    @GetMapping("/get/{id}")
    @ResponseBody
    public ImageDocument getImage(@PathVariable Integer id) {
        Object u = this.imageCRUD.findById(id).orElse(null);
        
        if (u == null) {
            return null;
        }
        return (ImageDocument) u;
    }

    // pegar todas imagens
    @Secured("USER")
    @GetMapping("/getall")
    @ResponseBody
    public List<ImageDocument> geAllStatus() {
        return this.imageCRUD.findAll();
    }

    // como usar recursos avancados do mongodb

}
