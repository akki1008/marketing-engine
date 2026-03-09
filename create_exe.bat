@echo off
echo Creating executable for Marketing Engine...
echo.

pip install pyinstaller
pyinstaller --onefile --windowed --name MarketingEngine app.py

echo.
echo Executable created! Check the 'dist' folder for MarketingEngine.exe
echo Share this .exe file with your friends - they can run it without installing anything!
echo.
pause