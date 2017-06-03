<?php
	$redir = False;
	include 'db.php';
	include 'checkSession.php';

	$name = $con->real_escape_string($_GET['name']);
	$q = "SELECT ip FROM users WHERE username = '$name';";
	$res = $con->query($q);

	echo $res->fetch_assoc()['ip'];

	$con->close();
?>