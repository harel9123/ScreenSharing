<?php
	$redir = False;
	include 'db.php';
	include 'checkSession.php';

	$username = $_SESSION['username'];

	$q = "SELECT ready FROM users WHERE username = '$username';";
	$res = $con->query($q);
	if (!$res)
	{
		$con->close();
		exit();
	}
	$rList = $res->fetch_assoc()['ready'];

	$q = "SELECT pending FROM users WHERE username = '$username';";
	$res = $con->query($q);
	if (!$res)
	{
		$con->close();
		exit();
	}
	$pList = $res->fetch_assoc()['pending'];
	echo $rList.' '.$pList;
?>