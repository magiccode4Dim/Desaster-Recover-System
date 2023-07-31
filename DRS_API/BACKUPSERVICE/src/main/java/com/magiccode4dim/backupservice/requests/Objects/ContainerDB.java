package com.magiccode4dim.backupservice.requests.Objects;

public class ContainerDB extends Container {
    private String dir;
    private String dbimage;

    public ContainerDB() {
        super();
    }
    public String getDir() {
        return dir;
    }
    public void setDir(String dir) {
        this.dir = dir;
    }
    public String getDbimage() {
        return dbimage;
    }
    public void setDbimage(String dbimage) {
        this.dbimage = dbimage;
    }

    
    
}
