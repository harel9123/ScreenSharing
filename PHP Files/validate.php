<?php
	$redir = False;
	include 'db.php';
	include 'checkSession.php';

	$name = $con->real_escape_string($_GET['name']);
	$code = $con->real_escape_string($_GET['code']);

	$q = "SELECT code FROM users WHERE username = '$name';";
	$res = $con->query($q);
	$orgCode = $res->fetch_assoc()['code'];

	if ($code === $orgCode)
	{
		$q = "SELECT pending FROM users WHERE username = '$name';";
		$res = $con->query($q);
		if (!$res)
		{
			$con->close();
			exit();
		}
		$pList = $res->fetch_assoc()['pending'];

		if (strpos($pList, ','.$name.',') !== False)
		{
			$con->close();
			exit();
		}

		$pList .= $_SESSION['username'].',';

		$q = "UPDATE users SET pending = '".$pList."' WHERE username = '$name';";
		$res = $con->query($q);
		if (!$res)
		{
			$con->close();
			exit();
		}
		echo "true";
	}
	else
	{
		echo "false";
	}

	$con->close();
?>