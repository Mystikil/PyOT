<?php
require_once 'config.php';
if (!isset($_SESSION['account_id']) || !$_SESSION['is_admin']) {
    header('Location: index.php');
    exit();
}

$section = $_GET['section'] ?? 'home';
$table = $_GET['table'] ?? '';
$action = $_POST['action'] ?? '';
$message = '';

function get_columns($mysqli, $table) {
    $cols = [];
    if($res = $mysqli->query("SHOW COLUMNS FROM `$table`")) {
        while($row = $res->fetch_assoc()) {
            $cols[] = $row['Field'];
        }
    }
    return $cols;
}

// Process actions for various sections
if ($section === 'ban' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $playerId = intval($_POST['player_id'] ?? 0);
    if ($playerId) {
        $stmt = $mysqli->prepare('INSERT INTO bans (ban_type, ban_by, ban_data, ban_reason, ban_expire) VALUES (1, ?, ?, ?, UNIX_TIMESTAMP()+86400)');
        $by = $_SESSION['account_id'];
        $reason = 'Banned via admin panel';
        $stmt->bind_param('iis', $by, $playerId, $reason);
        $stmt->execute();
        $message = 'Player banned.';
    } else {
        $message = 'Invalid player id.';
    }
}

if ($section === 'status' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username'] ?? '');
    $accountId = intval($_POST['account_id'] ?? 0);
    $groupId = intval($_POST['group_id'] ?? 1);
    $blocked = isset($_POST['blocked']) ? 1 : 0;

    if ($username) {
        $stmt = $mysqli->prepare('SELECT id FROM accounts WHERE name=?');
        $stmt->bind_param('s', $username);
        $stmt->execute();
        $res = $stmt->get_result();
        if ($row = $res->fetch_assoc()) {
            $accountId = intval($row['id']);
        }
    }

    if ($accountId) {
        $stmt = $mysqli->prepare('UPDATE accounts SET group_id=?, blocked=? WHERE id=?');
        $stmt->bind_param('iii', $groupId, $blocked, $accountId);
        $stmt->execute();
        $message = 'Account updated.';
    } else {
        $message = 'Account not found.';
    }
}

if ($section === 'items' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['add_item'])) {
        $id = intval($_POST['id'] ?? 0);
        $type = intval($_POST['type'] ?? 0);
        $name = trim($_POST['name'] ?? '');
        if ($id && $name) {
            $stmt = $mysqli->prepare('INSERT INTO items (id, type, name) VALUES (?, ?, ?)');
            $stmt->bind_param('iis', $id, $type, $name);
            $stmt->execute();
            $message = 'Item added.';
        } else {
            $message = 'Missing item fields.';
        }
    } elseif (isset($_POST['remove_item'])) {
        $id = intval($_POST['id'] ?? 0);
        if ($id) {
            $stmt = $mysqli->prepare('DELETE FROM items WHERE id=?');
            $stmt->bind_param('i', $id);
            $stmt->execute();
            $message = 'Item removed.';
        } else {
            $message = 'Invalid item id.';
        }
    }
}

if ($section === 'itemlookup' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $serial = trim($_POST['serial'] ?? '');
    if (isset($_POST['duplicate']) && $serial) {
        $stmt = $mysqli->prepare('SELECT data FROM items WHERE serial=?');
        $stmt->bind_param('s', $serial);
        $stmt->execute();
        $res = $stmt->get_result();
        if ($row = $res->fetch_assoc()) {
            $data = $row['data'];
            $newserial = bin2hex(random_bytes(16));
            $ins = $mysqli->prepare('INSERT INTO items(serial,data) VALUES(?,?)');
            $ins->bind_param('ss', $newserial, $data);
            $ins->execute();
            $message = 'Duplicated as ' . htmlspecialchars($newserial);
        } else {
            $message = 'Item not found.';
        }
    } elseif ($serial) {
        $stmt = $mysqli->prepare('SELECT data FROM items WHERE serial=?');
        $stmt->bind_param('s', $serial);
        $stmt->execute();
        $res = $stmt->get_result();
        if ($row = $res->fetch_assoc()) {
            $itemdata = base64_encode($row['data']);
        } else {
            $message = 'Item not found.';
        }
    }
}

