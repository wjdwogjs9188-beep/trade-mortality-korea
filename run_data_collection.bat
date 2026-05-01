@echo off
pushd "%~dp0"

echo === Step 0/5: Install packages ===
python -m pip install -r requirements.txt
if errorlevel 1 goto :err

echo.
echo === Step 1/5: ECOS explore ===
python 2_scripts\data_collection\01_ecos_explore.py

echo.
echo === Step 2/5: ECOS household delinquency ===
python 2_scripts\data_collection\02_ecos_household_delinquency.py

echo.
echo === Step 3/5: Comtrade ADH 8 countries ===
python 2_scripts\data_collection\03_comtrade_adh_china.py

echo.
echo === Step 4/5: Comtrade Korea-China bilateral ===
python 2_scripts\data_collection\04_comtrade_korea_china.py

echo.
echo === Step 5/5: Comtrade China-World ===
python 2_scripts\data_collection\05_comtrade_china_world.py

echo.
echo === ALL DONE ===
goto :end

:err
echo.
echo *** ERROR — see above ***
popd
pause
exit /b 1

:end
popd
pause
