import os
import sys
import subprocess

ARCHITECTURE = "x64"
if len(sys.argv) > 1:
    ARCHITECTURE = sys.argv[1]

CWD = os.getcwd().replace("\\", "/")
PYTHON_EXE_PATH = "C:/Program Files/Python311/python.exe"
MSVC = "C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build/vcvarsall.bat"

metadata = dict()
fhandler = open("metadata.txt", "r", encoding="utf-8")
for line in fhandler:
    item = line.strip().split("=")
    key = item[0].strip()
    value = item[1].strip()
    metadata[key] = value
fhandler.close()

if os.path.exists("Dist/Program"):
    os.system("rmdir /s /q Dist\\Program")

command = '"{}" {}&'.format(MSVC, ARCHITECTURE)
command += '"{}" -m nuitka '.format(PYTHON_EXE_PATH)
command += '--standalone --disable-console '
command += '--output-dir="{}/Dist" '.format(CWD)
command += '--remove-output '
command += '--output-filename="{}" '.format(metadata["filename"])
command += '--enable-plugin=tk-inter '
command += '--force-stderr-spec=logs.log '
command += '--force-stdout-spec=logs.log '
command += '--product-version={} '.format(metadata["version"])
command += '--company-name="{}" '.format(metadata["company"])
command += '--product-name="{}" '.format(metadata["name"])
command += '--windows-icon-from-ico="{}" '.format(metadata["icon-windows"])
command += '--file-description="{}" '.format(metadata["description"])
command += '--copyright="{}" '.format(metadata["copyright"])
# command += '--include-data-files=DATAPATH=DATAPATH '
command += '--main="{}" &'.format("main.py")
command += 'move "Dist/main.dist" "Dist/Program"'

os.system(f"cmd /c {command}")

if os.path.exists("Dist/Program"):
    with open("Dist/Program/DATAPATH", "w", encoding="utf-8") as f:
        f.write("../Data\n")