if ($section === 'password' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username'] ?? '');
    $accountId = intval($_POST['account_id'] ?? 0);
    $newpass = $_POST['new_password'] ?? '';

    if ($username) {
        $stmt = $mysqli->prepare('SELECT id, salt FROM accounts WHERE name=?');
        $stmt->bind_param('s', $username);
        $stmt->execute();
        $res = $stmt->get_result();
        if ($row = $res->fetch_assoc()) {
            $accountId = intval($row['id']);
            $salt = $row['salt'];
        }
    } elseif ($accountId) {
        $stmt = $mysqli->prepare('SELECT salt FROM accounts WHERE id=?');
        $stmt->bind_param('i', $accountId);
        $stmt->execute();
        $res = $stmt->get_result();
        if ($row = $res->fetch_assoc()) {
            $salt = $row['salt'];
        }
    }

    if (!empty($salt) && $accountId && $newpass) {
        $hash = sha1($salt . $newpass);
        $upd = $mysqli->prepare('UPDATE accounts SET password=? WHERE id=?');
        $upd->bind_param('si', $hash, $accountId);
        $upd->execute();
        $message = 'Password updated.';
    } else {
        $message = 'Failed to update password.';
    }
}

if ($section === 'tables' && $table && $action) {
    if ($action === 'delete') {
        $id = intval($_POST['id']);
        $stmt = $mysqli->prepare("DELETE FROM `$table` WHERE id=?");
        $stmt->bind_param('i', $id);
        $stmt->execute();
    } else {
        $cols = get_columns($mysqli, $table);
        $values = [];
        $sets = [];
        $types = '';
        foreach ($cols as $c) {
            if ($c == 'id') continue;
            $values[] = $_POST[$c] ?? null;
            $sets[] = "`$c`=?";
            $types .= 's';
        }
        if ($action === 'update') {
            $id = intval($_POST['id']);
            $values[] = $id;
            $types .= 'i';
            $stmt = $mysqli->prepare("UPDATE `$table` SET " . implode(',', $sets) . " WHERE id=?");
        } else { // create
            $stmt = $mysqli->prepare("INSERT INTO `$table` (" . implode(',', array_slice($cols,1)) . ") VALUES (" . rtrim(str_repeat('?,', count($cols)-1), ',') . ")");
        }
        $stmt->bind_param($types, ...$values);
        $stmt->execute();
    }
    header('Location: admin.php?section=tables&table=' . urlencode($table));
    exit();
}

include 'header.php';
?>
<div class="container mx-auto">
<h2 class="text-xl font-semibold mb-4">Admin Panel</h2>
<nav class="mb-4 space-x-4">
    <a class="text-blue-400" href="admin.php?section=tables">Tables</a>
    <a class="text-blue-400" href="admin.php?section=ban">Ban Player</a>
    <a class="text-blue-400" href="admin.php?section=status">Change Status</a>
    <a class="text-blue-400" href="admin.php?section=items">Manage Items</a>
    <a class="text-blue-400" href="admin.php?section=itemlookup">Lookup Item</a>
    <a class="text-blue-400" href="admin.php?section=password">Reset Password</a>
</nav>
<?php if($message) { echo '<p class="text-green-400">'.htmlspecialchars($message).'</p>'; } ?>
<?php if ($section === 'tables' && !$table): ?>
    <h3 class="font-bold mb-2">Select a table to edit</h3>
    <ul class="list-disc pl-5">
    <?php if($res = $mysqli->query('SHOW TABLES')) { while($row = $res->fetch_array()) { ?>
        <li><a class="text-blue-400 hover:underline" href="admin.php?section=tables&amp;table=<?php echo urlencode($row[0]); ?>"><?php echo htmlspecialchars($row[0]); ?></a></li>
    <?php }} ?>
    </ul>
