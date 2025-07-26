<?php
require_once 'config.php';

if (isset($_SESSION['account_id'])) {
    header('Location: characters.php');
    exit();
}

$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    if ($username && $password) {
        $stmt = $mysqli->prepare('SELECT id, group_id, salt, password FROM accounts WHERE name=?');
        $stmt->bind_param('s', $username);
        $stmt->execute();
        $result = $stmt->get_result();
        if ($row = $result->fetch_assoc()) {
            $hash = sha1($row['salt'] . $password);
            if ($hash === $row['password']) {
                $_SESSION['account_id'] = $row['id'];
                $_SESSION['is_admin'] = ($row['group_id'] >= ADMIN_GROUP_ID);
                header('Location: characters.php');
                exit();
            }
        }
        $error = 'Invalid login.';
    } else {
        $error = 'Enter username and password';
    }
}
?>
<?php include 'header.php'; ?>
<h2 class="text-xl font-bold mb-2">Login</h2>
<?php if($error) { echo '<p class="error">'.htmlspecialchars($error).'</p>'; } ?>
<form method="post" class="space-y-2">
    <label class="block">Username: <input type="text" name="username" class="border p-1" /></label>
    <label class="block">Password: <input type="password" name="password" class="border p-1" /></label>
    <input type="submit" value="Login" class="bg-blue-500 text-white px-4 py-2 rounded" />
</form>
<?php include 'footer.php'; ?>
