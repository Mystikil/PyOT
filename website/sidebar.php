<?php
require_once __DIR__.'/config.php';

$highscores = [];
if ($mysqli) {
    if ($result = $mysqli->query("SELECT name, experience FROM players ORDER BY experience DESC LIMIT 5")) {
        while ($row = $result->fetch_assoc()) {
            $highscores[] = $row;
        }
    }
    $mostKills = [];
    if ($result = $mysqli->query("SELECT p.name, COUNT(*) as kills FROM pvp_deaths d JOIN players p ON d.killer_id = p.id GROUP BY d.killer_id ORDER BY kills DESC LIMIT 5")) {
        while ($row = $result->fetch_assoc()) {
            $mostKills[] = $row;
        }
    }
    // Fetch number of players currently online
    $onlineCount = null;
    if ($result = $mysqli->query("SELECT COUNT(*) as cnt FROM players WHERE online = 1")) {
        $row = $result->fetch_assoc();
        $onlineCount = intval($row['cnt']);
    }
}

// Determine if the game server is reachable
$serverOnline = false;
if (isset($SERVER_STATUS_HOST, $SERVER_STATUS_PORT)) {
    $fp = @fsockopen($SERVER_STATUS_HOST, $SERVER_STATUS_PORT, $errno, $errstr, 1);
    if ($fp) {
        $serverOnline = true;
        fclose($fp);
    }
}
?>
<div class="space-y-4">
    <div class="bg-gray-100 p-4 rounded">
        <h3 class="font-bold mb-2">Links</h3>
        <ul class="list-disc pl-5 space-y-1">
            <li><a class="text-blue-500 hover:underline" href="features.php">Features</a></li>
            <li><a class="text-blue-500 hover:underline" href="downloads.php">Downloads</a></li>
            <li><a class="text-blue-500 hover:underline" href="community.php">Community</a></li>
            <li><a class="text-blue-500 hover:underline" href="media.php">Media</a></li>
            <li><a class="text-blue-500 hover:underline" href="support.php">Support</a></li>
            <li><a class="text-blue-500 hover:underline" href="changelog.php">Changelog</a></li>
        </ul>
    </div>

    <div class="bg-gray-100 p-4 rounded">
        <h3 class="font-bold mb-2">Server Status</h3>
        <p>Status: <?php echo $serverOnline ? '<span class="text-green-600">Online</span>' : '<span class="text-red-600">Offline</span>'; ?></p>
        <?php if ($onlineCount !== null) { ?>
        <p>Players online: <?php echo $onlineCount; ?></p>
        <?php } ?>
    </div>
    <?php if ($highscores) { ?>
    <div class="bg-gray-100 p-4 rounded">
        <h3 class="font-bold mb-2">Highscores</h3>
        <ul class="space-y-1">
            <?php foreach ($highscores as $row) { ?>
            <li><a class="text-blue-500 hover:underline" href="character.php?name=<?php echo urlencode($row['name']); ?>"><?php echo htmlspecialchars($row['name']); ?></a> - <?php echo intval($row['experience']); ?></li>
            <?php } ?>
        </ul>
    </div>
    <?php } ?>
    <?php if (!empty($mostKills)) { ?>
    <div class="bg-gray-100 p-4 rounded">
        <h3 class="font-bold mb-2">Most Kills</h3>
        <ul class="space-y-1">
            <?php foreach ($mostKills as $row) { ?>
            <li><a class="text-blue-500 hover:underline" href="character.php?name=<?php echo urlencode($row['name']); ?>"><?php echo htmlspecialchars($row['name']); ?></a> - <?php echo intval($row['kills']); ?></li>
            <?php } ?>
        </ul>
    </div>
    <?php } ?>
    <div class="bg-gray-100 p-4 rounded">
        <h3 class="font-bold mb-2">Discord</h3>
        <iframe src="https://discord.com/widget?id=YOUR_DISCORD_ID&theme=dark" width="100%" height="300" allowtransparency="true" frameborder="0"></iframe>
    </div>
</div>
