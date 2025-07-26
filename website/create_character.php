<?php
require_once 'config.php';
if (!isset($_SESSION['account_id'])) {
    header('Location: index.php');
    exit();
}
$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');
    $sex = intval($_POST['sex'] ?? 0);
    if ($name) {
        $stmt = $mysqli->prepare('INSERT INTO players (name, account_id, sex, world_id) VALUES (?, ?, ?, 0)');
        $stmt->bind_param('sii', $name, $_SESSION['account_id'], $sex);
        if ($stmt->execute()) {
            header('Location: characters.php');
            exit();
        } else {
            $error = 'Failed to create character.';
        }
    } else {
        $error = 'Name is required.';
    }
}
?>
<?php include 'header.php'; ?>
<h2 class="text-xl font-semibold mb-4">Create Character</h2>
<?php if($error) echo '<p class="text-red-500">'.htmlspecialchars($error).'</p>'; ?>
<form class="space-y-4" method="post">
    <label class="block">Name: <input class="text-gray-800 p-1 rounded" type="text" name="name" /></label>
    <label class="block">Sex:
        <select class="text-gray-800 p-1 rounded" name="sex">
            <option value="0">Male</option>
            <option value="1">Female</option>
        </select>
    </label>
    <input class="bg-blue-600 hover:bg-blue-700 text-white py-1 px-3 rounded" type="submit" value="Create" />
</form>

<?php include 'footer.php'; ?>
