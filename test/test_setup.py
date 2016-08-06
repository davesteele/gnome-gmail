
import subprocess
import pytest


@pytest.mark.parametrize("interpreter", ("python2.7", "python3"))
def test_setup_dry_run(interpreter):
    cmd = "%s setup.py --dry-run install" % interpreter
    assert 0 == subprocess.call(cmd.split())
