#!/usr/bin/env python
# -*- coding: utf-8 -*

# standard library
import os

# external libraries
from fabric.api import put, sudo, settings, cd

zinstance_dir = '/usr/local/Plone/zinstance'


def update_nginx_conf():
    put('hmc.csuohio.edu.conf',
        '/etc/nginx/sites-available/hmc.csuohio.edu.conf', use_sudo=True)
    with settings(warn_only=True):
        sudo('ln -s /etc/nginx/sites-available/hmc.csuohio.edu.conf ' +
             '/etc/nginx/sites-enabled/hmc.csuohio.edu.conf')
    sudo('/etc/init.d/nginx restart')


def plonectl(arg):
    """Start, stop, restart."""
    plonectl = os.path.join(zinstance_dir, 'bin/plonectl')
    sudo('{} {}'.format(plonectl, arg), user='plone_daemon')


def push_buildout_files():
    file_names = os.listdir(os.path.split(__file__)[0])
    cfg_file_names = [f for f in file_names if f.endswith('.cfg') and not
                      f.startswith('.')]
    for file_name in cfg_file_names:
        file_path_on_server = os.path.join(zinstance_dir, file_name)
        # TODO : change this put to rsync
        put(file_name, file_path_on_server, use_sudo=True)
        sudo('chown plone_buildout:plone_group {}'.format(file_path_on_server))
        sudo('chmod go-rw {}'.format(file_path_on_server))
        if file_name == 'buildout.cfg':
            sudo('chmod u+rw {}'.format(file_path_on_server))
        else:
            sudo('chmod u+w {}'.format(file_path_on_server))
            sudo('chmod ugo+r {}'.format(file_path_on_server))


def buildout(args=''):
    plonectl('stop')
    with cd(zinstance_dir):
        sudo('bin/buildout {}'.format(args), user='plone_buildout')
    plonectl('start')
