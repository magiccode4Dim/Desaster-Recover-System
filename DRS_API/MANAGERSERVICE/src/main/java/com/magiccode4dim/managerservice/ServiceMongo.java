package com.magiccode4dim.managerservice;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface ServiceMongo extends MongoRepository<ServiceDocument, String>{
    
}
