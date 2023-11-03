import os

arch = "x64"

main_module = "src/main.py"

output_dir = "dist"
output = f"{output_dir}\\main.dist"
dist = f"{output_dir}\\Himnario_{arch}"

metadata = dict()
fhandler = open("metadata.txt", "r", encoding="utf-8")
for line in fhandler:
    item = line.strip().split("=")
    key = item[0].strip()
    value = item[1].strip()
    metadata[key] = value
fhandler.close()

with open("VERSION", "r", encoding="utf-8") as fversion:
    version = fversion.readline()
    metadata["product-version"] = version.strip()
    fversion.close()

# --include-data-dir=assets/Data=Data
parameters = f"""
    --standalone
    --disable-console
    --remove-output
    --output-dir={output_dir}
    --force-stderr-spec=logs.err.txt
    --enable-plugin=tk-inter
    --output-filename="{metadata["output-filename"]}"
    --product-version="{metadata["product-version"]}"
    --company-name="{metadata["company-name"]}"
    --product-name="{metadata["product-name"]}"
    --windows-icon-from-ico={metadata["icon-windows"]}
    --file-description="{metadata["file-description"]}"
    --copyright="{metadata["copyright"]}"
    --include-data-files=VERSION=VERSION
    --jobs=6
"""

parameters = " ".join([p.strip() for p in parameters.split("\n")])
cmd = f"cmd /c nuitka {main_module} {parameters}"
os.system(cmd)
os.system(f"if exist {dist} rmdir /s /q {dist}")
os.system(f"if exist {output} move {output} {dist}")

# os.system(cmd)
# os.system(f"rm")
# os.system(f"xcopy /y /s /i {output} {dist}")
# os.system(f"rmdir /s /q {output}")
