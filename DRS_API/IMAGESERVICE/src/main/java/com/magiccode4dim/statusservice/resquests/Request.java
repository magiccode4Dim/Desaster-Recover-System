package com.magiccode4dim.statusservice.resquests;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.*;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import java.util.Map;

public class Request {

    public static <T> ResponseEntity<String> sendPostRequest(T data, Map<String, String> params, HttpHeaders headers,
            String url) {
        // Configurar o ObjectMapper para serializar o objeto em JSON
        ObjectMapper objectMapper = new ObjectMapper();
        String jsonData;
        try {
            jsonData = objectMapper.writeValueAsString(data);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
            return null;
        }

        // Configuração do RestTemplate
        RestTemplate restTemplate = new RestTemplate();

        // Configuração dos cabeçalhos da requisição
        if (headers == null) {
            headers = new HttpHeaders();
        }
        headers.setContentType(MediaType.APPLICATION_JSON);

        // Configuração do corpo da requisição
        MultiValueMap<String, String> body = new LinkedMultiValueMap<>();
        body.add("json", jsonData);

        // Adicionar parâmetros à requisição, se fornecidos
        if (params != null) {
            for (Map.Entry<String, String> entry : params.entrySet()) {
                body.add(entry.getKey(), entry.getValue());
            }
        }

        // Configuração da entidade HTTP
        HttpEntity<MultiValueMap<String, String>> requestEntity = new HttpEntity<>(body, headers);

        // Chamada POST para a URL de destino
        ResponseEntity<String> responseEntity = restTemplate.exchange(url, HttpMethod.POST, requestEntity,
                String.class);

        return responseEntity;
    }

    public static <T> ResponseEntity<String> sendGetRequest(Map<String, String> params, HttpHeaders headers,
            String url) {
        // Configuração do RestTemplate
        RestTemplate restTemplate = new RestTemplate();

        // Configuração dos cabeçalhos da requisição
        if (headers == null) {
            headers = new HttpHeaders();
        }

        // Adicionar parâmetros à URL, se fornecidos
        if (params != null) {
            url += "?";
            for (Map.Entry<String, String> entry : params.entrySet()) {
                url += entry.getKey() + "=" + entry.getValue() + "&";
            }
            url = url.substring(0, url.length() - 1); // Remover o último "&" da URL
        }

        // Configuração da entidade HTTP
        HttpEntity<String> requestEntity = new HttpEntity<>(headers);

        // Chamada GET para a URL de destino
        ResponseEntity<String> responseEntity = restTemplate.exchange(url, HttpMethod.GET, requestEntity, String.class);

        return responseEntity;
    }
      public static ResponseEntity<String> sendDeleteRequest(Map<String, String> params, HttpHeaders headers, String url) {
        // Configuração do RestTemplate
        RestTemplate restTemplate = new RestTemplate();

        // Configuração dos cabeçalhos da requisição
        if (headers == null) {
            headers = new HttpHeaders();
        }

        // Adicionar parâmetros à URL, se fornecidos
        if (params != null) {
            url += "?";
            for (Map.Entry<String, String> entry : params.entrySet()) {
                url += entry.getKey() + "=" + entry.getValue() + "&";
            }
            url = url.substring(0, url.length() - 1); // Remover o último "&" da URL
        }

        // Configuração da entidade HTTP
        HttpEntity<String> requestEntity = new HttpEntity<>(headers);

        // Chamada DELETE para a URL de destino
        ResponseEntity<String> responseEntity = restTemplate.exchange(url, HttpMethod.DELETE, requestEntity, String.class);

        return responseEntity;
    }

}
