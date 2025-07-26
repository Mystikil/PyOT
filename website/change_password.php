<?php
require_once 'config.php';
if (!isset($_SESSION['account_id'])) {
    header('Location: index.php');
    exit();
}

$error = '';
$success = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $current = $_POST['current'] ?? '';
    $newpass = $_POST['new'] ?? '';
    $confirm = $_POST['confirm'] ?? '';

    if (!$current || !$newpass || !$confirm) {
        $error = 'All fields are required.';
    } elseif ($newpass !== $confirm) {
        $error = 'New passwords do not match.';
    } else {
        $stmt = $mysqli->prepare('SELECT password, salt FROM accounts WHERE id=?');
        $stmt->bind_param('i', $_SESSION['account_id']);
        $stmt->execute();
        $res = $stmt->get_result();
        if ($row = $res->fetch_assoc()) {
            $hash = sha1($row['salt'] . $current);
            if ($hash !== $row['password']) {
                $error = 'Current password incorrect.';
            } else {
                $newHash = sha1($row['salt'] . $newpass);
                $upd = $mysqli->prepare('UPDATE accounts SET password=? WHERE id=?');
                $upd->bind_param('si', $newHash, $_SESSION['account_id']);
                if ($upd->execute()) {
                    $success = 'Password changed successfully.';
                } else {
                    $error = 'Failed to update password.';
                }
            }
        } else {
            $error = 'Account not found.';
        }
    }
}
?>
<?php include 'header.php'; ?>
<h2 class="text-xl font-semibold mb-4">Change Password</h2>
<?php if($error) { echo '<p class="text-red-500">'.htmlspecialchars($error).'</p>'; } ?>
<?php if($success) { echo '<p class="text-green-400">'.htmlspecialchars($success).'</p>'; } ?>
<form class="space-y-4" method="post">
    <label class="block">Current Password: <input class="text-gray-800 p-1 rounded" type="password" name="current" /></label>
    <label class="block">New Password: <input class="text-gray-800 p-1 rounded" type="password" name="new" /></label>
    <label class="block">Confirm New Password: <input class="text-gray-800 p-1 rounded" type="password" name="confirm" /></label>
    <input class="bg-blue-600 hover:bg-blue-700 text-white py-1 px-3 rounded" type="submit" value="Change Password" />

</form>
<?php include 'footer.php'; ?>
