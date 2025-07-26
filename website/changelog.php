<?php
include 'header.php';

$entries = [];
$file = __DIR__ . '/changelog.json';
if (file_exists($file)) {
    $json = file_get_contents($file);
    $data = json_decode($json, true);
    if (is_array($data)) {
        $entries = $data;
    }
}
?>
<div class="container mx-auto grid grid-cols-4 gap-4">
    <div class="col-span-3">
        <h2 class="text-xl font-bold mb-2">Changelog</h2>
        <?php if ($entries) { ?>
        <table class="table-auto border-collapse">
            <thead>
                <tr>
                    <th class="border px-4 py-2">Date</th>
                    <th class="border px-4 py-2">Update</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($entries as $entry) { ?>
                <tr>
                    <td class="border px-4 py-2"><?php echo htmlspecialchars($entry['date']); ?></td>
                    <td class="border px-4 py-2"><?php echo htmlspecialchars($entry['update']); ?></td>
                </tr>
                <?php } ?>
            </tbody>
        </table>
        <?php } else { ?>
        <p>No changelog available.</p>
        <?php } ?>
    </div>
    <div>
        <?php include 'sidebar.php'; ?>
    </div>
</div>
<?php include 'footer.php'; ?>
