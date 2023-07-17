/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.magiccode4dim.userservice;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.annotation.Secured;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

/**
 *
 * @author narci
 */

@RestController
@RequestMapping("/drs/api/user")
public class UserService {

    private final AdministradorCRUD  AdminCrud;
    private final AuthUserCRUD  AuthCrud;


    @Autowired
    public UserService(AdministradorCRUD ac, AuthUserCRUD auc) {
        this.AdminCrud= ac;
        this.AuthCrud = auc;
    }

    //create new user
    @Secured("USER")
    @PostMapping("/create")
    public String create(@RequestBody Administrador newAdministrador) {
        //verifica se usuario django existe 
        //PARA ESSE CASO VAI SE USAR O ID DO ADMINISTRADOR PARA APASSAR O ID DO AUTH DE MODO A FACILITAR
        if( !this.AuthCrud.existsById(newAdministrador.getId())){
            return "Utilizador DJango nao existe";
        }
        newAdministrador.setAuthUser(this.AuthCrud.getOne(newAdministrador.getId()));
        //cria novo administrador
        this.AdminCrud.save(newAdministrador);
        return "Sucesso";
    }

    //update user
    @Secured("USER")
    @PutMapping("/update")
    public String update(@RequestBody Administrador newAdministrador){
        //PARA ESSE CASO O ID VAI SER DO ADMINISTRADOR MESMO
        if( !this.AdminCrud.existsById(newAdministrador.getId())){
            return "Utilizador Administrador nao existe";
        }
        Administrador a =  AdminCrud.getOne(newAdministrador.getId());
        //se a foto ou o nome da instituicao forem diferentes, troca
        if(!a.getFoto().equals(newAdministrador.getFoto()) && newAdministrador.getFoto()!=null){
            a.setFoto(newAdministrador.getFoto());
        }
        if(!a.getInstituicao().equals(newAdministrador.getInstituicao()) && newAdministrador.getInstituicao()!=null){
            a.setInstituicao(newAdministrador.getInstituicao());
        }
        AdminCrud.save(a);
        return "Sucesso";
    }
    //delete administrador
    @Secured("USER")
    @DeleteMapping("/delete/{id}")
    public String delete(@PathVariable Integer id){
        if( !this.AdminCrud.existsById(id)){
            return "Utilizador Administrador nao existe";
        }
        this.AdminCrud.deleteById(id);
        return "Apagado com Sucesso";
    }
    //get administrador
    @Secured("USER")
    @GetMapping("/get/{id}")
    @ResponseBody
    public Administrador getAdministrador(@PathVariable Integer id){
        Object u = this.AdminCrud.findById(id).orElse(null);;
        if (u == null) {
            return null;
        }
        return (Administrador)u;
    }
    //get all administrador
    @Secured("USER")
    @GetMapping("/getall")
    @ResponseBody
    public List<Administrador> getAllAdmin(){
        return this.AdminCrud.findAll();
    }


}
