# Show usage
function Show-Usage {
    Write-Output "Usage: Upload.ps1 <firmware_file_path> <port>"
    Write-Output "Example: Upload.ps1 file.hex COM3"
}

# Install Arduino CLI if not already installed
. ".\Scripts\ArduinoInstall.ps1" *>&1

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$arduino_cli = Join-Path $scriptDir "..\tools\arduino-cli.exe"


# $firmware = "$PWD\..\sketches\Telemetrix4Arduino\build\arduino.avr.uno\Telemetrix4Arduino.ino.hex"
$firmware = $args[0]
if (-not $firmware) {
    Write-Output "Error: No firmware file provided."
    Show-Usage
    exit 1
}

$port = $args[1]
if (-not $port) {
    Write-Output "Error: No port provided."
    Show-Usage
    exit 1
}

$board = "arduino:avr:uno"

Write-Output "Uploading firmware ($firmware) to board ($board) on port ($port)..."

& "$arduino_cli" upload -p $port --fqbn $board -i $firmware -v -t 

if ($LASTEXITCODE -eq 0) {
    Write-Output "Firmware has been uploaded successfully."
} else {
    Write-Output "Failed to upload the firmware."
    exit 1
}

