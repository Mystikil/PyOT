<?php
require_once 'config.php';

$name = isset($_GET['name']) ? trim($_GET['name']) : '';
$id = isset($_GET['id']) ? intval($_GET['id']) : 0;

if ($id) {
    $stmt = $mysqli->prepare('SELECT p.id,p.name,p.sex,p.health,p.mana,p.experience,s.fist,s.sword,s.club,s.axe,s.distance,s.shield,s.fishing FROM players p LEFT JOIN player_skills s ON p.id=s.player_id WHERE p.id=?');
    $stmt->bind_param('i', $id);
} elseif ($name) {
    $stmt = $mysqli->prepare('SELECT p.id,p.name,p.sex,p.health,p.mana,p.experience,s.fist,s.sword,s.club,s.axe,s.distance,s.shield,s.fishing FROM players p LEFT JOIN player_skills s ON p.id=s.player_id WHERE p.name=?');
    $stmt->bind_param('s', $name);
} else {
    header('Location: index.php');
    exit();
}

$stmt->execute();
$result = $stmt->get_result();
$character = $result->fetch_assoc();
if (!$character) {
    echo 'Character not found';
    exit();
}

function levelFromExp($exp) {
    $l1 = pow(sqrt(3)*sqrt((243*($exp**2)) - (48600*$exp) + 3680000) + (27*$exp) - 2700, 1.0/3);
    $l2 = pow(30, 2.0/3);
    $l3 = 5 * pow(10, 2.0/3);
    $l4 = pow(3, 1.0/3) * $l1;
    return (int) round(($l1/$l2) - ($l3/$l4) + 2);
}

$level = levelFromExp($character['experience']);
?>
<?php include 'header.php'; ?>
<h2 class="text-xl font-semibold mb-4">Character Stats: <?php echo htmlspecialchars($character['name']); ?></h2>
<table class="min-w-full bg-gray-800 rounded mb-4">
    <tbody>
        <tr class="border-t border-gray-700"><th class="p-2 text-left">Level</th><td class="p-2"><?php echo $level; ?></td></tr>
        <tr class="border-t border-gray-700"><th class="p-2 text-left">Experience</th><td class="p-2"><?php echo intval($character['experience']); ?></td></tr>
        <tr class="border-t border-gray-700"><th class="p-2 text-left">Health</th><td class="p-2"><?php echo intval($character['health']); ?></td></tr>
        <tr class="border-t border-gray-700"><th class="p-2 text-left">Mana</th><td class="p-2"><?php echo intval($character['mana']); ?></td></tr>
    </tbody>
</table>
<h3 class="text-lg font-semibold mb-2">Skills</h3>
<table class="min-w-full bg-gray-800 rounded">
    <thead>
        <tr class="text-left">
            <th class="p-2">Fist</th>
            <th class="p-2">Sword</th>
            <th class="p-2">Club</th>
            <th class="p-2">Axe</th>
            <th class="p-2">Distance</th>
            <th class="p-2">Shield</th>
            <th class="p-2">Fishing</th>
        </tr>
    </thead>
    <tbody>
        <tr class="border-t border-gray-700">
            <td class="p-2 text-center"><?php echo intval($character['fist']); ?></td>
            <td class="p-2 text-center"><?php echo intval($character['sword']); ?></td>
            <td class="p-2 text-center"><?php echo intval($character['club']); ?></td>
            <td class="p-2 text-center"><?php echo intval($character['axe']); ?></td>
            <td class="p-2 text-center"><?php echo intval($character['distance']); ?></td>
            <td class="p-2 text-center"><?php echo intval($character['shield']); ?></td>
            <td class="p-2 text-center"><?php echo intval($character['fishing']); ?></td>
        </tr>
    </tbody>
</table>
<?php include 'footer.php'; ?>
