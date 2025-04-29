
@echo off
setlocal

set args=%*
echo Arguments passed: %args%

set port=%2
set firmware=%1

REM Check if the firmware file exists
if not exist "%firmware%" (
    echo Firmware file not found: %firmware%
    exit /b 1
)

REM Check if the port is valid
if "%port%"=="" (
    echo No port specified. Please provide a valid port.
    exit /b 1
)

echo Updating firmware on %port% with %firmware%

REM Check if the port is available
@echo off
mode %port% >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo Port %port% is not available. Please check the connection.
  exit /b 1
) else (
  echo Port %port% is available.
)

REM Start the firmware update process
echo Updating firmware on %port%...

REM Call arduino-cli to upload the firmware

set arduino-cli_path=.\tools\arduino-cli.exe

"%arduino-cli_path%" upload -p %port% -i %firmware% --fqbn arduino:avr:uno

@REM "%arduino-cli_path%" compile -p %port% %firmware% --fqbn esp32:esp32:esp32

if %ERRORLEVEL% neq 0 (
    echo Firmware update failed. Please check the connection and try again.
    exit /b 1
)

echo Firmware update completed successfully.
echo.