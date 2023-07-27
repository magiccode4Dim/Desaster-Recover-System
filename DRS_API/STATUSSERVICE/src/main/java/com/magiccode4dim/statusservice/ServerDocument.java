package com.magiccode4dim.statusservice;

import org.springframework.data.mongodb.core.mapping.Document;


import org.springframework.data.annotation.Id;


@Document(collection = "Server")

public class ServerDocument {
    @Id
    private String id;

    private String serverAdress;

    private String nome;

    private String token;

   

    public String getServerAdress() {
        return serverAdress;
    }

    public void setServerAdress(String serverAdress) {
        this.serverAdress = serverAdress;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    
}
