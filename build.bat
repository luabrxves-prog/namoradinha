@echo off
setlocal
cd /d %~dp0

echo ==========================================
echo   Gerando NossoQuiz.exe ^<3
echo ==========================================

where py >nul 2>nul
if %errorlevel%==0 (
    set PYTHON=py
) else (
    set PYTHON=python
)

%PYTHON% -m pip install -r requirements.txt
if errorlevel 1 goto :erro

%PYTHON% -m PyInstaller --noconfirm --clean --onefile --windowed --name NossoQuiz main.py
if errorlevel 1 goto :erro

echo.
echo Pronto! O executavel esta em:
echo %cd%\dist\NossoQuiz.exe
echo.
pause
exit /b 0

:erro
echo.
echo Nao foi possivel gerar o executavel.
echo Verifique se o Python esta instalado e tente novamente.
pause
exit /b 1
