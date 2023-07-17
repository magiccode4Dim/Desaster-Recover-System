package com.magiccode4dim.statusservice;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface ImageMongo extends MongoRepository<ImageDocument, Integer>{
    
}
