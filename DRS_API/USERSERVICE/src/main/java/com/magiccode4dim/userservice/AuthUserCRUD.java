package com.magiccode4dim.userservice;
import org.springframework.data.jpa.repository.JpaRepository;


public interface AuthUserCRUD extends JpaRepository<AuthUser, Integer> {
    
}
