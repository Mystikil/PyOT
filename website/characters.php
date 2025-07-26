<?php
require_once 'config.php';
if (!isset($_SESSION['account_id'])) {
    header('Location: index.php');
    exit();
}
$accountId = $_SESSION['account_id'];
$result = $mysqli->prepare('SELECT id,name FROM players WHERE account_id=?');
$result->bind_param('i', $accountId);
$result->execute();
$characters = $result->get_result();
?>
<?php include 'header.php'; ?>
<h2 class="text-xl font-semibold mb-4">My Characters</h2>
<table class="min-w-full bg-gray-800 rounded">
<thead>
  <tr class="text-left">
    <th class="p-2">Name</th>
    <th class="p-2">Actions</th>
  </tr>
</thead>
<tbody>
<?php while($row = $characters->fetch_assoc()) { ?>
  <tr class="border-t border-gray-700">
    <td class="p-2"><a class="text-blue-400 hover:underline" href="character.php?id=<?php echo $row['id']; ?>"><?php echo htmlspecialchars($row['name']); ?></a></td>
    <td class="p-2">
        <form class="inline" method="post" action="delete_character.php">
            <input type="hidden" name="id" value="<?php echo $row['id']; ?>" />
            <input class="bg-red-600 hover:bg-red-700 text-white py-1 px-2 rounded" type="submit" value="Delete" />
        </form>
    </td>
  </tr>
<?php } ?>
</tbody>
</table>

<?php include 'footer.php'; ?>
