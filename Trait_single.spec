# -*- mode: python -*-
from kivy.deps import sdl2, glew

block_cipher = None


a = Analysis(['src\\main.py'],
             pathex=['.'],
             binaries=[],
             datas=[('json', 'json'), ('assets\\Trait_hd.png', 'assets'), ('assets\\Trait_hd_action.png', 'assets')],
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
          name='Trait',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='assets\\Trait.ico')
