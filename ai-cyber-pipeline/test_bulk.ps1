# ------------------------------
# PowerShell Test for /bulk_ingest
# ------------------------------

$baseUrl = "http://localhost:5000/bulk_ingest"

Write-Host "=== Testing BULK LOG ingestion ===" -ForegroundColor Cyan

$logs = @{
    logs = @(
        "Oct 2 08:05:00 server sshd[12345]: Failed password for root from 203.91.112.5 port 22 ssh2",
        "Oct 2 08:10:00 server sshd[12346]: Accepted password for user from 192.168.1.10 port 22 ssh2",
        "Oct 2 08:12:00 server sshd[12347]: Failed password for admin from 203.91.112.8 port 22 ssh2"
    )
} | ConvertTo-Json -Depth 3

$responseLogs = Invoke-RestMethod -Uri $baseUrl -Method POST -ContentType "application/json" -Body $logs
$responseLogs | ConvertTo-Json -Depth 4 | Write-Output


Write-Host "`n=== Testing BULK MESSAGE ingestion ===" -ForegroundColor Cyan

$messages = @{
    messages = @(
        "Congratulations! You've won a lottery. Click here to claim.",
        "Your bank account has been blocked. Verify immediately.",
        "Hey, are we still on for lunch tomorrow?"
    )
} | ConvertTo-Json -Depth 3

$responseMsgs = Invoke-RestMethod -Uri $baseUrl -Method POST -ContentType "application/json" -Body $messages
$responseMsgs | ConvertTo-Json -Depth 4 | Write-Output
