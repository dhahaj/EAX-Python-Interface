
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

# Check if the Arduino CLI is already installed
if (Test-Path -Path "..\temp\arduino-cli.exe") {
    Write-Output "Arduino CLI is already installed."
}
else {
    # Download the file
    Invoke-WebRequest -Uri $url -OutFile $output

    # Verify if the file has been downloaded
    if (Test-Path -Path $output) {
        Write-Output "Arduino CLI zip file has been downloaded successfully to $output"

        # Unzip the contents
        Expand-Archive -Path $output -DestinationPath $extractPath -Force

        Write-Output "Arduino CLI zip file has been extracted successfully to $extractPath"
    }
    else {
        Write-Output "Failed to download Arduino CLI zip file."
        exit 1
    }

}