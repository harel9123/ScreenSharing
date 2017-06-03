<?php 
  $redir = False;
  include 'checkSession.php';
  $username = $_SESSION['username'];

  if (!isset($_SESSION['username']))
  {
    header('Location: ./');
    exit();
  }
?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>User Panel</title>

    <!-- Bootstrap core CSS -->
    <link href="https://v4-alpha.getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="panel.css" rel="stylesheet">
  </head>

  <body style = "max-width: 100%;">
    <div class = "form-addfriend">
      <button class="btn btn-lg btn-primary btn-block" type="button" onclick = "javascript:window.location.href = './logout.php';">Logout</button>
    </div>

    <table >
      <tr align = "center"> 
        <td>
          <h2 class="form-addfriend-heading">Add friend</h2>
        </td>

        <td>
          <h2>Friends List</h2>
        </td>
      </tr>

      <tr align = "center">
        <td>
          <div class="container" style="display: inline-block" align = "middle">
            <form class="form-addfriend" action = "./addfriend.php" method = "POST">
              <label for="username" class="sr-only">Username</label>
              <input type="text" name="username" id="username" class="form-control" placeholder="Username" required autofocus>
              <button class="btn btn-lg btn-primary btn-block" type="submit">Add</button>
            </form>
          </div>
        </td>

        <td>
          <div class="container">
            <?php
              include 'db.php';
              include 'createlist.php';
              friendsList($con, $username);
            ?>
          </div>
        </td>
      </tr>
    </table>

    <script src="https://v4-alpha.getbootstrap.com/assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>

