package com.magiccode4dim.statusservice.resquests.Objects;

public class Image {
    /**
    image = {
        'fromImage':  'alpine',
        'tag':'latest'
    }
     */
    private String fromImage;
    private String tag;
    


    public Image(String fromImage, String tag) {
        this.fromImage = fromImage;
        this.tag = tag;
    }
    public String getFromImage() {
        return fromImage;
    }
    public void setFromImage(String fromImage) {
        this.fromImage = fromImage;
    }
    public String getTag() {
        return tag;
    }
    public void setTag(String tag) {
        this.tag = tag;
    }
    

    
}
