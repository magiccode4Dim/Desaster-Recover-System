package com.magiccode4dim.managerservice.requests.Objects;

public class Network {
    private String nome;
    private String rede;
    private String gateway;


    
    public Network() {
    }
    public String getNome() {
        return nome;
    }
    public void setNome(String nome) {
        this.nome = nome;
    }
    public String getRede() {
        return rede;
    }
    public void setRede(String rede) {
        this.rede = rede;
    }
    public String getGateway() {
        return gateway;
    }
    public void setGateway(String gateway) {
        this.gateway = gateway;
    }

    
}
