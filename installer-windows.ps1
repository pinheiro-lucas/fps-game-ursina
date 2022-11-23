# To use any remove script the first time, type into a powershell:
# Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

echo "[1/8] Installing Scoop"

try {
	irm get.scoop.sh | iex
} finally {
    try { scoop install git } finally {
        $buckets = 'main'
        foreach ($bucket in $buckets) {
            try {
                echo "[2/8] Adding bucket $bucket..."
                scoop bucket add $bucket
            } finally {
                # Nothing here because its just a warning.
            }
        }

		Write-Host "[3/8] Updating Scoop..."
		scoop update git
		scoop update

		echo "[4/8] Installing Python"


		$packages = 'python'

		foreach ($package in $packages) {
			try { scoop install $package } finally { scoop update $package }
		}
	}

	echo ""
	scoop status

	echo "[5/8] Creating the virtual env"
	python -m venv venv

	.\venv\Scripts\Activate.ps1

	echo "[6/8] Installing requirements"
    pip install -r requirements.txt

    echo "[7/8] Setup server information:"

    $server_ip = Read-Host "Server IP"
    $server_ssl = Read-Host "Is SSL connection [Y/n]?"
    if ($server_ssl -eq 'y' -OR $server_ssl -eq 'Y' -OR $server_ssl -eq '') {
        $server_ssl = "true"
        $server_port = ""
    } else {
        $server_ssl = "false"
        $server_port = Read-Host "Server Port"
    }

    $config = @"
SERVER_IP="$server_ip"
SERVER_PORT="$server_port"
SERVER_SSL="$server_ssl"
DEVELOPMENT_MODE="false"
FULLSCREEN="true"
"@

    New-Item .\.env
    Set-Content .\.env "$config"

    echo "[8/8] Starting the game"
    python .\main.py

    pause
}
Footer
