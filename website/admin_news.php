<?php
require_once 'config.php';
if (!isset($_SESSION['account_id']) || !$_SESSION['is_admin']) {
    header('Location: index.php');
    exit();
}

$editId = intval($_GET['edit'] ?? 0);
$title = '';
$body = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';
    $id = intval($_POST['id'] ?? 0);
    $title = trim($_POST['title'] ?? '');
    $body = trim($_POST['body'] ?? '');

    if ($action === 'create' && $title && $body) {
        $stmt = $mysqli->prepare('INSERT INTO news (title, body, posted_at) VALUES (?, ?, UNIX_TIMESTAMP())');
        $stmt->bind_param('ss', $title, $body);
        $stmt->execute();
        header('Location: admin_news.php');
        exit();
    } elseif ($action === 'update' && $id) {
        $stmt = $mysqli->prepare('UPDATE news SET title=?, body=? WHERE id=?');
        $stmt->bind_param('ssi', $title, $body, $id);
        $stmt->execute();
        header('Location: admin_news.php');
        exit();
    } elseif ($action === 'delete' && $id) {
        $stmt = $mysqli->prepare('DELETE FROM news WHERE id=?');
        $stmt->bind_param('i', $id);
        $stmt->execute();
        header('Location: admin_news.php');
        exit();
    }
}

if ($editId) {
    $stmt = $mysqli->prepare('SELECT title, body FROM news WHERE id=?');
    $stmt->bind_param('i', $editId);
    $stmt->execute();
    $res = $stmt->get_result();
    if ($row = $res->fetch_assoc()) {
        $title = $row['title'];
        $body = $row['body'];
    } else {
        $editId = 0;
    }
}

$news = [];
if ($res = $mysqli->query('SELECT id, title, posted_at FROM news ORDER BY posted_at DESC')) {
    while ($row = $res->fetch_assoc()) {
        $news[] = $row;
    }
}
?>
<?php include 'header.php'; ?>
<div class="container mx-auto grid grid-cols-4 gap-4">
    <div class="col-span-3">
        <h2 class="text-xl font-bold mb-2">News Administration</h2>
        <form method="post" class="space-y-2">
            <?php if ($editId) { ?>
            <input type="hidden" name="action" value="update" />
            <input type="hidden" name="id" value="<?php echo $editId; ?>" />
            <?php } else { ?>
            <input type="hidden" name="action" value="create" />
            <?php } ?>
            <label class="block">Title:
                <input type="text" name="title" value="<?php echo htmlspecialchars($title); ?>" class="border p-1 w-full" />
            </label>
            <label class="block">Body:
                <textarea id="news-body" name="body" rows="10" class="border p-1 w-full"><?php echo htmlspecialchars($body); ?></textarea>
            </label>
            <input type="submit" value="<?php echo $editId ? 'Update' : 'Create'; ?>" class="bg-blue-500 text-white px-4 py-2 rounded" />
            <?php if ($editId) { ?>
            <a href="admin_news.php" class="text-blue-500 ml-2">Cancel</a>
            <?php } ?>
        </form>
        <h3 class="text-lg font-bold mt-4">Existing News</h3>
        <table class="border-collapse border border-gray-400 mt-2">
            <tr><th class="border p-2">Title</th><th class="border p-2">Posted</th><th class="border p-2">Actions</th></tr>
            <?php foreach ($news as $row) { ?>
            <tr>
                <td class="border p-2"><?php echo htmlspecialchars($row['title']); ?></td>
                <td class="border p-2"><?php echo date('Y-m-d H:i', intval($row['posted_at'])); ?></td>
                <td class="border p-2">
                    <a href="admin_news.php?edit=<?php echo $row['id']; ?>" class="text-blue-500">Edit</a>
                    <form method="post" class="inline" action="admin_news.php" onsubmit="return confirm('Delete this entry?');">
                        <input type="hidden" name="action" value="delete" />
                        <input type="hidden" name="id" value="<?php echo $row['id']; ?>" />
                        <input type="submit" value="Delete" class="bg-red-500 text-white px-2 py-1 rounded ml-2" />
                    </form>
                </td>
            </tr>
            <?php } ?>
        </table>
    </div>
    <div>
        <?php include 'sidebar.php'; ?>
    </div>
</div>
<?php include 'footer.php'; ?>
<script src="https://cdn.tiny.cloud/1/no-api-key/tinymce/6/tinymce.min.js" referrerpolicy="origin"></script>
<script>
tinymce.init({
    selector: '#news-body',
    plugins: 'image link lists advlist code',
    toolbar: 'undo redo | styles | bold italic underline | alignleft aligncenter alignright | bullist numlist outdent indent | forecolor | image | code',
    menubar: false,
    branding: false
});
</script>
