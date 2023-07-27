package com.magiccode4dim.statusservice.util;


import java.security.SecureRandom;
import java.util.Base64;
import java.util.UUID;

public class RandomToken {

    public static String generateRandomToken(int length) {
        // array de bytes com o tamanho especificado
        byte[] randomBytes = new byte[length];

       // bytes com valores aleatórios
        SecureRandom secureRandom = new SecureRandom();
        secureRandom.nextBytes(randomBytes);

        // array de bytes para uma string no formato Base64
        String token = Base64.getUrlEncoder().withoutPadding().encodeToString(randomBytes);

        return token;
    }

     public static String generateRandomString() {
        // Crie um UUID aleatório
        UUID uuid = UUID.randomUUID();

        // Obtenha a representação do UUID como uma string (sem hífens)
        String randomString = uuid.toString().replaceAll("-", "");

       
        return randomString;
        
    }
}
