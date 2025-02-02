@echo off
echo Creating models directory...
mkdir models
if errorlevel 1 (
    echo Failed to create models directory
    pause
    exit /b 1
)

echo Installing required packages...

echo Installing PyQt5...
pip install pyqt5
if errorlevel 1 (
    echo Failed to install PyQt5
    pause
    exit /b 1
)

echo Installing rembg...
pip install rembg
if errorlevel 1 (
    echo Failed to install rembg
    pause
    exit /b 1
)

echo Installing Pillow...
pip install pillow
if errorlevel 1 (
    echo Failed to install Pillow
    pause
    exit /b 1
)

echo All packages installed successfully!
pause