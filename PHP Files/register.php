<?php include 'checkSession.php';?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Register</title>

    <!-- Bootstrap core CSS -->
    <link href="https://v4-alpha.getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="register.css" rel="stylesheet">
  </head>

  <body>

<?php
  include 'db.php';
  include 'helper.php';

  if (isset($_POST["username"]) && 
      isset($_POST["password"]) && 
      isset($_POST["email"])    &&
      isset($_POST["code"]))
  {
    $username = $con->real_escape_string($_POST["username"]);
    $password = $con->real_escape_string($_POST["password"]);
    $email = $con->real_escape_string($_POST["email"]);
    $code = $con->real_escape_string($_POST["code"]);

    if (!verifyInput($username, $password, $email, $code) ||
        !userExist($con, $username, $email))
    {
      $con->close();
    }
    else
    {
      $password = sha1($password);

      $q = "INSERT INTO users(username, password, email, friends, code, ip) VALUES('$username', '$password', '$email', '', '$code', '');";
      if (!$con->query($q))
      {
        echo "<div class='container' align = 'middle'>";
        echo "<h2 class='form-register-heading'>Registration failed !<br>Try again later !<br></h2>";
        echo "</div>";
      }
      else
      {
        header("Location: ./");
      }
      $con->close();
    }
    
  }
?>

    <div class="container" align = "middle">

      <form class="form-register" action = "./register.php" method = "POST">
        <h2 class="form-register-heading">Please register</h2>

        <label for="username" class="sr-only">Username</label>
        <input type="text" name="username" id="username" class="form-control" placeholder="Username" required autofocus>
        
        <label for="password" class="sr-only">Password</label>
        <input type="password" name="password" id="password" class="form-control" placeholder="Password" required>
        
        <label for="email" class="sr-only">Email</label>
        <input type="email" name="email" id="email" class="form-control" placeholder="Email" required>
        
        <label for="code" class="sr-only">Secret Code</label>
        <input type="password" name="code" id="code" class="form-control" placeholder="Secret Code" maxlength="4" required>

        <button class="btn btn-lg btn-primary btn-block" type="submit">Register</button>
      </form>

    </div>

    <script src="https://v4-alpha.getbootstrap.com/assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
