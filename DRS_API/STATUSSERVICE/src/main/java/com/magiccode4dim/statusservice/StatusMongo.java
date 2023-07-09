package com.magiccode4dim.statusservice;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface StatusMongo extends MongoRepository<StatusDocument, Integer>{
    
}
