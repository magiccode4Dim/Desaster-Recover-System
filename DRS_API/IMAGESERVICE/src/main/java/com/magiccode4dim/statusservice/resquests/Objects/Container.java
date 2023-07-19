package com.magiccode4dim.statusservice.resquests.Objects;

public class Container {
    private String name;
    private String Image;
    private String Hostname;
    private String username;
    private String password;
    private String createuser;


    public Container() {
      
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public String getImage() {
        return Image;
    }
    public void setImage(String image) {
        Image = image;
    }
    public String getHostname() {
        return Hostname;
    }
    public void setHostname(String hostname) {
        Hostname = hostname;
    }
    public String getUsername() {
        return username;
    }
    public void setUsername(String username) {
        this.username = username;
    }
    public String getPassword() {
        return password;
    }
    public void setPassword(String password) {
        this.password = password;
    }

    public void createsuperUser(){
        //"useradd -m -s /bin/bash narciso && echo 'narciso:2001' | chpasswd && usermod -aG sudo narciso && /usr/sbin/sshd -D"
        this.createuser =   this.createuser = "useradd -m -s /bin/bash "+this.username+" && echo '"+this.username+":"+this.password+"' | chpasswd && usermod -aG sudo "+this.username+" && /usr/sbin/sshd -D";
    }
    public void setCreateuser(String createuser) {
        this.createuser = createuser;
    }
    public String getCreateuser() {
        return createuser;
    }




    
    
}
