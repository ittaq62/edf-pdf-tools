# -*- mode: python ; coding: utf-8 -*-
# Configuration PyInstaller de EDF PDF Tools.
# Build : python build.py (genere splash.png puis lance PyInstaller sur ce fichier)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # Bibliotheques tirees par des dependances optionnelles mais inutilisees ici :
    # les exclure allege l'executable et accelere son extraction au lancement
    excludes=['numpy', 'lxml', 'psutil', 'charset_normalizer'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

splash = Splash(
    'splash.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=(20, 240),
    text_size=9,
    text_color='#888888',
    text_default='Chargement...',
    always_on_top=False,
)

exe = EXE(
    pyz,
    a.scripts,
    splash,
    splash.binaries,
    a.binaries,
    a.datas,
    [],
    name='EDF_PDF_Tools',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['Logo-EDF.png'],
)
