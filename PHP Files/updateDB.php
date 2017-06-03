<?php
	$redir = False;
	include 'db.php';
	include 'checkSession.php';

	$username = $_SESSION['username'];
	$name = $con->real_escape_string($_GET['name']);
	$mode = $con->real_escape_string($_GET['mode']);

	if ($mode === "0")
	{
		$q = "SELECT pending FROM users WHERE username = '$username';";
		$res = $con->query($q);

		$pList = $res->fetch_assoc()['pending'];
		$pList = str_replace($name.',', '', $pList);

		$q = "UPDATE users SET pending = '".$pList."' WHERE username = '$username';";
		$res = $con->query($q);
		if (!$res)
		{
			$con->close();
			exit();
		}

		$q = "SELECT ready FROM users WHERE username = '$name';";
		$res = $con->query($q);

		$rList = $res->fetch_assoc()['ready'];
		$rList .= $username.',';

		$q = "UPDATE users SET ready = '".$rList."' WHERE username = '$name';";
		$res = $con->query($q);
		if (!$res)
		{
			$con->close();
			exit();
		}
	}
	else if ($mode === "1")
	{
		$q = "SELECT ready FROM users WHERE username = '$username';";
		$res = $con->query($q);

		$rList = $res->fetch_assoc()['ready'];
		$rList = str_replace($name.',', '', $rList);

		$q = "UPDATE users SET ready = '".$rList."' WHERE username = '$username';";
		$res = $con->query($q);
		if (!$res)
		{
			$con->close();
			exit();
		}
	}

	$con->close();
?>