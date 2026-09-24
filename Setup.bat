@echo off&setlocal

:: Edit these if needed to point towards the correct location for your system
:: Make sure not to insert any spaces around the equals sign
set "KSP_GameData_Folder=C:\Steam\steamapps\common\Kerbal Space Program\GameData"
set "Texconv_Path=C:\Program Files\Texconv\texconv.exe"

where python > nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python was not found in your system's PATH.
    echo Please install python, or if it is installed, add it to the PATH system environmental variable.
    pause
    exit /b
)

for /f "delims=" %%f in ('dir "%~dp0Data" /ad /b') do (
    python "%~dp0AutoPatcher\auto_patcher.py" --mod-name="%%f" --gamedata-folder="%KSP_GameData_Folder%" --texconv-path="%Texconv_Path%"
)

IF %ERRORLEVEL% NEQ 0 (
    PAUSE
) ELSE (
    ping 192.0.2.0 -n 2 -w 500>nul
)
