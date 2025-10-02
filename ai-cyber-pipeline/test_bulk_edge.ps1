$baseUrl = "http://localhost:5000/bulk_ingest"
Write-Host "=== Bulk logs (edge cases) ==="

$logs = @{
    logs = @(
        "Oct 2 08:05:00 server sshd[12345]: Failed password for root from 203.91.112.5 port 22 ssh2",
        "   ",  # whitespace-only (should be skipped)
        "Oct 2 08:10:00 server sshd[12346]: Accepted password for user1 from 10.0.0.5 port 22 ssh2",
        "Malformed log entry without expected format",
        ("A" * 1000)  # very long line
    )
} | ConvertTo-Json -Depth 4

$response = Invoke-RestMethod -Uri $baseUrl -Method POST -ContentType "application/json" -Body $logs
$response | ConvertTo-Json -Depth 5 | Out-File "outputs/bulk_logs_test_response.json"
Write-Host "Saved outputs/bulk_logs_test_response.json"

Write-Host "`n=== Bulk messages (edge cases) ==="
$messages = @{
    messages = @(
        "Congratulations! You've won a lottery. Click here to claim.",
        "",
        "Your bank account has been blocked. Verify immediately.",
        "Hello, this is a test message (unicode placeholder)",
        ("Spam" * 200)
    )
} | ConvertTo-Json -Depth 4

$response = Invoke-RestMethod -Uri $baseUrl -Method POST -ContentType "application/json" -Body $messages
$response | ConvertTo-Json -Depth 5 | Out-File "outputs/bulk_messages_test_response.json"
Write-Host "Saved outputs/bulk_messages_test_response.json"

