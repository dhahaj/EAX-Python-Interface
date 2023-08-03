# This script will update the firmware on the Arduino board. 

function Print-Usage {
    Write-Output "Usage: "
    Write-Output "    UpdateFirmware.ps1 [arduinoId] [port]"
    Write-Output "      arduinoId: The id of the arduino board."
    Write-Output "      port: The COM port to use."
    Write-Output ""
    Write-Output "If the arguments are not provided, the script will prompt for user input."
    Write-Output ""
}

# Create the new directory if it does not exist
if (-not (Test-Path "tools")) {
    New-Item -Path "tools" -ItemType Directory > $null
}

# Install arduino-cli.exe
. ".\Scripts\ArduinoInstall.ps1" *>&1
# & "$PWD\Scripts\ArduinoInstall.ps1"

$arduino_cli = ".\tools\arduino-cli.exe"

Write-Output "$PWD"

function Install-Telemetrix4Arduino {
    # Install Telemetrix4Arduino library using Arduino CLI
    . "$arduino_cli" lib install Telemetrix4Arduino *>&1

    # Verify if the library has been installed
    if ($LASTEXITCODE -eq 0) {
        Write-Output "Telemetrix4Arduino library has been installed successfully."
    }
    else {
        Write-Output "Failed to install Telemetrix4Arduino library."
        exit 1
    }
}

Install-Telemetrix4Arduino

function Update-Arduino {
    
    # Update the core index
    Write-Output "Updating core index."
    . "$arduino_cli" core update-index *>&1


    # Install adafruit:avr core
    Write-Output "Installing arduino:avr core."
    . "$arduino_cli" core install arduino:avr *>&1

    
    # Verify if the core has been installed
    if ($LASTEXITCODE -eq 0) {
        Write-Output "arduino:avr:uno core has been installed successfully."
    }
    else {
        Write-Output "Failed to install arduino:avr:uno."
        exit 1
    }

}

Update-Arduino


# Exit function
function Exit-Function {
    Write-Output "Exiting script."
    exit 1
}

# Define the board fqbn, sketch file location and port
$fqbn = "arduino:avr:uno" # Arduino Uno
# $fqbn = "arduino:avr:mega" # Arduino Mega
$sketch = ".\sketches\Telemetrix4Arduino\Telemetrix4Arduino.ino"
$headerFile = ".\sketches\Telemetrix4Arduino\Telemetrix4Arduino_config.h"
$logfile = ".\tools\arduino_log"

# Get the arduino id
if ($args.Length -lt 1) {
    Read-Host -Prompt 'Please enter the arduino id: ' -OutVariable arduinoId > $null
}
else {
    $arduinoId = $args[0]
}

Write-Output "Using arduino id: $arduinoId"
Write-Output "Parameters:"
Write-Output "arduino_cli: $arduino_cli"
Write-Output "fqbn: $fqbn"
Write-Output "sketch: $sketch"
Write-Output "headerFile: $headerFile"
$arduinoId = "TELEMETRIX4ARDUINO_ID $arduinoId"


Set-Content -Path $headerFile -Value "#define $arduinoId"


# Compile the sketch
. "$arduino_cli" compile --log-file $logfile --log-level info --fqbn $fqbn $sketch *>&1



# Verify if the sketch has been compiled
if ($LASTEXITCODE -eq 0) {
    Write-Output "Sketch has been compiled successfully."
}
else {
    Write-Output "Failed to compile the sketch."
    Write-Output "View the log file for more information: $logfile"
    Exit-Function
}



if ($args.Length -lt 2) {

    # List all COM ports
    $comPorts = [System.IO.Ports.SerialPort]::getportnames()

    # Print all COM ports
    Write-Output "Available COM ports:"
    for ($i = 0; $i -lt $comPorts.Length; $i++) {
        Write-Output "  $($i + 1): $($comPorts[$i])"
    }

    # Ask for user input
    $selectedPortIndex = Read-Host -Prompt 'Please enter the number of the COM port to use'

    # Get the selected COM port
    $selectedPort = $comPorts[$selectedPortIndex - 1]

}
else {
    $selectedPort = $args[1]
}


Write-Output "You selected COM port: $selectedPort"

Write-Output "Uploading sketch."

# Upload the sketch
. "$arduino_cli" upload -p $selectedPort --log-file $logfile --log-level info --fqbn $fqbn $sketch *>&1


# Verify if the sketch has been uploaded
if ($LASTEXITCODE -eq 0) {
    Write-Output "Sketch has been uploaded successfully."
    exit 0
}
else {
    Write-Output "Failed to upload the sketch."
    Write-Output "View the log file for more information: $logfile"
    Exit-Function
}


function Remove-Temporary-Files {
    Remove-Item -Recurse ..\tools\
    Write-Output "Removed temporary files."    
}


