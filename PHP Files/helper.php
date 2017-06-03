<?php
	function checkLen($arg, $min, $max)
	{
		$len = strlen($arg);
		if ($len >= $min and $len <= $max)
		{
			return True;
		}
		return False;
	}

	function verifyInput($username, $password, $email, $code)
	{
		$isLegal = True;

		if (!checkLen($username, 5, 15) || 
			!preg_match('/[a-z0-9]*/i', $username))
		{
			echo "<div class='container' align = 'middle'>";
			echo "<h2 class='form-register-heading'>Illegal username !<br></h2>";
			echo "</div>";
			$isLegal = False;
		}
		if (!checkLen($password, 6, 100))
		{
			echo "<div class='container' align = 'middle'>";
			echo "<h2 class='form-register-heading'>Illegal password !<br></h2>";
			echo "</div>";
			$isLegal = False;
		}
		if (!checkLen($email, 6, 50) || 
			!preg_match('/[a-z0-9]*\@[a-z0-9]*\.[a-z0-9]]*/i', $email))
		{
			echo "<div class='container' align = 'middle'>";
			echo "<h2 class='form-register-heading'>Illegal email !<br></h2>";
			echo "</div>";
			$isLegal = False;
		}
		if (!checkLen($code, 4, 4) ||
			!preg_match('/[0-9]$/i', $code))
		{
			echo "<div class='container' align = 'middle'>";
			echo "<h2 class='form-register-heading'>Illegal code !<br></h2>";
			echo "</div>";
			$isLegal = False;
		}
		return $isLegal;
	}

	function userExist($con, $username, $email)
	{
		$res = $con->query("SELECT * FROM users WHERE email = '$email' or username = '$username';");
		if ($res === False)
		{
			echo "<h3>Registration failed !<br>Try again later !<br></h3>";
			return False;
		}
		else if ($res->num_rows)
		{
			echo "<h3>Email / Username already exists in the system !<br>Register using another email / username !<br></h3>";
			return False;
		}
		return True;
	}
?>