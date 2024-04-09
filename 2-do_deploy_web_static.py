#!/usr/bin/python3
'''deploy packed web_static to web servers'''
from os import path
from fabric.api import put, run, env

env.hosts = ['3.90.84.154', '35.174.204.42']
env.user = 'ubuntu'


def do_deploy(archive_path):
    '''deploy to web server'''
    if not path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        filename_ext = archive_path.split('/')[-1]
        filename = filename_ext.split('.')[0]
        run(f'mkdir -p /data/web_static/releases/{filename}/')
        run(f"tar -xzf /tmp/{filename_ext} \
            -C /data/web_static/releases/{filename}/")
        run(f"rm /tmp/{filename_ext}")
        run(f"mv /data/web_static/releases/{filename}/web_static/* \
            /data/web_static/releases/{filename}/")
        run(f"rm -rf /data/web_static/releases/{filename}/web_static")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -s /data/web_static/releases/{filename}/ \
            /data/web_static/current")
        print('New version deployed!')
        return True
    except Exception as e:
        return False
