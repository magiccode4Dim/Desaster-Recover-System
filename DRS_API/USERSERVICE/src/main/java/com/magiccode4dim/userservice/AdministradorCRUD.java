package com.magiccode4dim.userservice;
import org.springframework.data.jpa.repository.JpaRepository;


public interface AdministradorCRUD extends JpaRepository<Administrador, Integer> {
    
}
