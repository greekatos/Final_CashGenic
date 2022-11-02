a = Analysis(['main.py'],
             pathex=['.'],
             binaries=[],
             datas=[('data\\*.tsv', 'data')],
             hiddenimports=['sklearn.neighbors.typedefs','sklearn.neighbors.quad_tree','sklearn.tree._utils','boto',
             'smart_open'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='xyz',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='favicon.ico', version='Resources.rc')