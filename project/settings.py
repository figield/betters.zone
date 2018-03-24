import os
from pathlib import Path


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
debug_file = Path(BASE_DIR + '/debug')
secret_file = Path(BASE_DIR + '/secret_key')
if secret_file.is_file() and not debug_file.is_file():
    with secret_file.open() as f:
        SECRET_KEY = f.read().strip()
    from project.production import *
else:
    SECRET_KEY = 'SECRET_KEY'
    print("Running project in debug mode...")
    from project.debug import *
