#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import join
from fabric.api import env, task
from fagungis.tasks import *


@task
def example():
    #  name of your project - no spaces, no special chars
    env.project = 'example_production'
    #  hg repository of your project
    env.repository = 'https://bitbucket.org/DNX/example'
    #  hosts to deploy your project, users must be sudoers
    env.hosts = ['root@192.168.1.1', ]
    # additional packages to be installed on the server
    env.additional_packages = [
        'mercurial',
    ]
    #  system user, owner of the processes and code on your server
    #  the user and it's home dir will be created if not present
    env.django_user = 'django'
    # user group
    env.django_user_group = env.django_user
    #  the code of your project will be located here
    env.django_user_home = join('/opt', env.django_user)
    #  projects path
    env.projects_path = join(env.django_user_home, 'projects')
    #  the root path of your project
    env.code_root = join(env.projects_path, env.project)
    #  the path where manage.py and settings.py of this project is located
    env.django_project_root = join(env.code_root, 'sites', 'prod')
    #  django media dir
    env.django_media_path = join(env.code_root, 'media')
    #  django static dir
    env.django_static_path = join(env.code_root, 'static')
    #  django media url and root dir
    env.django_media_url = '/site_media/media/'
    env.django_media_root = env.code_root
    #  django static url and root dir
    env.django_static_url = '/site_media/static/'
    env.django_static_root = env.code_root
    #  do you use south in your django project?
    env.south_used = False
    #  virtualenv root
    env.virtenv = join(env.django_user_home, 'envs', env.project)
    #  some virtualenv options, must have at least one
    env.virtenv_options = ['distribute', 'no-site-packages', ]
    #  always ask user for confirmation when run any tasks
    env.ask_confirmation = True

    ### START gunicorn settings ###
    #  be sure to not have anything running on that port
    env.gunicorn_bind = "127.0.0.1:8100"
    env.gunicorn_logfile = '%(django_user_home)s/logs/projects/%(project)s_gunicorn.log' % env
    env.rungunicorn_script = '%(django_user_home)s/scripts/rungunicorn_%(project)s.sh' % env
    env.gunicorn_workers = 2
    env.gunicorn_worker_class = "eventlet"
    env.gunicorn_loglevel = "info"
    ### END gunicorn settings ###

    ### START nginx settings ###
    env.nginx_server_name = 'example.com'  # Only domain name, without 'www' or 'http://'
    env.nginx_conf_file = '%(django_user_home)s/configs/nginx/%(project)s.conf' % env
    env.nginx_client_max_body_size = 10  # Maximum accepted body size of client request, in MB
    env.nginx_htdocs = '%(django_user_home)s/htdocs' % env
    ### END nginx settings ###

    ### START supervisor settings ###
    env.supervisorctl = '/usr/bin/supervisorctl'  # supervisorctl script
    env.supervisor_autostart = 'true'  # true or false
    env.supervisor_autorestart = 'true'  # true or false
    env.supervisor_redirect_stderr = 'true'  # true or false
    env.supervisor_stdout_logfile = '%(django_user_home)s/logs/projects/supervisord_%(project)s.log' % env
    env.supervisord_conf_file = '%(django_user_home)s/configs/supervisord/%(project)s.conf' % env
    ### END supervisor settings ###
