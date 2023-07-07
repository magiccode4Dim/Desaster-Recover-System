package com.magiccode4dim.statusservice;
import org.springframework.data.jpa.repository.JpaRepository;


public interface StatusCRUD extends JpaRepository<Status, Integer> {
    
}
