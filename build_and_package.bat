@echo off

REM Clean previous builds
echo Cleaning previous builds...
rmdir /s /q build
rmdir /s /q dist
del InsideImmune.exe 2>nul
del InsideImmune.zip 2>nul

REM Build the project
echo Building the project...
pyinstaller --onefile --name InsideImmune --distpath . --add-data "assets;assets" --add-data "data;data" main.py

REM Check if the build was successful
if exist "InsideImmune.exe" (
    echo Build completed successfully.
) else (
    echo Build failed. Exiting...
    exit /b 1
)

REM Package the executable and required files into a zip
echo Packaging the game into InsideImmune-Windows.zip...
powershell -Command "Compress-Archive -Path InsideImmune.exe, assets, data, README.md -DestinationPath InsideImmune-Windows.zip"

echo Packaging complete. InsideImmune-Windows.zip is ready for distribution!
pause