from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'packages': ['rumps', 'datetime', 'pyperclip', 'keyring', 'http', 'json', 'hashlib'],
    'plist': {
        'LSUIElement': False,
    },
}

setup(
    app=APP,
    
    name="ZeroTier Cortana",
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)