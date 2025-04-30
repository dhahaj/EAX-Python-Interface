# -*- mode: python ; coding: utf-8 -*-
import telemetrix_aio
import os

telemetrix_aio_path = os.path.dirname(telemetrix_aio.__file__)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('util/resources.py', '.'),
        ('util', 'util'),
        ('config_loader.py', '.'), 
        ('imports.py', '.'), 
        ('ui', 'ui'), 
        ('resource_rc.py', '.'), 
        ('icons_rc.py', '.'), 
        ('arduino.py', '.'), 
        ('settings.py', '.'), 
        ('applogger.py', '.'), 
        ('constants.py', '.'), 
        ('device.py', '.'), 
        ('settings.py', '.'), 
        ('main.py', '.'),
        ('globals.py', '.'),
        (telemetrix_aio_path, 'telemetrix_aio'),
    ],
    hiddenimports=[
        'qdarkstyle', 
        'qtpy.QtCore', 
        'qtpy', 
        'yaml', 
        'loguru', 
        'sqlite3', 
        'bcrypt', 
        'shutil',
        'serial',
        'serial.serialutil',
        'serial.tools.list_ports',
        ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='EAXInterface',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    hide_console='minimize-early',
)
