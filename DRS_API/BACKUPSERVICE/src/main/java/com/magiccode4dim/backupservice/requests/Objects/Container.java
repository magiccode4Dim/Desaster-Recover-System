package com.magiccode4dim.backupservice.requests.Objects;

public class Container {
    private String name;
    private String Hostname;
    private String username;
    private String password;
    private String volume;


    public Container() {
      
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
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
    public String getVolume() {
        return volume;
    }
    public void setVolume(String volume) {
        this.volume = volume;
    }

    



    
    
}
