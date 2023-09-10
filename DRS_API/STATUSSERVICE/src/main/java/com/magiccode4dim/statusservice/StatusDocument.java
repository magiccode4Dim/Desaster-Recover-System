package com.magiccode4dim.statusservice;

import org.springframework.data.mongodb.core.mapping.Document;

import java.util.Date;

import org.springframework.data.annotation.Id;


@Document(collection = "status")
public class StatusDocument {
    @Id
    private String id;

    private String serverID;
    private Date data_criacao;

    private Boolean value = false;

    private String token;
    //DATA received
    private Double cpu;
    private Double memory;
    private Double disc;
    private Double totalup;
    private Double totaldown;
    private Double nowup;
    private Double nowdown;

    /* {
        "cpu":cpu_usage,
        "memory":memory_usage,
        "disc":disk_usage
    } 
     */
    

    public Boolean getValue() {
        return value;
    }

    public StatusDocument() {
        this.cpu = 0.0;
        this.memory = 0.0;
        this.disc = 0.0;
        this.totalup = 0.0;
        this.totaldown = 0.0;
        this.nowup = 0.0;
        this.nowdown = 0.0;
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
   
    public Double getCpu() {
        return cpu;
    }

    public void setCpu(Double cpu) {
        this.cpu = cpu;
    }

    public Double getMemory() {
        return memory;
    }

    public void setMemory(Double memory) {
        this.memory = memory;
    }

    public Double getDisc() {
        return disc;
    }

    public void setDisc(Double disc) {
        this.disc = disc;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getServerID() {
        return serverID;
    }

    public void setServerID(String serverID) {
        this.serverID = serverID;
    }

    public Double getTotalup() {
        return totalup;
    }

    public Double getTotaldown() {
        return totaldown;
    }

    public Double getNowup() {
        return nowup;
    }

    public Double getNowdown() {
        return nowdown;
    }
    

}
