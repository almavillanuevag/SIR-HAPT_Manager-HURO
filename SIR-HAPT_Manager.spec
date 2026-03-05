from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path
import os

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[
        ('app.kv', '.'),
        ('sir-hapt-huro-firebase-adminsdk.json', '.'),
        ('logo.ico', '.'),
        ('logo.png', '.'),
    ],
    hiddenimports=['kivymd.icon_definitions'],
    hookspath=[kivymd_hooks_path],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    a.binaries,
    a.zipfiles,
    a.datas,
    name='SIR-HAPT',
    debug=False,
    strip=False,
    upx=True,
    console=False,
    icon='logo.ico',
)