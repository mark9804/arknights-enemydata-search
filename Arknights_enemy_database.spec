# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['C:\\Users\\Mark\\Desktop\\各种小工具\\arknights\\Arknights_enemy_database\\Arknights_enemy_database.py'],
             pathex=['C:\\Users\\Mark\\Desktop\\各种小工具\\arknights\\Arknights_enemy_database'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          name='Arknights_enemy_database',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='C:\\Users\\Mark\\Desktop\\各种小工具\\arknights\\Arknights_enemy_database\\RHODES_ISLAND_ICON.ico')
