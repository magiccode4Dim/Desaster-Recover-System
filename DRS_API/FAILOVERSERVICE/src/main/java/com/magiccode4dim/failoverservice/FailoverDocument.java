package com.magiccode4dim.failoverservice;

import org.springframework.data.mongodb.core.mapping.Document;
import java.util.Date;
import java.util.List;

import org.springframework.data.annotation.Id;

@Document(collection = "failover")
public class FailoverDocument{
	@Id
    private String id;
    private String nome;
    private String serverID;
	private List<Object> services;

    

	public FailoverDocument() {
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public List<Object> getServices() {
        return services;
    }

    public void setServices(List<Object> services) {
        this.services = services;
    }

    public String getServerID() {
        return serverID;
    }

    public void setServerID(String serverID) {
        this.serverID = serverID;
    }
    
    
    

}