<?php elseif ($section === 'tables'): $cols = get_columns($mysqli, $table); ?>
    <a class="text-blue-400" href="admin.php?section=tables">&larr; Back to table list</a>
    <h3 class="font-bold mt-2 mb-2">Table: <?php echo htmlspecialchars($table); ?></h3>
    <?php if (isset($_GET['edit']) || isset($_GET['new'])): ?>
        if(isset($_GET['edit'])) {
            $id = intval($_GET['edit']);
            $res = $mysqli->query("SELECT * FROM `$table` WHERE id=$id");
            $row = $res->fetch_assoc();
            $action = 'update';
        } else {
            $row = array_fill_keys($cols, '');
            $row['id'] = '';
            $action = 'create';
        }
    ?>
        <form method="post" class="space-y-2 mt-2">
            <input type="hidden" name="section" value="tables" />
            <input type="hidden" name="action" value="<?php echo $action; ?>" />
            <input type="hidden" name="table" value="<?php echo htmlspecialchars($table); ?>" />
            <?php foreach ($cols as $c) { if($c == 'id' && $action=='create') continue; ?>
                <label class="block">
                    <?php echo htmlspecialchars($c); ?>:
                    <input type="text" name="<?php echo htmlspecialchars($c); ?>" value="<?php echo htmlspecialchars($row[$c] ?? ''); ?>" class="text-gray-800 p-1 rounded w-full" />
                </label>
            <?php } ?>
            <?php if ($action == 'update') { ?>
                <input type="hidden" name="id" value="<?php echo intval($row['id']); ?>" />
            <?php } ?>
            <input type="submit" class="bg-blue-600 hover:bg-blue-700 text-white py-1 px-3 rounded" value="Save" />
        </form>
    <?php else: ?>
        <a class="text-blue-400" href="admin.php?section=tables&amp;table=<?php echo urlencode($table); ?>&amp;new=1">Create new entry</a>
        <table class="min-w-full bg-gray-800 rounded mt-2">
            <thead>
            <tr>
                <?php foreach ($cols as $c) { ?>
                    <th class="p-2 text-left"><?php echo htmlspecialchars($c); ?></th>
                <?php } ?>
                <th class="p-2">Actions</th>
            </tr>
            </thead>
            <tbody>
            <?php if($res = $mysqli->query("SELECT * FROM `$table` LIMIT 50")) { while($row = $res->fetch_assoc()) { ?>
                <tr class="border-t border-gray-700">
                    <?php foreach ($cols as $c) { ?>
                        <td class="p-2 text-sm"><?php echo htmlspecialchars($row[$c]); ?></td>
                    <?php } ?>
                    <td class="p-2 space-x-2">
                        <a class="text-blue-400" href="admin.php?section=tables&amp;table=<?php echo urlencode($table); ?>&amp;edit=<?php echo intval($row['id']); ?>">Edit</a>
                        <form method="post" class="inline" onsubmit="return confirm('Delete entry?');">
                            <input type="hidden" name="section" value="tables" />
                            <input type="hidden" name="action" value="delete" />
                            <input type="hidden" name="table" value="<?php echo htmlspecialchars($table); ?>" />
                            <input type="hidden" name="id" value="<?php echo intval($row['id']); ?>" />
                            <input type="submit" value="Delete" class="bg-red-600 hover:bg-red-700 text-white py-1 px-2 rounded" />
                        </form>
                    </td>
                </tr>
            <?php }} ?>
            </tbody>
        </table>
    <?php endif; ?>
<?php elseif ($section === 'ban'): ?>
    <h3 class="font-bold mb-2">Ban Player</h3>
    <form method="post" class="space-y-2">
        <input type="hidden" name="section" value="ban" />
        <label class="block">Player ID:
            <input type="number" name="player_id" class="text-gray-800 p-1 rounded w-full" />
        </label>
        <input type="submit" value="Ban" class="bg-red-600 hover:bg-red-700 text-white py-1 px-3 rounded" />
    </form>
