/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.magiccode4dim.imageservice;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
/**
 *
 * @author narci
 */
@RestController
public class ImageService {
    EntityManagerFactory emf = Persistence.createEntityManagerFactory("IMAGESERVICE_PU");
    @GetMapping("/createnewimage")
    public String teste() {
        ImageJpaController i =  new ImageJpaController(emf);
        Image im = new Image();
        im.setId(1);
        im.setNome("Ubuntu");
        im.setVersion("20.04");
        im.setDescricao("Ubuntu server");
        try {
            i.create(im);
        } catch (Exception ex) {
            Logger.getLogger(ImageService.class.getName()).log(Level.SEVERE, null, ex);
        }
        return "TESTE";
    }
}
