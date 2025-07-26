<!DOCTYPE html>
<html>
<head>
    <title>Character Manager</title>
    <meta charset="utf-8" />
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="style.css">
</head>
<body class="bg-gray-900 text-gray-100 font-sans min-h-screen p-6">
<header class="mb-4 text-center">
  <img src="#######" alt="Header placeholder" class="header-img">
    <nav class="mt-2">
    <ul class="flex space-x-4 justify-center">
  <li><a class="text-blue-400 hover:text-white" href="index.php">Home</a></li>
  <?php if(isset($_SESSION['account_id'])) { ?>
      <li><a class="text-blue-400 hover:text-white" href="characters.php">My Characters</a></li>
      <li><a class="text-blue-400 hover:text-white" href="create_character.php">Create Character</a></li>
      <li><a class="text-blue-400 hover:text-white" href="change_password.php">Change Password</a></li>
      <li><a class="text-blue-400 hover:text-white" href="logout.php">Logout</a></li>
      <?php if(isset($_SESSION['is_admin']) && $_SESSION['is_admin']) { ?>
          <li><a class="text-blue-400 hover:text-white" href="admin.php">Admin Panel</a></li>
      <?php } ?>
  <?php } else { ?>
      <li><a class="text-blue-400 hover:text-white" href="login.php">Login</a></li>
      <li><a class="text-blue-400 hover:text-white" href="register.php">Register</a></li>
  <?php } ?>
    </ul>
    </nav>
  </header>
  <main class="main-container mx-auto">
