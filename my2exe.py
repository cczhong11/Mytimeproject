from distutils.core import setup
import py2exe

setup(windows=['my_gui.py'],
      options={
       "py2exe": {
        "excludes": ["six.moves.urllib.parse"]
    }
})