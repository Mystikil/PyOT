<?php
// Database configuration derived from config.py
$DB_HOST = 'localhost';
$DB_USER = 'root';
$DB_PASS = '';

$DB_NAME = 'pyotz';

// Host and port of the game server used for status checks
$SERVER_STATUS_HOST = '127.0.0.1';
$SERVER_STATUS_PORT = 7172;

// Minimum group id considered an admin account
define('ADMIN_GROUP_ID', 6);


$mysqli = new mysqli($DB_HOST, $DB_USER, $DB_PASS, $DB_NAME);
if ($mysqli->connect_errno) {
    die('Failed to connect to MySQL: ' . $mysqli->connect_error);
}

session_start();
?>
