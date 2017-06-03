<?php
	session_start();
	if (isset($_SESSION["username"]) && !isset($redir))
	{
		header("Location: ./panel.php");
		exit();
	}
?>