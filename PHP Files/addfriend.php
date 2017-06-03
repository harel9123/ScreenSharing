<?php 
	$redir = False;
	include 'checkSession.php';
	include 'helper.php';
	include 'db.php';

	if (!isset($_POST['username']))
	{
		header("Location: ./panel.php");
		exit();
	}

	$toAdd = $con->real_escape_string($_POST['username']);
	$currUname = $_SESSION['username'];

	if (!checkLen($toAdd, 5, 15) || 
		!preg_match('/[a-z0-9]*/i', $toAdd))
	{
		echo "<script>alert('Illegal username !')</script>";
		$con->close();
		echo "<script>window.location.href = './panel.php'</script>";
		exit();
	}

	$q = "SELECT friends FROM users WHERE username = '$currUname';";
	$res = $con->query($q);

	$fList = $res->fetch_assoc()['friends'];
	$count = substr_count($fList, ',');

	if ($count == 60)
	{
		echo "<script>alert('Your friends list is full !')</script>";
		$con->close();
		echo "<script>window.location.href = './panel.php'</script>";
		exit();
	}

	if (strpos($fList, ','.$toAdd.',') !== False)
	{
		echo "<script>alert('Friend already exist !')</script>";
		$con->close();
		echo "<script>window.location.href = './panel.php'</script>";
		exit();
	}

	$fList .= $toAdd . ',';
	$q = "UPDATE users SET friends = '$fList' WHERE username = '$currUname';";
	$con->query($q);

	$con->close();

	header('Location: ./panel.php');
	exit();
?>