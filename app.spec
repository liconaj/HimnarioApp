# -*- mode: python -*-

block_cipher = None
file_name = "HimnarioApp"
add_files = []

a = Analysis(['main.py', 'finder.py', 'music.py','player.py','settings.py'],
    pathex=['C:\Users\josue\AppData\Roaming\Python\Python311\Scripts'],
    binaries=[],
    datas=add_files,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=file_name,
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )