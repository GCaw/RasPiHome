<html>
<title>Room Temperature</title>

<head>

<!--
https://www.chartjs.org/docs/latest/
http://www.pchart.net/features-charting
http://wiki.pchart.net/doc.scatter.drawscatterplotChart.html

https://phptherightway.com/#pdo_extension
https://secure.php.net/manual/en/pdo.connections.php
https://phpdelusions.net/pdo
-->

</head>

<body>

<table width="600"  border="0" cellpadding="0" cellspacing="5" style="margin: 0px auto;">
<tr>
<td align=center> "uid" </td>
<td align=center> "time (UTC)" </td>
<td align=center> "temp (C)" </td>
<td align=center> "out temp (C)" </td>
<td align=center> "air press (hPa)" </td>
</tr>

<?php
include('config.php');
try {
    $con = new PDO($hostdb, $user, $pass);
    $result = $con->query("SELECT * FROM environment");
}
catch(PDOException $ex) {
    echo "An Error occured!";
    die();
}
  
while($row = $result->fetch(PDO::FETCH_ASSOC))
{
    echo "<tr>";
    echo "<td align=center> $row[uid]</td>";
    echo "<td align=center> $row[datetime]</td>";
    echo "<td align=right>$row[temperature]</td>";
    echo "<td align=right>$row[outside_temp]</td>";
    echo "<td align=right>$row[air_pressure]</td>";
    echo "</tr>";
}
 
echo "</table>";

$con = null

?>
</body>
</html>