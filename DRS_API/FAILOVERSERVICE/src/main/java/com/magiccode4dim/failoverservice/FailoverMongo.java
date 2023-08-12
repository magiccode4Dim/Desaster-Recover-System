package com.magiccode4dim.failoverservice;


import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;


public interface FailoverMongo  extends MongoRepository<FailoverDocument, String> {
    
}
