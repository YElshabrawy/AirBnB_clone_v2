#!/usr/bin/python3
'''Deploy a compressed tar archive of web_static to web servers'''

import os
from fabric.api import put, run, env, task, local
from datetime import datetime

env.user = "ubuntu"
env.hosts = ['54.236.207.221', '3.89.146.24']


@task
def do_pack():
    """Compress web_static directory"""
    try:
        now = datetime.now()
        dt_format = now.strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_{}.tgz".format(dt_format)
        local("mkdir -p versions")
        local("tar -cvzf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except Exception as e:
        return None


@task
def do_deploy(archive_path):
    """Distribute archive to web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        folder_name = archive_name.split('.')[0]
        release_path = "/data/web_static/releases/{}/".format(folder_name)

        put(archive_path, '/tmp/')
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_name, release_path))
        run("rm /tmp/{}".format(archive_name))
        run("mv {}web_static/* {}".format(release_path, release_path))
        run("rm -rf {}web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))
        print("New version deployed!")
        return True
    except Exception as e:
        return False
