@echo off
title Hospital Readmission Analysis - Running All Scripts
color 0A

echo ============================================================
echo   HOSPITAL READMISSION ANALYSIS - DACS08 Portfolio Project
echo   Running All Python Scripts
echo ============================================================
echo.

set "PROJECT=C:\Users\hariv\Downloads\files\hospital_project"
set PYTHONUTF8=1

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python from https://python.org
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if cleaned data exists - if not, run Phase 1 & 2 first
if not exist "%PROJECT%\diabetic_data_cleaned.csv" (
    echo [STEP 1/4] Running Phase 1 and 2: Data Understanding and Cleaning...
    python "%PROJECT%\phase1_2_eda.py"
    if errorlevel 1 goto :error
    echo [DONE] Phase 1 and 2 complete!
) else (
    echo [SKIP] Cleaned dataset already exists - skipping Phase 1 and 2
)

echo.
echo [STEP 2/4] Running Phase 3 and 4: EDA - 10 Questions + Medium Analysis...
python "%PROJECT%\phase3_4_eda.py"
if errorlevel 1 goto :error
echo [DONE] Phase 3 and 4 complete!

echo.
echo [STEP 3/4] Running Phase 5: Machine Learning + Patient Clustering...
echo This may take 2-5 minutes...
python "%PROJECT%\phase5_advanced.py"
if errorlevel 1 goto :error
echo [DONE] Phase 5 complete!

echo.
echo [STEP 4/4] Generating Summary Dashboard Charts...
python "%PROJECT%\generate_summary_charts.py"
if errorlevel 1 goto :error
echo [DONE] Summary charts complete!

echo.
echo ============================================================
echo   ALL SCRIPTS COMPLETED SUCCESSFULLY!
echo ============================================================
echo.
echo Output files:
echo   - Cleaned data : %PROJECT%\diabetic_data_cleaned.csv
echo   - All charts   : %PROJECT%\plots\
echo   - Key results  : %PROJECT%\plots\model_metrics.csv
echo   - Segments     : %PROJECT%\plots\patient_segments.csv
echo.

REM Open the plots folder automatically
echo Opening plots folder...
explorer "%PROJECT%\plots"

echo.
echo Press any key to exit...
pause >nul
exit /b 0

:error
echo.
echo [ERROR] A script failed. Check the error message above.
echo.
pause
exit /b 1
