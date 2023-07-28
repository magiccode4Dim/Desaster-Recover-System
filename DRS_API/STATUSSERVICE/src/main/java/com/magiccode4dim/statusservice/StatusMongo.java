package com.magiccode4dim.statusservice;
import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface StatusMongo extends MongoRepository<StatusDocument, String>{
    List<StatusDocument> findByServerID(String id);
}
