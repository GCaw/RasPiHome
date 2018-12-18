<?php

include('config.php');
include('utctime.php');

try {
    $con = new PDO($hostdb, $user, $pass);
    $result = $con->query("INSERT INTO user_requests (datetime, request_type, parameters, completed, requested_user) VALUES ('" . $utcnow . "','" . $_GET['req'] . "','" . $_GET['args'] . "','0','" . $_SERVER['REMOTE_ADDR']. "');");
} 
catch(PDOException $ex) {
    echo "An Error occured!";
    die();
}

$con = null;

?>