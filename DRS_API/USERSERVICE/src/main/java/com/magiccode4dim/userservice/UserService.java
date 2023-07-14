/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.magiccode4dim.userservice;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 *
 * @author narci
 */

@RestController
@RequestMapping("/drs/api/user")
public class UserService {

    private final AdministradorCRUD  aCrud;
    private final AuthUserCRUD  auCrud;


    @Autowired
    public UserService(AdministradorCRUD ac, AuthUserCRUD auc) {
        this.aCrud = ac;
        this.auCrud = auc;
    }

    @GetMapping("/test/{id_auth_user}")
    public String teste(@PathVariable Integer id_auth_user) {
        //verifica se usuario django existe
        AuthUser au =  this.auCrud.getOne(id_auth_user);
        if(au==null){
            return "Utilizador DJango nao existe";
        }

        //cria novo administrador
        Administrador a = new Administrador();
        a.setFoto("foto.png");
        a.setInstituicao("AAEE");
        a.setAuthUser(au);
        this.aCrud.save(a);


        return "Sucesso";
    }

}
