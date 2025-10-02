$baseUrl = "http://localhost:5000/ingest_message"

# Read each line from data/message.txt
$messages = Get-Content -Path "data/message.txt"

foreach ($msg in $messages) {
    if (![string]::IsNullOrWhiteSpace($msg)) {
        # Ensure message is sent as a simple string JSON
        $payload = @{ message = [string]$msg } | ConvertTo-Json -Compress
        try {
            $response = Invoke-RestMethod -Uri $baseUrl -Method POST -ContentType "application/json" -Body $payload
            Write-Host "Sent: $msg"
            Write-Host "Response:" ($response | ConvertTo-Json -Depth 5)
            "`n"
        }
        catch {
            Write-Host "Error sending message: $msg"
            Write-Host $_.Exception.Message
        }
    }
}
