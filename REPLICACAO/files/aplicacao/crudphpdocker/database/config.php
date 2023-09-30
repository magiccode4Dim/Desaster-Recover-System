<?php

/*$host = getenv("DB_HOST");
$port = getenv("DB_PORT");
$username = getenv("DB_USER");
$password = getenv("DB_PASS");
$dbname = getenv("NAME");*/
$connection_string = "host='192.168.122.71' port=6004 dbname='crudphp' user='narciso' password='2001'";

$conn = pg_connect($connection_string);

if (!$conn) {
    echo "<marquee>Not connected to db</marquee> \n";
}