<?php elseif ($section === 'status'): ?>
    <h3 class="font-bold mb-2">Change Account Status</h3>
    <form method="post" class="space-y-2">
        <input type="hidden" name="section" value="status" />
        <label class="block">Username:
            <input type="text" name="username" class="text-gray-800 p-1 rounded w-full" />
        </label>
        <label class="block">or Account ID:
            <input type="number" name="account_id" class="text-gray-800 p-1 rounded w-full" />
        </label>
        <label class="block">Group ID:
            <input type="number" name="group_id" value="1" class="text-gray-800 p-1 rounded w-full" />
        </label>
        <label class="inline-flex items-center">
            <input type="checkbox" name="blocked" class="mr-2" /> Blocked
        </label>
        <input type="submit" value="Update" class="bg-blue-600 hover:bg-blue-700 text-white py-1 px-3 rounded" />
    </form>
<?php elseif ($section === 'items'): ?>
    <h3 class="font-bold mb-2">Manage Items</h3>
    <form method="post" class="space-y-2 mb-4">
        <input type="hidden" name="section" value="items" />
        <input type="hidden" name="add_item" value="1" />
        <label class="block">Item ID:
            <input type="number" name="id" class="text-gray-800 p-1 rounded w-full" />
        </label>
        <label class="block">Type:
            <input type="number" name="type" class="text-gray-800 p-1 rounded w-full" />
        </label>
        <label class="block">Name:
            <input type="text" name="name" class="text-gray-800 p-1 rounded w-full" />
        </label>
        <input type="submit" value="Add Item" class="bg-blue-600 hover:bg-blue-700 text-white py-1 px-3 rounded" />
    </form>
    <form method="post" class="space-y-2">
        <input type="hidden" name="section" value="items" />
        <input type="hidden" name="remove_item" value="1" />
        <label class="block">Item ID:
            <input type="number" name="id" class="text-gray-800 p-1 rounded w-full" />
        </label>
        <input type="submit" value="Remove Item" class="bg-red-600 hover:bg-red-700 text-white py-1 px-3 rounded" />
    </form>
<?php elseif ($section === 'itemlookup'): ?>
    <h3 class="font-bold mb-2">Lookup Item By Serial</h3>
    <form method="post" class="space-y-2 mb-4">
        <input type="hidden" name="section" value="itemlookup" />
        <label class="block">Serial:
            <input type="text" name="serial" class="text-gray-800 p-1 rounded w-full" value="<?php echo htmlspecialchars($_POST['serial'] ?? ''); ?>" />
        </label>
        <?php if(isset($itemdata)) { ?>
            <p class="break-all">Data (base64): <?php echo htmlspecialchars($itemdata); ?></p>
            <button type="submit" name="duplicate" value="1" class="bg-blue-600 hover:bg-blue-700 text-white py-1 px-3 rounded">Duplicate</button>
        <?php } ?>
        <input type="submit" value="Lookup" class="bg-blue-600 hover:bg-blue-700 text-white py-1 px-3 rounded" />
    </form>
<?php elseif ($section === 'password'): ?>
    <h3 class="font-bold mb-2">Reset Account Password</h3>
    <form method="post" class="space-y-2">
        <input type="hidden" name="section" value="password" />
        <label class="block">Username:
            <input type="text" name="username" class="text-gray-800 p-1 rounded w-full" />
        </label>
        <label class="block">or Account ID:
            <input type="number" name="account_id" class="text-gray-800 p-1 rounded w-full" />
        </label>
        <label class="block">New Password:
            <input type="password" name="new_password" class="text-gray-800 p-1 rounded w-full" />
        </label>
        <input type="submit" value="Change Password" class="bg-blue-600 hover:bg-blue-700 text-white py-1 px-3 rounded" />
    </form>
<?php endif; ?>
</div>
<?php include 'footer.php'; ?>
