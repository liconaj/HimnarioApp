@echo off
for /f "tokens=2 delims=:." %%x in ('chcp') do set cp=%%x
chcp 1252>nul

set APP_NAME=Himnario Adventista
set APP_EXECUTABLE=Program\Himnario.exe
set WORKING_DIR=%CD%\Dist
set SHORTCUT_NAME=%WORKING_DIR%\%APP_NAME%.lnk
set TARGET_PATH=%WORKING_DIR%\%APP_EXECUTABLE%

if exist %SHORTCUT_NAME% del %SHORTCUT_NAME%

echo Set WshShell = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo Set shortcut = WshShell.CreateShortcut("%SHORTCUT_NAME%") >> CreateShortcut.vbs
echo shortcut.TargetPath = "%TARGET_PATH%" >> CreateShortcut.vbs
echo shortcut.WorkingDirectory = "%WORKING_DIR%" >> CreateShortcut.vbs
echo shortcut.Description = "%APP_NAME%" >> CreateShortcut.vbs
echo shortcut.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs

chcp %cp%>nul