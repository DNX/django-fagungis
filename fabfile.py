from datetime import datetime
from os.path import join
from fabric.api import env, puts, abort, require, cd, hide
from fabric.operations import sudo, settings, run
from fabric.contrib import console
env.hosts = ['localhost', ]

from fabric.colors import _wrap_with


green_bg = _wrap_with('42')
red_bg = _wrap_with('41')

REPOSITORY = 'ssh://hg@bitbucket.org/DNX/project'
PROVIDING_PROJECT = ('prod', )


def prod():
    #  name of your project - no spaces, no special chars
    env.project = 'project_prod'
    #  hosts to deploy your project, users must be sudoers
    env.hosts = ['root@192.168.1.90', ]
    #  system user, owner of the processes and code on your server
    #  the user and it's home dir will be created if not present
    env.django_user = 'django'
    #  the code of your project will be located here
    env.django_user_home = join('/opt', env.django_user)
    #  the root path of your project
    env.code_root = join(env.django_user_home, 'projects', env.project)
    #  the path where manage.py and settings.py of this project is located
    env.django_project_root = join(env.code_root, 'sites', 'prod')
    #  django media dir
    env.django_media_path = join(env.code_root, 'media')
    #  django sattic dir
    env.django_static_path = join(env.code_root, 'static')
    #  virtualenv root
    env.virtenv = join(env.django_user_home, 'envs', env.project)
    #  always ask user for confirmation when run any tasks
    env.ask_confirmation = True

    ### START gunicorn settings ###
    env.gunicorn_bind = "127.0.0.1:8100"
    env.gunicorn_logfile = '%(django_user_home)s/logs/projects/%(project)s_gunicorn.log' % env
    env.gunicorn_workers = 4
    env.gunicorn_worker_class = "eventlet"
    ### END gunicorn settings ###


def _create_django_user():
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = sudo('useradd -d %(django_user_home)s -m -r %(django_user)s' % env)
        if 'already exists' in res:
            puts('User \'%(django_user)s\' already exists, will not be changed.' % env)
            return
        #  set password
        sudo('passwd %(django_user)s' % env)


def _setup_directories():
    sudo('mkdir -p %(code_root)s' % env)
    sudo('mkdir -p %(django_user_home)s/logs/nginx' % env)
    sudo('mkdir -p %(django_user_home)s/logs/projects' % env)
    sudo('mkdir -p %(django_user_home)s/configs/nginx' % env)
    sudo('mkdir -p %(django_user_home)s/configs/supervisord' % env)
    sudo('mkdir -p %(django_user_home)s/scripts' % env)
    sudo('mkdir -p %(django_user_home)s/htdocs' % env)
    sudo('mkdir -p %(django_user_home)s/tmp' % env)
    sudo('echo "<html><body>nothing here</body></html> " > %(django_user_home)s/htdocs/index.html' % env)


def pull():
    require('hosts', provided_by=PROVIDING_PROJECT)
    with cd(env.code_root):
        run('hg pull -u')


def setup():
    require('project', provided_by=PROVIDING_PROJECT)
    require('hosts', provided_by=PROVIDING_PROJECT)
    require('user', provided_by=PROVIDING_PROJECT)
    if env.ask_confirmation:
        if not console.confirm("Are you sure you want to setup %s?" % red_bg(env.project.upper()), default=False):
            abort("Aborting at user request.")
    puts(green_bg('Start setup...'))
    start_time = datetime.now()

    sudo('cd .')  # do nothing, just authenticate sudo user
    _create_django_user()
    _setup_directories()

    end_time = datetime.now()
    finish_message = '[%s] Correctly finished in %i seconds' % \
    (green_bg(end_time.strftime('%H:%M:%S')), (end_time - start_time).seconds)
    puts(finish_message)
