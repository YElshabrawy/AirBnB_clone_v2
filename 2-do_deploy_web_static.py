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


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    file_name = archive_path.split('/')[-1].split('.')[0]
    if not os.path.exists(archive_path):
        return False

    put(archive_path, '/tmp/')
    run(f'mkdir -p /data/web_static/releases/{file_name}/')
    run(f'tar -xzf /tmp/{file_name}.tgz -C /data/web_static/releases/{file_name}/')
    run(f'rm /tmp/{file_name}.tgz')
    run(f'mv /data/web_static/releases/{file_name}/web_static/* \
    /data/web_static/releases/{file_name}/')
    run(f'rm -rf /data/web_static/releases/{file_name}/web_static')
    run('rm -rf /data/web_static/current')
    run(f'ln -s /data/web_static/releases/{file_name}/ \
    /data/web_static/current')
    print('New version deployed!')
    return True
