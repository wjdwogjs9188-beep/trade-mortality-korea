@echo off
REM Document Converter GUI launcher (PDF / DOCX / XLSX / XLS / MD)
REM Double-click to run.
pushd "%~dp0"
python 2_scripts\utils\pdf_to_docx_gui.py
if errorlevel 1 (
 echo.
 echo *** Error: required libs not installed?
 echo Run: pip install pdf2docx==0.5.8 mammoth==1.8.0 pandas openpyxl xlrd
 echo.
 pause
)
popd
