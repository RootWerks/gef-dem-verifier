$ErrorActionPreference = "Stop"
$vectorFile = "vectors/golden.json"

if (-not (Test-Path $vectorFile)) {
    Write-Error "Error: $vectorFile not found."
    exit 1
}

$vectors = Get-Content -Raw $vectorFile | ConvertFrom-Json
foreach ($v in $vectors) {
    $jsonLine = $v | ConvertTo-Json -Compress
    Write-Host "--- Vector: $jsonLine"
    $jsonLine | python harness\eval.py
}
