package com.magiccode4dim.managerservice;

import org.springframework.data.mongodb.core.mapping.Document;
import java.util.Date;
import org.springframework.data.annotation.Id;

@Document(collection = "service")
public class ServiceDocument{
	@Id
    private String id;
	private Object service;

	public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }
    public Object getService() {
        return service;
    }

    public void setService(Object service) {
        this.service = service;
    }


}