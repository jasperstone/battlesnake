$terminalProfile = "PowerShell"

wt --window 0 new-tab -p $terminalProfile -d . `
    pwsh -noExit -Command {
        python main.py --port 8000
    }

wt --window 0 new-tab -p $terminalProfile -d . `
    pwsh -noExit -Command {
        python simple.py --port 8001 --seed 0
    }

Start-Sleep 3
wt --window 0 new-tab -p $terminalProfile -d . `
    pwsh -noExit -Command { `
        .\battlesnake.exe play `
        -W 11 `
        -H 11 `
        --name "us" `
        --url http://localhost:8000 `
        --name "them" `
        --url http://localhost:8001 `
        --browser
    }