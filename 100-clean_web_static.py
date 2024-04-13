#!/usr/bin/python3
'''clean up old versions of web_static'''
from fabric.api import run, env, local, task
from datetime import datetime
from os import path

env.hosts = ['3.90.84.154', '35.174.204.42']

@task
def do_clean(number=0):
    '''clean up old versions of web_static'''
    number = int(number)
    if number < 2:
        number = 1
    else:
        number += 1
    local("ls -t versions | tail -n +{} | xargs rm -rf".format(number))
    run("ls -t /data/web_static/releases | tail -n +{} | xargs rm -rf".format(number))
