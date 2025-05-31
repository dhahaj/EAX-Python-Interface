
param (
    [string]$port = $null,
    [int]$id = 1
    )


$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$toolDir = Join-Path $scriptDir "..\tools"

$arduino_cli = Join-Path $scriptDir "..\tools\arduino-cli.exe"
$sketchFile = Join-Path $scriptDir "..\sketches\Telemetrix4Arduino\Telemetrix4Arduino.ino"

$board = "arduino:avr:uno"

if (-not $id) {
    Write-Output "No Telemetrix ID specified. Using default ID: 1"
    $id = 1
} else {
    Write-Output "Using specified Telemetrix ID: $id"
}

$buildDefinition = "build.extra_flags=-DTELEMETRIX_ID=$id"

function arduino-cli-custom {
   & $toolDir\arduino-cli.exe --config-file "$toolDir\arduino-cli.yaml"  $args --libraries "$toolDir\libraries" --build-property $buildDefinition
}


# Check if a COM port is specified
if (-not $port) {

    Write-Output "No COM port specified. Exiting script."

    exit 1

    Write-Output "No COM port specified. Please select a COM port from the list."

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
} else {
    $selectedPort = $port
    Write-Output "Using specified COM port: $selectedPort"
}


arduino-cli-custom compile -u -v -b $board --verify -p $selectedPort $sketchFile

# Verify if the sketch has been uploaded
if ($LASTEXITCODE -eq 0) {
    Write-Output "Sketch has been uploaded successfully."
    exit 0
}
else {
    Write-Output "Failed to upload the sketch."
    exit 1
}

    # $newDir = "$PWD\..\tools"

# Create the new directory if it does not exist
# if (-not (Test-Path $newDir)) {
#     New-Item -Path $newDir -ItemType Directory > $null
# }

# Define the extraction path
# $extractPath = "$PWD\..\tools\"

# & "$scriptDir\ArduinoInstall.ps1"

# Install Telemetrix4Arduino library using Arduino CLI
# & $arduino_cli lib install Telemetrix4Arduino

# Verify if the library has been installed
# if ($LASTEXITCODE -eq 0) {
#     Write-Output "Telemetrix4Arduino library has been installed successfully."
# }
# else {
#     Write-Output "Failed to install Telemetrix4Arduino library."
#     exit 1
# }

# Update the core index
# & $arduino_cli core update-index

# Install adafruit:avr core
# & $arduino_cli core install arduino:avr

# Verify if the core has been installed
# if ($LASTEXITCODE -eq 0) {
#     Write-Output "arduino:avr core has been installed successfully."
# }
# else {
#     Write-Output "Failed to install arduino:avr core."
#     exit 1
# }

# Define the board fqbn, sketch file location and port
# $sketch = "$PWD\..\sketches\Telemetrix4Arduino\Telemetrix4Arduino.ino"

# Compile the sketch
# & $arduino_cli compile --fqbn $fqbn $sketchFile

# Verify if the sketch has been compiled
# if ($LASTEXITCODE -eq 0) {
#     Write-Output "Sketch has been compiled successfully."
# }
# else {
#     Write-Output "Failed to compile the sketch."
#     exit 1
# }



# Upload the sketch
if (-not (Test-Path $arduino_cli)) {
    Write-Output "Error: arduino-cli.exe not found in the expected path: $arduino_cli"
    exit 1
}
if (-not (Test-Path $sketchFile)) {
    Write-Output "Error: Sketch file not found at: $sketchFile"
    exit 1
}
Write-Output "Uploading sketch ($sketchFile) to board ($fqbn) on port ($selectedPort)..."
& $arduino_cli compile -p $selectedPort -b $fqbn -v -t -u $sketchFile



# Remove-Item -Recurse ..\tools\
# Write-Output "Removing temporary files."