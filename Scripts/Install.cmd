@echo off
rem -------------------------------------------------------------
rem Usage:  upload.cmd  [SKETCH_FILE] [COM_PORT]  [TELEMETRIX_ID]
rem Example: upload.cmd  COM5  3
rem If TELEMETRIX_ID omitted ⇒ defaults to 1
rem -------------------------------------------------------------
setlocal ENABLEDELAYEDEXPANSION

:: ---------- grab parameters ----------
set "file=%~1"
set "port=%~2"
set "id=%~3"
if "%id%"=="" set "id=1"

:: ---------- compute paths ----------
set "scriptDir=%~dp0"
for %%I in ("%scriptDir%\..") do set "baseDir=%%~fI"

set "toolDir=%baseDir%\tools"
set "arduino_cli=%toolDir%\arduino-cli.exe"
@REM set "sketchFile=%baseDir%\sketches\Telemetrix4Arduino\Telemetrix4Arduino.ino"
set "sketchFile=%baseDir%\%file%"
if not exist "%sketchFile%" (
    echo [ERROR] Sketch file "%sketchFile%" does not exist.  Exiting.
    exit /b 1
)
set "board=arduino:avr:uno"
set "buildDefinition=build.extra_flags=-DTELEMETRIX_ID=%id%"

:: ---------- sanity checks ----------
if "%port%"=="" (
    echo [ERROR] No COM port specified.  Exiting.
    exit /b 1
)
echo Uploading sketch "%sketchFile%" to %port%
echo Using Telemetrix ID  %id%

:: ---------- build + upload ----------
"%arduino_cli%" ^
    --config-file "%toolDir%\arduino-cli.yaml" ^
    --libraries "%toolDir%\libraries" ^
    --build-property "%buildDefinition%" ^
    compile -u -v --verify ^
    -b %board% -p %port% ^
    "%sketchFile%"

if errorlevel 1 (
    echo [ERROR] Upload failed.
    exit /b 1
) else (
    echo [OK] Sketch uploaded successfully.
    exit /b 0
)
