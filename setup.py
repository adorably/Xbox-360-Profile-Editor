from distutils.core import setup
import py2exe, sys

sys.argv.append('py2exe')

# For compiling to a portable executable.

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows = [{'script': "main.py"}],
    zipfile = None,
)