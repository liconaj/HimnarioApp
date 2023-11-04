@echo off
for /f "tokens=2 delims=:." %%x in ('chcp') do set cp=%%x
chcp 1252>nul

set APP_NAME=Himnario Adventista
set APP_EXECUTABLE=Himnario.exe

set WORKING_DIR=%~dp0
set WORKING_DIR=%WORKING_DIR:~0,-1%
set SHORTCUT_NAME=%WORKING_DIR%\%APP_NAME%.lnk
set TARGET_PATH=%WORKING_DIR%\Program\%APP_EXECUTABLE%

echo Set WshShell = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo Set shortcut = WshShell.CreateShortcut("%SHORTCUT_NAME%") >> CreateShortcut.vbs
echo shortcut.TargetPath = "%TARGET_PATH%" >> CreateShortcut.vbs
echo shortcut.WorkingDirectory = "%WORKING_DIR%" >> CreateShortcut.vbs
echo shortcut.Description = "%APP_NAME%" >> CreateShortcut.vbs
echo shortcut.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs

REM Copiar acceso directo al menu de inicio y al escritorio
copy "%SHORTCUT_NAME%" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\%APP_NAME%.lnk"
copy "%SHORTCUT_NAME%" "%USERPROFILE%\Desktop\%APP_NAME%.lnk"

chcp %cp%>nul