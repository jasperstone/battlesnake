$dateString = Get-Date -Format "yyyMMdd_HHmm"
$outFolder = "$PSScriptRoot/tests/$dateString"

if (!(Test-Path $outFolder)) {
    New-Item -ItemType Directory -Path $outFolder
}

0..10 | ForEach-Object -Parallel {
    $port1 = 8000 + $_ * 10
    $port2 = $port1 + 1
    $outFile = "$using:outFolder/$_.txt"

    $snake1proc = Start-Process -PassThru -FilePath python -ArgumentList "main.py --port $port1"
    $snake2proc = Start-Process -PassThru -FilePath python -ArgumentList "simple.py --port $port2 --seed 0"

    Start-Sleep 10
    Start-Process -Wait -FilePath .\battlesnake.exe -ArgumentList "play -W 11 -H 11 --name us --url http://localhost:$port1 --name them --url http://localhost:$port2 --output $outFile --browser"

    Stop-Process -Id $snake1proc.Id
    Stop-Process -Id $snake2proc.Id
}