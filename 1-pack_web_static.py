#!/usr/bin/python3
'''creates a .tgz archive from the contents of the web_static folder'''
from fabric.api import local
from datetime import datetime


def do_pack():
    '''packs up all files from web_static into a .tgz archive'''
    filename = f"web_static_{datetime.now().strftime('%Y%m%d%H%M%S')}.tgz"
    local("mkdir -p versions")
    compressed = local(f"tar -cvzf versions/{filename} web_static")
    return f"versions/{filename}" if compressed.succeeded else None
