package com.magiccode4dim.statusservice;

import org.springframework.data.mongodb.core.mapping.Document;

import java.util.Date;


import org.springframework.data.annotation.Id;


@Document(collection = "status")
public class StatusDocument {
    @Id
    private Integer id;

    private String serverAdress;

    private Date data_criacao;

    private Boolean value = false;

    private Integer id_service;

    public Integer getId_service() {
        return id_service;
    }

    public void setId_service(Integer id_service) {
        this.id_service = id_service;
    }

    public Boolean getValue() {
        return value;
    }

    public void setValue(Boolean value) {
        this.value = value;
    }

    public Date getData_criacao() {
        return data_criacao;
    }

    public void setData_criacao(Date data_criacao) {
        this.data_criacao = data_criacao;
    }

    public String getServerAdress() {
        return serverAdress;
    }

    public void setServerAdress(String serverAdress) {
        this.serverAdress = serverAdress;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

}
