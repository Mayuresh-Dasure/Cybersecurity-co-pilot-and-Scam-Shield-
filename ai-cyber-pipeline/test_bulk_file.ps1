$baseUrl = "http://localhost:5000/bulk_ingest"

# Helper to post in batches
function Post-Batches($lines, $type, $batchSize=100) {
    for ($i = 0; $i -lt $lines.Count; $i += $batchSize) {
        $end = [Math]::Min($i + $batchSize - 1, $lines.Count - 1)
        $batch = $lines[$i..$end]
        $body = if ($type -eq "log") { @{ logs = $batch } } else { @{ messages = $batch } }
        $json = $body | ConvertTo-Json -Depth 4
        try {
            $resp = Invoke-RestMethod -Uri $baseUrl -Method POST -ContentType "application/json" -Body $json
            $resp | ConvertTo-Json -Depth 5 | Out-File "outputs/bulk_${type}_response_${i}.json"
            Write-Host "Posted $type batch $i..$end -> processed:$($resp.processed) skipped:$($resp.skipped)"
        } catch {
            Write-Host "Error posting batch $i: $_"
        }
    }
}

# Read and clean files
if (Test-Path "data/log.txt") {
    $logLines = Get-Content "data/log.txt" | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
    Post-Batches -lines $logLines -type "log" -batchSize 200
} else {
    Write-Host "data/log.txt not found"
}

if (Test-Path "data/message.txt") {
    $msgLines = Get-Content "data/message.txt" | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
    Post-Batches -lines $msgLines -type "message" -batchSize 200
} else {
    Write-Host "data/message.txt not found"
}
