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

    // criar container
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

    // salvar um container como uma imagem
    // criar container
    @Secured("USER")
    @PostMapping("/container/saveasimage")
    @ResponseBody
    public ResponseEntity<String> createImageByContainer(@RequestBody ImageDocument cont) {
        // cria um container
        String url = this.apiDockerUri + "/container/commit"; // URL de destino
        Map<String, String> params = null; // Parâmetros opcionais
        // Enviar a requisição POST
        ResponseEntity<String> responseEntity = Request.sendPostRequest(cont, params, null, url);
        return responseEntity;
    }

    // faz o push da imagem no registrador privado
    @Secured("USER")
    @PostMapping("/pushtoregistry")
    @ResponseBody
    public ResponseEntity<String> pushImageOnprivatyRegistry(@RequestBody ImageDocument cont) {
        // cria um container
        String url = this.apiDockerUri + "/image/push"; // URL de destino
        Map<String, String> params = null; // Parâmetros opcionais
        // Enviar a requisição POST
        ResponseEntity<String> responseEntity = Request.sendPostRequest(cont, params, null, url);
        return responseEntity;
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
    //delete conteriner
    @Secured("USER")
    @DeleteMapping("/container/delete/{id}")
    @ResponseBody
    public  ResponseEntity<String> deleteContainer(@PathVariable String id) {
        // cria um container
        String url = this.apiDockerUri + "/container/delete/" + id; // URL de destino
        //System.out.println(url);
        ResponseEntity<String> responseEntity = Request.sendPostRequest(null, null, null, url);
        return responseEntity;
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
    public List<ImageDocument> geAllIMages() {
        return this.imageCRUD.findAll();
    }

    // retorna todos os containers em execucao
    @Secured("USER")
    @GetMapping("/container/getall")
    @ResponseBody
    public ResponseEntity<String> geAllContainers() {
        String url = this.apiDockerUri + "/containers/list"; // URL de destino
        // Enviar a requisição POST
        ResponseEntity<String> responseEntity = Request.sendGetRequest(null, null, url);
        return responseEntity;

    }

    // retorna um container com id
    @Secured("USER")
    @GetMapping("/container/get/{id}")
    @ResponseBody
    public ResponseEntity<String> geContainer(@PathVariable String id) {
        String url = this.apiDockerUri + "/container/" + id; // URL de destino
        // Enviar a requisição POST
        ResponseEntity<String> responseEntity = Request.sendGetRequest(null, null, url);
        return responseEntity;

    }

    // retorna todos os registradores disponiveis
    @Secured("USER")
    @GetMapping("/registry/getall")
    @ResponseBody
    public ResponseEntity<String> geRegistrys() {
        String url = this.apiDockerUri + "/registry/list"; // URL de destino
        // Enviar a requisição POST
        ResponseEntity<String> responseEntity = Request.sendGetRequest(null, null, url);
        return responseEntity;

    }

    // como usar recursos avancados do mongodb

}
