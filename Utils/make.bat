@echo off
for /f "tokens=2 delims=:." %%x in ('chcp') do set cp=%%x
chcp 1252>nul

nuitka src/main.py -o Himnario.exe^
    --standalone^
    --disable-console^
    -–windows-dependency-tool=pefile^
    -–experimental=use_pefile_recurse^
    -–experimental=use_pefile_fullrecurse^
    --force-stderr-spec="%%PROGRAM_BASE%%.err.txt"^
    --enable-plugin=tk-inter^
    --product-version="0.1.0"^
    --company-name="Liconaj"^
    --product-name="Himnario Adventista"^
    --windows-icon-from-ico=dist/Data/icon.ico^
    --file-description="Himnario Iglesia Adventista del Séptimo Día Letra y Música"^
    --copyright="© 2023 Josué Licona"^
    --jobs=8


chcp %cp%>nul