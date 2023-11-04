@echo off
for /f "tokens=2 delims=:." %%x in ('chcp') do set cp=%%x
chcp 1252>nul

set APP_NAME=Himnario Adventista
set START_MENU_SHORTCUT="%APPDATA%\Microsoft\Windows\Start Menu\Programs\%APP_NAME%.lnk"
set DESKTOP_SHORTCUT="%USERPROFILE%\Desktop\%APP_NAME%.lnk"

if exist %START_MENU_SHORTCUT% del %START_MENU_SHORTCUT%
if exist %DESKTOP_SHORTCUT% del %DESKTOP_SHORTCUT%

chcp %cp%>nul