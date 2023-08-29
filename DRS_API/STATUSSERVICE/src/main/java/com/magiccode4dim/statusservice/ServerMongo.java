package com.magiccode4dim.statusservice;


import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface ServerMongo extends MongoRepository<ServerDocument, String>{
     List<ServerDocument> findByToken(String token);
     List<ServerDocument> findByNome(String nome);
    
}
