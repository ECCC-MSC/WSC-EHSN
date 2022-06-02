# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['1_ElectronicFieldNotes.py'],
             pathex=['env\\Lib', '.'],
             binaries=[],
             datas=[
                 ('icon_transparent.png', '.'),
                 ('WSC_EHSN.xsml', '.'),
                 ('WSC_EHSN_Summary.xsml', '.'),
                 ('WSC_EHSN_VIEW.xsml', '.'),
                 ('icon_transparent.ico', '.'),
                 ('icon.ico', '.'),
                 ('downarrow.png', '.'),
                 ('backarrow.png', '.'),
                 ('icon_transparent.jpg', '.'),
                 ('config.xml', '.')],
             hiddenimports=['common'],
             hookspath=[],
             hooksconfig={},
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
          name='WSC_eHSN_v2_3_1',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='icon.ico')
