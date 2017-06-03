<script>
	function httpGet(theUrl)
	{
	    var xmlHttp = new XMLHttpRequest();
	    xmlHttp.open("GET", theUrl, false);
	    xmlHttp.send(null);
	    return xmlHttp.responseText;
	}

	function clickEvent(name)
	{
		var code = document.getElementById(name).value;
		data = httpGet("http://127.0.0.1/validate.php?name=" + name + "&code=" + code);
		alert(data);
		if (data.includes("true") == true)
		{
			var x = document.getElementById(name + "2");
			x.hidden = false;
		}
	}

	function startView(name)
	{
		IP = httpGet("http://127.0.0.1/getIP.php?name=" + name);
		data = httpGet("http://127.0.0.1/checkLists.php?name=" + name + "&list=ready");

		if (data == "false")
		{
			alert(name + " Didn't allow you to watch his screen !");
		}
		else
		{
			if (IP != '')
			{
				httpGet("http://127.0.0.1/updateDB.php?name=" + name + "&mode=1");
				alert("Run viewScreen.py with the argument: " + IP);
			}
		}
	}

	function startShare(name)
	{
		IP = httpGet("http://127.0.0.1/getIP.php?name=" + name);
		data = httpGet("http://127.0.0.1/checkLists.php?name=" + name + "&list=pending");
		
		if (data == "false")
		{
			alert(name + " Didn't request watching your screen !");
		}
		else
		{
			if (IP != '')
			{
				httpGet("http://127.0.0.1/updateDB.php?name=" + name + "&mode=0");
				alert("Run screenShare.py with the argument: " + IP);
			}
		}
	}
</script>

<?php
	function friendsList($con, $username)
	{
		$pair = createList($con, $username);
		printList($pair[0], $pair[1]);
	}

	function createList($con, $username)
	{
		$q = "SELECT friends FROM users WHERE username = '$username';";
		$res = $con->query($q);

		$fList = $res->fetch_assoc()['friends'];
		$names = explode(',', $fList);
		$status = array();
		for ($i = 0; $i < count($names); $i++)
		{
			if (userAdded($con, $username, $names[$i]) === False)
			{
				array_push($status, "");
				continue;
			}

			$q = "SELECT status FROM users WHERE username = '".$names[$i]."';";
			$res = $con->query($q);
			if (!$res)
			{
				array_push($status, "");
				continue;
			}

			$tempStatus = $res->fetch_assoc()['status'];
			if ($tempStatus == 1)
			{
				array_push($status, "Online");
			}
			else
			{
				array_push($status, "Offline");
			}
		}

		$both = array($names, $status);
		return $both;
	}

	function printList($names, $status)
	{
		echo "<div class = 'container' align = 'center'>";
		echo "<table align = ''>";
		for ($i = 0; $i < count($names); $i++)
		{
			if ($status[$i] != 'middle')
			{
				echo "<tr>";
				echo "<td>".$names[$i]."</td>";
				if ($status[$i] === "Online")
				{
					$currName = $names[$i];
					echo "<td>
						  <input type = 'text' id = '".$currName."' maxlength = 4 placeholder = 'Secret code'>
						  <button onclick = 'clickEvent(\"".$currName."\")'>Request</button>
						  <div id = '".$currName."2' hidden = true>
						  Request Sent...
						  </div>
						  <button onclick = 'startView(\"".$currName."\")' id = '".$currName."3'>
						  View
						  </button>
						  <button onclick = 'startShare(\"".$currName."\")' id = '".$currName."4'>
						  Share
						  </button>
						  </td>";
				}
				else
				{
					echo "<td>".$status[$i]."</td>";
				}
				echo "</tr>";
			}
		}
		echo "</table>";
		echo "</div>";
	}

	function userAdded($con, $username, $friendName)
	{
		$q = "SELECT friends FROM users WHERE username = '$friendName';";
		$res = $con->query($q);
		if (!$res)
		{
			return False;
		}

		$fList = $res->fetch_assoc()['friends'];

		return strpos($fList, $username);
	}
?>