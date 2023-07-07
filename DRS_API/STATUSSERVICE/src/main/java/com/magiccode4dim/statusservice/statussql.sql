/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
/**
 * Author:  narciso
 * Created: Jul 5, 2023
 */

 /*
+---------------+--------------+------+-----+---------+----------------+
| Field         | Type         | Null | Key | Default | Extra          |
+---------------+--------------+------+-----+---------+----------------+
| id            | int          | NO   | PRI | NULL    | auto_increment |
| server_adress | varchar(700) | YES  |     | NULL    |                |
| data_criacao  | date         | YES  |     | NULL    |                |
| value         | int          | YES  |     | NULL    |                |
| id_service    | int          | YES  |     | NULL    |                |
+---------------+--------------+------+-----+---------+----------------+
 */


create table status(id int primary key auto_increment, server_adress varchar(700)
, data_criacao date,value int,id_service int);

desc status;