<?php
require_once 'config.php';
if (!isset($_SESSION['account_id']) || !$_SESSION['is_admin']) {
    header('Location: index.php');
    exit();
}
$playerId = intval($_POST['id'] ?? 0);
if ($playerId) {
    $stmt = $mysqli->prepare('INSERT INTO bans (ban_type, ban_by, ban_data, ban_reason, ban_expire) VALUES (1, ?, ?, ?, UNIX_TIMESTAMP()+86400)');
    $by = $_SESSION['account_id'];
    $reason = 'Banned from admin panel';
    $stmt->bind_param('iis', $by, $playerId, $reason);
    $stmt->execute();
}
header('Location: admin.php');
exit();
