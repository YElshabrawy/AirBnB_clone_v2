#!/usr/bin/python3
"""Package initializer"""
import os
# from dotenv import load_dotenv
# load_dotenv()

HBNB_TYPE_STORAGE = os.getenv('HBNB_TYPE_STORAGE')

if HBNB_TYPE_STORAGE == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
