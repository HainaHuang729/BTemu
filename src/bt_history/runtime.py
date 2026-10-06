"""Confine 21cmFAST import-time configuration IO to an absent private config."""
import importlib
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

def import_native(root):
    sys.path.insert(0,str(root))
    original=Path.expanduser
    # This only redirects the import-time user cache config. Physics source is unmodified.
    with TemporaryDirectory(prefix='bt_history_config_') as scratch:
        def expand(path):
            return Path(scratch)/'absent.yml' if str(path)=='~/.21cmfast/config.yml' else original(path)
        with patch.object(Path,'expanduser',expand):
            native=importlib.import_module('py21cmfast.c_21cmfast')
    return native
