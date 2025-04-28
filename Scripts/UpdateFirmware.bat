
@echo off
set args=%*
echo Arguments passed: %args%

set port=%2
set firmware=%1

echo Updating firmware on %port% with %firmware%
echo.

@REM echo Press any key to continue or Ctrl+C to cancel.
@REM pause >nul
@REM echo.

echo Starting firmware update...
echo.

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

REM Check if the port is available
@REM for /f "tokens=*" %%i in ('mode') do (
@REM     echo %%i
@REM     echo %%i | findstr /i "%port%" >nul
@REM     if errorlevel 1 (
@REM         echo Port %port% is not available. Please check the connection.
@REM         exit /b 1
@REM     )
@REM )

REM Start the firmware update process
echo Updating firmware on %port%...
echo.

REM Call arduino-cli to upload the firmware

set arduino-cli_path=.\tools\arduino-cli.exe

"%arduino-cli_path%" upload -p %port% -i %firmware% --fqbn arduino:avr:uno

if errorlevel 1 (
    echo Firmware update failed. Please check the connection and try again.
    exit /b 1
)

echo Firmware update completed successfully.
echo.