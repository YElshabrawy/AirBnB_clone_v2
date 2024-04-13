#!/usr/bin/python3
'''clean up old versions of web_static'''
from fabric.api import run, env, local, task
from datetime import datetime
from os import path

env.hosts = ['3.90.84.154', '35.174.204.42']

@task
def do_pack():
    '''packs up all files from web_static into a .tgz archive'''
    filename = f"web_static_{datetime.now().strftime('%Y%m%d%H%M%S')}.tgz"
    local("mkdir -p versions")
    compressed = local(f"tar -cvzf versions/{filename} web_static")
    return f"versions/{filename}" if compressed.succeeded else None


@task
def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    file_name = archive_path.split('/')[-1].split('.')[0]
    if not path.exists(archive_path):
        return False

    put(archive_path, '/tmp/')
    run(f'mkdir -p /data/web_static/releases/{file_name}/')
    run(f'tar -xzf /tmp/{file_name}.tgz -C \
    /data/web_static/releases/{file_name}/')
    run(f'rm /tmp/{file_name}.tgz')
    run(f'mv /data/web_static/releases/{file_name}/web_static/* \
    /data/web_static/releases/{file_name}/')
    run(f'rm -rf /data/web_static/releases/{file_name}/web_static')
    run('rm -rf /data/web_static/current')
    run(f'ln -s /data/web_static/releases/{file_name}/ \
    /data/web_static/current')
    print('New version deployed!')
    return True


@task
def deploy():
    """creates and distributes an archive to the web servers"""
    archive = do_pack()
    if not archive:
        return False
    return do_deploy(archive)


@task
def do_clean(number=0):
    '''clean up old versions of web_static'''
    try:
        number = int(number)
        if number < 0:
            return False
        if number == 0 or number == 1:
            number = 1
        local(f'cd versions; ls -t | tail -n +{number} | xargs rm -rf --')
        for host in env.hosts:
            env.host_string = host
            run(f'cd /data/web_static/releases; ls -t | tail -n +{number} | xargs rm -rf --')
        return True
    except Exception as e:
        return False
