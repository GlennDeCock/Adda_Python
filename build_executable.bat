@echo off
REM ===================================================================
REM Build AddAttachment Executable
REM This script creates a standalone .exe file for non-technical users
REM ===================================================================

echo.
echo ============================================
echo  Building AddAttachment Executable
echo ============================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ERROR: PyInstaller is not installed!
    echo.
    echo Please install it by running:
    echo   pip install pyinstaller
    echo.
    echo Or if using conda:
    echo   conda install -c conda-forge pyinstaller
    echo.
    pause
    exit /b 1
)

REM Clean previous build
echo [1/4] Cleaning previous build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo       Done!
echo.

REM Build the executable
echo [2/4] Building executable with PyInstaller...
echo       This may take a few minutes...
pyinstaller AddAttachment_Main.spec --clean

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)
echo       Done!
echo.

REM Check if build was successful
if exist "dist\AddAttachment_Main.exe" (
    echo [3/4] Copying required files...
    REM Copy conf.yaml if not already included
    if exist conf.yaml copy conf.yaml dist\
    echo       Done!
    echo.
    
    echo [4/4] Build completed successfully!
    echo.
    echo ============================================
    echo  SUCCESS!
    echo ============================================
    echo.
    echo Your executable is ready at:
    echo   %cd%\dist\AddAttachment_Main.exe
    echo.
    echo File size: 
    dir dist\AddAttachment_Main.exe | find "AddAttachment_Main.exe"
    echo.
    echo You can now distribute the "dist" folder to users.
    echo Make sure conf.yaml is in the same folder as the .exe
    echo.
) else (
    echo [3/4] ERROR: Executable not found after build!
    echo       Build may have failed. Check errors above.
    echo.
)

echo.
echo Press any key to open the dist folder...
pause >nul
explorer dist

exit /b 0
