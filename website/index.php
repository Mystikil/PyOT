<?php
require_once 'config.php';

$news = [];
if ($mysqli) {
    if ($result = $mysqli->query('SELECT title, body, posted_at FROM news ORDER BY posted_at DESC LIMIT 5')) {
        while ($row = $result->fetch_assoc()) {
            $news[] = $row;
        }
    }
}
?>
<?php include 'header.php'; ?>
<div class="container mx-auto grid grid-cols-12 gap-4">
    <div class="col-span-3 space-y-4">
        <div class="bg-gray-800 p-4 rounded">Left Box 1</div>
        <div class="bg-gray-800 p-4 rounded">Left Box 2</div>
    </div>
    <div class="col-span-6 space-y-4">
        <?php if ($news) { ?>
            <?php foreach ($news as $row) { ?>
            <div class="bg-gray-800 p-4 rounded border border-gray-700 custom-shadow">
                <h3 class="text-lg font-bold mb-1"><?php echo htmlspecialchars($row['title']); ?></h3>
                <p class="text-sm text-gray-400 mb-2"><?php echo date('Y-m-d H:i', intval($row['posted_at'])); ?></p>
                <div><?php echo $row['body']; ?></div>
            </div>
            <?php } ?>
        <?php } else { ?>
            <p>No news entries found.</p>
        <?php } ?>
    </div>
    <div class="col-span-3 space-y-4">
        <div class="bg-gray-800 p-4 rounded">Right Box 1</div>
        <div class="bg-gray-800 p-4 rounded">Right Box 2</div>
    </div>
</div>
<?php include 'footer.php'; ?>
