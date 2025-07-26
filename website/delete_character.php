<?php
require_once 'config.php';
if (!isset($_SESSION['account_id'])) {
    header('Location: index.php');
    exit();
}
$playerId = intval($_POST['id'] ?? 0);
if ($playerId) {
    if ($_SESSION['is_admin']) {
        $stmt = $mysqli->prepare('DELETE FROM players WHERE id=?');
        $stmt->bind_param('i', $playerId);
        $stmt->execute();
    } else {
        $stmt = $mysqli->prepare('DELETE FROM players WHERE id=? AND account_id=?');
        $stmt->bind_param('ii', $playerId, $_SESSION['account_id']);
        $stmt->execute();
    }
}
header('Location: '.($_SESSION['is_admin'] ? 'admin.php' : 'characters.php'));
exit();
