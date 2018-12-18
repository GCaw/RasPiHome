<?php
include('config.php');
include('utctime.php');

try {
    $con = new PDO($hostdb, $user, $pass);
    $result = $con->query("INSERT INTO environment (datetime, temperature, air_pressure, outside_temp) VALUES ('" . $utcnow . "','" . $_GET['temp'] . "','" . $_GET['air'] . "','" . $_GET['temp_out'] . "');");
}
catch(PDOException $ex) {
    echo "An Error occured!";
    die();
}

$con = null;
?>