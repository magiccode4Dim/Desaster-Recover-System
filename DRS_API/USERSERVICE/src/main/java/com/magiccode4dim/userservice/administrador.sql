/*
mysql> desc administrador;
+--------------+---------------+------+-----+---------+----------------+
| Field        | Type          | Null | Key | Default | Extra          |
+--------------+---------------+------+-----+---------+----------------+
| id           | int           | NO   | PRI | NULL    | auto_increment |
| instituicao  | varchar(2000) | YES  |     | NULL    |                |
| foto         | varchar(2000) | YES  |     | NULL    |                |
| auth_user_id | int           | YES  | MUL | NULL    |                |
+--------------+---------------+------+-----+---------+----------------+
*/

create table administrador(id int primary key auto_increment,instituicao  varchar(2000),
foto varchar(2000), auth_user_id int, foreign key(auth_user_id)
references auth_user(id)
);