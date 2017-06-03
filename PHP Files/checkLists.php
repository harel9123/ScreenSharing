<?php
	$redir = False;
	include 'db.php';
	include 'checkSession.php';

	$username = $_SESSION['username'];
	$name = $con->real_escape_string($_GET['name']);
	$list = $con->real_escape_string($_GET['list']);

	$q = "SELECT $list FROM users WHERE username = '$username';";
	$res = $con->query($q);
	$l = $res->fetch_assoc()[$list];

	if (strpos($l, $name) === False)
	{
		echo "false";
	}
	else
	{
		echo "true";
	}

	$con->close();
?>