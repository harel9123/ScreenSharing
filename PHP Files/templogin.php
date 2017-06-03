<?php include 'checkSession.php';?>

<!DOCTYPE html>
<html>
<head>
<title>Login</title>
</head>
<body align = "middle">

<?php
	include 'db.php';

	if (isset($_POST["username"]) && 
		isset($_POST["password"]))
	{
		$username = $con->real_escape_string($_POST["username"]);
		$password = sha1($con->real_escape_string($_POST["password"]));

		$q = "SELECT id, friends FROM users WHERE username = '$username' and password = '$password';";

		$res = $con->query($q);
		if (!$res)
		{
			echo "<h3>Login failed !<br>Try again later !<br></h3>";
		}
		else
		{
			if (!$res->num_rows)
			{
				echo "<h3>Username/Password are incorrect !<br></h3>";
			}
			else
			{
				$res->data_seek(0);
				$row = $res->fetch_assoc();
				$friends = $row["friends"];

				$_SESSION["username"] = $username;
				$_SESSION["friends"] = $friends;

				$q = "UPDATE users SET status = 1 WHERE username = '$username';";

				$res = $con->query($q);
				if (!$res)
				{
					echo "<h3>Login failed !<br>Try again later !<br></h3>";
					header("Location: ./logout.php");
					exit();
				}
				header("Location: ./panel.php");
			}
		}
	}
	$con->close();
?>

<h2>Login</h2>

<form action = "./login.php" method = "POST">
	Username:
	<input type = "text" name = "username" spaceholder = "Username"/><br>
	Password:
	<input type = "password" name = "password" spaceholder = "Password"/><br>
	<br>
	<input type = "submit" value = "Login">
</form>

</body>
</html>