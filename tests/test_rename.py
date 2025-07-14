import os
import tempfile
from rename import rename_extensionless_files

def create_file(path, content=b''):
    with open(path, 'wb') as f:
        f.write(content)

def test_rename_extensionless_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create extensionless hex file
        fname1 = '00000001'
        fpath1 = os.path.join(tmpdir, fname1)
        create_file(fpath1)
        # Create extensionless non-hex file
        fname2 = 'abcdefgh'
        fpath2 = os.path.join(tmpdir, fname2)
        create_file(fpath2)
        # Create file with extension
        fname3 = '00000002.app'
        fpath3 = os.path.join(tmpdir, fname3)
        create_file(fpath3)

        renamed = rename_extensionless_files(tmpdir)
        # Only the hex file should be renamed
        assert len(renamed) == 1
        old_path, new_path = renamed[0]
        assert old_path == fpath1
        assert new_path == fpath1 + '.app'
        assert not os.path.exists(fpath1)
        assert os.path.exists(fpath1 + '.app')
        # Non-hex and already extended files should remain
        assert os.path.exists(fpath2)
        assert os.path.exists(fpath3)
