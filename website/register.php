<?php
require_once 'config.php';
if (isset($_SESSION['account_id'])) {
    header('Location: characters.php');
    exit();
}
$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username'] ?? '');
    $password = $_POST['password'] ?? '';
    $confirm  = $_POST['confirm'] ?? '';
    if (!$username || !$password || !$confirm) {
        $error = 'All fields are required.';
    } elseif ($password !== $confirm) {
        $error = 'Passwords do not match.';
    } else {
        $check = $mysqli->prepare('SELECT id FROM accounts WHERE name=?');
        $check->bind_param('s', $username);
        $check->execute();
        $check->store_result();
        if ($check->num_rows > 0) {
            $error = 'Username already exists.';
        } else {
            $salt = bin2hex(random_bytes(5));
            $hash = sha1($salt . $password);
            $ins = $mysqli->prepare('INSERT INTO accounts (name, password, salt, group_id) VALUES (?, ?, ?, 1)');
            $ins->bind_param('sss', $username, $hash, $salt);
            if ($ins->execute()) {
                $_SESSION['account_id'] = $ins->insert_id;
                $_SESSION['is_admin'] = false;
                header('Location: characters.php');
                exit();
            } else {
                $error = 'Failed to register.';
            }
        }
    }
}
include 'header.php';
?>
<h2 class="text-xl font-semibold mb-4">Register</h2>
<?php if($error) echo '<p class="text-red-500">'.htmlspecialchars($error).'</p>'; ?>
<form class="space-y-4" method="post">
    <label class="block">Username: <input class="text-gray-800 p-1 rounded" type="text" name="username" /></label>
    <label class="block">Password: <input class="text-gray-800 p-1 rounded" type="password" name="password" /></label>
    <label class="block">Confirm Password: <input class="text-gray-800 p-1 rounded" type="password" name="confirm" /></label>
    <input class="bg-blue-600 hover:bg-blue-700 text-white py-1 px-3 rounded" type="submit" value="Register" />

</form>
<?php include 'footer.php'; ?>
