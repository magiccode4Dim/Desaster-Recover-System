package com.magiccode4dim.statusservice;

import org.springframework.data.mongodb.core.mapping.Document;
import java.util.Date;
import org.springframework.data.annotation.Id;


@Document(collection = "images")
public class ImageDocument {
    @Id
    private Integer id;

    private String nome;

    private String tag;

    private Date data_criacao;

    private String downloadComand;

    private String descricao;

    private String foto;

    private String simple_exec_comand;

    private String hash;
/** Este ultimo atributo so 'e usado na hora de criar uma imagem apartir do cantainer */
    private String containerID;


    public String getHash() {
        return hash;
    }

    public void setHash(String hash) {
        this.hash = hash;
    }

    public String getSimple_exec_comand() {
        return simple_exec_comand;
    }

    public void setSimple_exec_comand(String simple_exec_comand) {
        this.simple_exec_comand = simple_exec_comand;
    }
    

    public String getContainerID() {
        return containerID;
    }

    public void setContainerID(String containerID) {
        this.containerID = containerID;
    }

    public String getFoto() {
        return foto;
    }

    public String getTag() {
        return tag;
    }

    public void setTag(String tag) {
        this.tag = tag;
    }

    public void setFoto(String foto) {
        this.foto = foto;
    }

    public String getDescricao() {
        return descricao;
    }

    public void setDescricao(String descricao) {
        this.descricao = descricao;
    }

    public String getDownloadComand() {
        return downloadComand;
    }

    public void setDownloadComand(String downloadComand) {
        this.downloadComand = downloadComand;
    }

    public Date getData_criacao() {
        return data_criacao;
    }

    public void setData_criacao(Date data_criacao) {
        this.data_criacao = data_criacao;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

}