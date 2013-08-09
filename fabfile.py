#!/usr/bin/env python
# -*- coding: utf-8 -*

from fabric.api import put, sudo, settings


def update_nginx_conf():
    put('hmc.csuohio.edu.conf',
        '/etc/nginx/sites-available/hmc.csuohio.edu.conf', use_sudo=True)
    with settings(warn_only=True):
        result = sudo('ln -s /etc/nginx/sites-available/hmc.csuohio.edu.conf /etc/nginx/sites-enabled/hmc.csuohio.edu.conf')
    sudo('/etc/init.d/nginx restart')

def plonectl(arg):
    """Start, stop, restart."""
    sudo('/usr/local/Plone/zinstance/bin/plonectl {}'.format(arg), user='plone_daemon')
