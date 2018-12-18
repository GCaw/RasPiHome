<html>
<title>Room Temperature</title>
<head>

</head>

<body>

<?php

include('config.php');

try {
    $con = new PDO($hostdb, $user, $pass);
    $result = $con->query("SELECT * FROM environment ORDER BY uid DESC LIMIT 1");
}
catch(PDOException $ex) {
    echo "An Error occured!";
    die();
}

while($row = $result->fetch(PDO::FETCH_ASSOC))
{
    echo "The last entry was:";
    echo "</br>";
    echo "</br>";

    echo "inside: $row[temperature] deg C - outside: $row[outside_temp] deg C - pressure: $row[air_pressure] hPa";
    
    echo "</br>";
    echo "</br>";
    echo "at $row[datetime] UTC";
}

$con = null

?>

</body>
</html>