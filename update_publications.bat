@echo off
echo Google Scholar Publication Updater
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found. Starting publication update...
echo.

REM Try to run the scholarly fetcher first
echo Attempting to fetch publications from Google Scholar...
python scholar_fetcher.py

if errorlevel 1 (
    echo.
    echo Automated fetching failed. Trying CSV method...
    echo.
    
    REM Check if CSV file exists
    if exist publications.csv (
        echo Found publications.csv, processing...
        python update_publications.py
    ) else (
        echo.
        echo No publications.csv found.
        echo.
        echo To update your publications manually:
        echo 1. Go to https://scholar.google.es/citations?user=bsDDtYYAAAAJ
        echo 2. Click Export ^> CSV
        echo 3. Save as publications.csv in this directory
        echo 4. Run this script again
        echo.
    )
)

echo.
echo Publication update complete!
echo Check the _publications directory for new files.
pause
