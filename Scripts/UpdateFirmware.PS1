# This script will update the firmware on the Arduino board. 

# Define the URL to the Arduino CLI zip file
$url = "https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip"

$newDir = "$PWD\..\temp"

# Create the new directory if it does not exist
if (-not (Test-Path $newDir)) {
    New-Item -Path $newDir -ItemType Directory > $null
}

# Define the output location
$output = "$PWD\..\temp\arduino-cli_latest_Windows_64bit.zip"

# Define the extraction path
$extractPath = "$PWD\..\temp\"

# Install arduino-cli.exe
& "$PWD\ArduinoInstall.ps1"

# Install Telemetrix4Arduino library using Arduino CLI
& "$extractPath\arduino-cli.exe" lib install Telemetrix4Arduino

# Verify if the library has been installed
if ($LASTEXITCODE -eq 0) {
    Write-Output "Telemetrix4Arduino library has been installed successfully."
}
else {
    Write-Output "Failed to install Telemetrix4Arduino library."
    exit 1
}

# Update the core index
& "$extractPath\arduino-cli.exe" core update-index

# Install adafruit:avr core
& "$extractPath\arduino-cli.exe" core install adafruit:avr

# Verify if the core has been installed
if ($LASTEXITCODE -eq 0) {
    Write-Output "adafruit:avr core has been installed successfully."
}
else {
    Write-Output "Failed to install adafruit:avr core."
    exit 1
}

# Define the board fqbn, sketch file location and port
$fqbn = "adafruit:avr:metro"
$sketch = "$PWD\..\sketches\Telemetrix4Arduino\Telemetrix4Arduino.ino"

Read-Host -Prompt 'Please enter the arduino id: ' -OutVariable arduinoId > $null

$headerFile = "$PWD\..\sketches\Telemetrix4Arduino\Telemetrix4Arduino_config.h"

$arduinoId = "TELEMETRIX4ARDUINO_ID $arduinoId"

# Replace the arduino id in the header file
(Get-Content $headerFile) | ForEach-Object { $_ -replace "TELEMETRIX4ARDUINO_ID 1", $arduinoId } | Set-Content $headerFile

# Compile the sketch
& "..\temp\arduino-cli.exe" compile --fqbn $fqbn $sketch

# Verify if the sketch has been compiled
if ($LASTEXITCODE -eq 0) {
    Write-Output "Sketch has been compiled successfully."
}
else {
    Write-Output "Failed to compile the sketch."
    exit 1
}

# List all COM ports
$comPorts = [System.IO.Ports.SerialPort]::getportnames()

# Print all COM ports
Write-Output "Available COM ports:"
for ($i=0; $i -lt $comPorts.Length; $i++) {
    Write-Output "  $($i + 1): $($comPorts[$i])"
}

# Ask for user input
$selectedPortIndex = Read-Host -Prompt 'Please enter the number of the COM port to use'

# Get the selected COM port
$selectedPort = $comPorts[$selectedPortIndex - 1]

Write-Output "You selected COM port: $selectedPort"

# Upload the sketch
& "..\temp\arduino-cli.exe" upload -p $selectedPort --fqbn $fqbn $sketch

# Verify if the sketch has been uploaded
if ($LASTEXITCODE -eq 0) {
    Write-Output "Sketch has been uploaded successfully to $port."
}
else {
    Write-Output "Failed to upload the sketch."
    exit 1
}

Remove-Item -Recurse ..\temp\
Write-Output "Removing temporary files."