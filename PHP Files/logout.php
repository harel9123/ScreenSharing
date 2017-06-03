<?php
	$redir = False;
	include 'checkSession.php';
	include 'db.php';

	$username = $_SESSION['username'];
	$q = "UPDATE users SET status = 0 WHERE username = '$username';";

	$con->query($q);

	session_start();
	session_unset();
	session_destroy();

	header("Location: ./");
?>