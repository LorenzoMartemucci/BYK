# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

a = Analysis(
    ['src/main_interface.py'],
    pathex=['./src'],
    binaries=[],
    datas=[
        ('rsc/*', 'rsc'),
        ('C:/Users/XT144AC/AppData/Roaming/nltk_data/tokenizers/punkt', 'nltk_data/tokenizers/punkt'),
        ('C:/Users/XT144AC/AppData/Roaming/nltk_data/corpora/stopwords', 'nltk_data/corpora/stopwords'),
    ]
    hiddenimports=collect_submodules('transformers') + [
        'sklearn.utils._typedefs',                 # Often needed for sklearn
        'sentence_transformers.models',            # Sentence Transformers
        'torch',
        'transformers',
        'openai'
    ],
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Robbi',
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
    icon=['./rsc/robot_icon.ico'],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Robbi'
)