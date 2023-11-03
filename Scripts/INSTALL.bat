@echo off

set APP_NAME=Himnario Adventista
set APP_EXECUTABLE=Himnario.exe

REM Crear acceso directo en el escritorio
set SHORTCUT_NAME=%USERPROFILE%\Desktop\%APP_NAME%.lnk
set WORKING_DIR=%~dp0
set WORKING_DIR=%WORKING_DIR:~0,-1%
set TARGET_PATH=%WORKING_DIR%\%APP_EXECUTABLE%

echo Set WshShell = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo Set shortcut = WshShell.CreateShortcut("%SHORTCUT_NAME%") >> CreateShortcut.vbs
echo shortcut.TargetPath = "%TARGET_PATH%" >> CreateShortcut.vbs
echo shortcut.WorkingDirectory = "%WORKING_DIR%" >> CreateShortcut.vbs
echo shortcut.Description = "%APP_NAME%" >> CreateShortcut.vbs
echo shortcut.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs

REM Copiar acceso directo al menu de inicio
copy "%SHORTCUT_NAME%" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\%APP_NAME%.lnk"
