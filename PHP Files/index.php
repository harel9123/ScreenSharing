<?php include 'checkSession.php';?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Signin</title>

    <!-- Bootstrap core CSS -->
    <link href="https://v4-alpha.getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="signin.css" rel="stylesheet">
  </head>

  <body>

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
      echo "<div class='container' align = 'middle'>";
      echo "<h2 class='form-signin-heading'>Login failed !<br>Try again later !<br></h2>";
      echo "</div>";
    }
    else
    {
      if (!$res->num_rows)
      {
        echo "<div class='container' align = 'middle'>";
        echo "<h2 class='form-signin-heading'>Username/Password are incorrect !<br></h2>";
        echo "</div>";
      }
      else
      {
        $res->data_seek(0);
        $row = $res->fetch_assoc();
        $friends = $row["friends"];

        $_SESSION["username"] = $username;
        $_SESSION["friends"] = $friends;

        $ip = $_SERVER['REMOTE_ADDR'];
        
        $q = "UPDATE users SET ip = '$ip', status = 1 WHERE username = '$username';";

        $res = $con->query($q);
        if (!$res)
        {
          echo "<div class='container' align = 'middle'>";
          echo "<h2 class='form-signin-heading'>Login failed !<br>Try again later !<br></h2>";
          echo "</div>";
          header("Location: ./logout.php");
          exit();
        }
        
        header("Location: ./panel.php");
      }
    }
  }
  $con->close();
?>

    <div class="container" align = "middle">

      <form class="form-signin" action = "./" method = "POST">
        <h2 class="form-signin-heading">Please sign in</h2>

        <label for="username" class="sr-only">Username</label>
        <input type="text" name="username" id="username" class="form-control" placeholder="Username" required autofocus>
        <label for="password" class="sr-only">Password</label>
        <input type="password" name="password" id="password" class="form-control" placeholder="Password" required>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
        <button class="btn btn-lg btn-primary btn-block" type="button" onclick = "javascript:window.location.href = './register.php';">Register</button>
      </form>

    </div>

    <script src="https://v4-alpha.getbootstrap.com/assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
