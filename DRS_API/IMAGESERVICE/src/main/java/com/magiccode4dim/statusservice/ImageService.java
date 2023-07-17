/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.magiccode4dim.statusservice;

import java.io.IOException;
import java.util.Date;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.annotation.Secured;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

//Jython
import org.python.core.PyObject;
import org.python.util.PythonInterpreter;


//docker

/**
 *
 * @author narci
 */

@RestController
@RequestMapping("/drs/api/image")
public class ImageService {

    private final ImageMongo imageCRUD;

    // jython
    @Secured("USER")
    @GetMapping("/jython")
    public String jython() {
        // Criar uma instância do interpretador Python
        PythonInterpreter interpreter = new PythonInterpreter();

        // Executar uma linha de código Python
        interpreter.exec("print('Hello from Python')");

        // Chamar uma função Python e obter o resultado
        interpreter.exec("def add(a, b):\n    return a + b");
        PyObject result = interpreter.eval("add(2, 3)");
        System.out.println("Resultado: " + result);

        // Fechar o interpretador Python
        interpreter.close();
        
        return "jYTHON";
    }

    @Autowired
    public ImageService(ImageMongo ss) {
        this.imageCRUD = ss;
    }

    @Secured("USER")
    @PostMapping("/download")
    public String downloadImage(@RequestBody ImageDocument ido) {
        // fazer o download da imagem no docker hub e guarda no registry
        return "Salvo Com Sucesso";
    }

    // o adiministrador cria uma imagem
    @Secured("USER")
    @PostMapping("/create")
    public String create(@RequestBody ImageDocument ido) {
        // Salva um container em execucao em um determinado servidor como uma imagem e
        // guarda no registry
        // deve existir um servidor de execucao de containeris
        // Configurar as credenciais de autenticação básica

        // ido.setData_criacao(new Date());
        // this.imageCRUD.save(ido);
        return "Salvo Com Sucesso";
    }

    // apagar imagem
    @Secured("USER")
    @DeleteMapping("/delete/{id}")
    public String delete(@PathVariable Integer id) {
        this.imageCRUD.deleteById(id);
        return "Salvo Com Sucesso";
    }

    // pegar a imagem com id
    @Secured("USER")
    @GetMapping("/get/{id}")
    @ResponseBody
    public ImageDocument getImage(@PathVariable Integer id) {
        Object u = this.imageCRUD.findById(id).orElse(null);
        ;
        if (u == null) {
            return null;
        }
        return (ImageDocument) u;
    }

    // pegar todas imagens
    @Secured("USER")
    @GetMapping("/getall")
    @ResponseBody
    public List<ImageDocument> geAllStatus() {
        return this.imageCRUD.findAll();
    }

    // como usar recursos avancados do mongodb

}
