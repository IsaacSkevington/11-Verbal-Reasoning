# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['verbalquestionsetter.py'],
             pathex=['D:\\Users\\SSAPP\\Documents\\code\\Python\\Tim Verbal'],
             binaries=[],
             datas=[('wordData.bin', '.'), ('allwords.bin', '.'), ('commonwords.bin', '.'), ('11+Logo.ico', '.')],
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
          name='11+ Verbal Reasoning Practice',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          icon='11+Logo.ico',
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False)
