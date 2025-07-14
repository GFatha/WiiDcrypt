import os
import tempfile
import shutil
import pytest
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from wiiman.folder_validator import is_valid_cdn_file

def create_file(path, content=b''):
    with open(path, 'wb') as f:
        f.write(content)

def test_valid_cdn_file_types():
    with tempfile.TemporaryDirectory() as tmpdir:
        for ext in ['.app', '.tmd', '.tik', '.cert', '.h3']:
            fname = f'file{ext}'
            fpath = os.path.join(tmpdir, fname)
            create_file(fpath)
            assert is_valid_cdn_file(fname, tmpdir)

def test_alternate_tmd():
    with tempfile.TemporaryDirectory() as tmpdir:
        fname = 'tmd.0'
        fpath = os.path.join(tmpdir, fname)
        create_file(fpath)
        assert is_valid_cdn_file(fname, tmpdir)
        fname2 = 'tmd.123'
        fpath2 = os.path.join(tmpdir, fname2)
        create_file(fpath2)
        assert is_valid_cdn_file(fname2, tmpdir)

def test_valid_no_extension_hex():
    with tempfile.TemporaryDirectory() as tmpdir:
        fname = '00000001'
        fpath = os.path.join(tmpdir, fname)
        create_file(fpath)
        assert is_valid_cdn_file(fname, tmpdir)

def test_invalid_no_extension_nonhex():
    with tempfile.TemporaryDirectory() as tmpdir:
        fname = 'abcdefgh'
        fpath = os.path.join(tmpdir, fname)
        create_file(fpath)
        assert not is_valid_cdn_file(fname, tmpdir)

def test_invalid_extension():
    with tempfile.TemporaryDirectory() as tmpdir:
        fname = 'file.txt'
        fpath = os.path.join(tmpdir, fname)
        create_file(fpath)
        assert not is_valid_cdn_file(fname, tmpdir)

def test_file_does_not_exist():
    with tempfile.TemporaryDirectory() as tmpdir:
        assert not is_valid_cdn_file('missing.app', tmpdir)
        assert not is_valid_cdn_file('tmd.0', tmpdir)
        assert not is_valid_cdn_file('00000001', tmpdir)
