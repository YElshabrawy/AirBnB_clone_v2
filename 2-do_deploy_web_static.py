#!/usr/bin/python3
'''m'''
import os
from fabric.api import put, run, env, task, local
from datetime import datetime

env.user = "ubuntu"
env.hosts = ['54.236.207.221', '3.89.146.24']


@task
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


@task
def do_deploy(archive_path):
    '''deploy to web server'''
    if not os.path.isfile(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')
        archive_name = os.path.basename(archive_path)
        folder_name = archive_name.split('.')[0]
        release_path = "/data/web_static/releases/{}/".format(folder_name)

        run(f'mkdir -p {release_path}')
        run(f'tar -xzf /tmp/{archive_name} -C {release_path}')
        run(f'rm /tmp/{archive_name}')
        run(f'mv {release_path}web_static/* {release_path}')
        run(f'rm -rf {release_path}web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s -f {release_path} /data/web_static/current')
        return True
    except Exception:
        return False
