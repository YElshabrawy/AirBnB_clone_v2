#!/usr/bin/python3
"""Fabric script that generates a .tgz
archive from the contents of the
web_static folder of your AirBnB Clone repo"""
from fabric.api import local
from datetime import datetime


def do_pack():
    '''Function to generate a .tgz file'''
    local("mkdir -p versions")
    filename = "versions/web_static_{}.tgz" \
        .format(datetime.now().strftime("%Y%m%d%H%M%S"))
    result = local("tar -cvzf {} web_static".format(filename))
    if result.failed:
        return None
    else:
        return filename
