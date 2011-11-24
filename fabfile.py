from datetime import datetime
from os.path import join
from fabric.api import env, puts, abort, require, cd, hide
from fabric.operations import sudo, settings, run
from fabric.contrib import console
from fabric.contrib.files import upload_template
env.hosts = ['localhost', ]

from fabric.colors import _wrap_with


green_bg = _wrap_with('42')
red_bg = _wrap_with('41')

REPOSITORY = 'https://bitbucket.org/DNX/django-fagungis'
PROVIDING_PROJECT = ('prod', )


def prod():
    #  name of your project - no spaces, no special chars
    env.project = 'project_prod'
    #  hosts to deploy your project, users must be sudoers
    env.hosts = ['root@192.168.1.1', ]
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
    #  django media dir, if not in code_root please adjust also nginx.conf
    env.django_media_path = join(env.code_root, 'media')
    #  django sattic dir, if not in code_root please adjust also nginx.conf
    env.django_static_path = join(env.code_root, 'static')
    #  do you use south in your django project?
    env.south_used = False
    #  virtualenv root
    env.virtenv = join(env.django_user_home, 'envs', env.project)
    #  some virtualenv options, must have at least one
    env.virtenv_options = ['distribute', 'no-site-packages', ]
    #  always ask user for confirmation when run any tasks
    env.ask_confirmation = True

    ### START gunicorn settings ###
    env.gunicorn_bind = "127.0.0.1:8100"
    env.gunicorn_logfile = '%(django_user_home)s/logs/projects/%(project)s_gunicorn.log' % env
    env.gunicorn_workers = 4
    env.gunicorn_worker_class = "eventlet"
    env.gunicorn_loglevel = "info"
    ### END gunicorn settings ###

    ### START nginx settings ###
    env.nginx_server_name = 'example.com'  # Only domain name, without 'www' or 'http://'
    ### END nginx settings ###

    ### START supervisor settings ###
    env.supervisorctl = '/usr/bin/supervisorctl'  # supervisorctl script
    env.supervisor_autostart = 'true'  # true or false
    env.supervisor_autorestart = 'true'  # true or false
    env.supervisor_redirect_stderr = 'true'  # true or false
    env.supervisor_stdout_logfile = '%(django_user_home)s/logs/projects/supervisord_%(project)s.log' % env
    ### END supervisor settings ###


def _create_django_user():
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = sudo('useradd -d %(django_user_home)s -m -r %(django_user)s' % env)
        if 'already exists' in res:
            puts('User \'%(django_user)s\' already exists, will not be changed.' % env)
            return
        #  set password
        sudo('passwd %(django_user)s' % env)


def _verify_sudo():
    ''' we just check if the user is sudoers '''
    sudo('cd .')


def _install_nginx():
    # add nginx stable ppa
    sudo('add-apt-repository ppa:nginx/stable')
    sudo('apt-get update')
    sudo('apt-get install nginx')
    sudo('/etc/init.d/nginx start')


def _install_dependencies():
    ''' Ensure those Debian/Ubuntu packages are installed '''
    packages = [
        'mercurial',
        'python-pip',
        'supervisor',
    ]
    sudo('aptitude install %s' % ' '.join(packages))
    _install_nginx()
    sudo('pip install --upgrade pip')


def _install_requirements():
    ''' you must have a file called requirements.txt in your project root'''
    requirements = join(env.code_root, 'requirements.txt')
    virtenvrun('pip install -r %s' % requirements)


def _install_gunicorn():
    """ force gunicorn installation into your virtualenv, even if it's installed globally.
    for more details: https://github.com/benoitc/gunicorn/pull/280 """
    virtenvrun('pip install -I gunicorn')


def _install_virtualenv():
    sudo('pip install virtualenv')


def _create_virtualenv():
    sudo('virtualenv --%s %s' % (' --'.join(env.virtenv_options), env.virtenv))


def _setup_directories():
    sudo('mkdir -p %(projects_path)s' % env)
    sudo('mkdir -p %(django_user_home)s/logs/nginx' % env)
    sudo('mkdir -p %(django_user_home)s/logs/projects' % env)
    sudo('mkdir -p %(django_user_home)s/configs/nginx' % env)
    sudo('mkdir -p %(django_user_home)s/configs/supervisord' % env)
    sudo('mkdir -p %(django_user_home)s/scripts' % env)
    sudo('mkdir -p %(virtenv)s' % env)
    sudo('echo "<html><body>nothing here</body></html> " > %(django_user_home)s/htdocs/index.html' % env)


def hg_pull():
    require('hosts', provided_by=PROVIDING_PROJECT)
    with cd(env.code_root):
        run('hg pull -u')


def virtenvrun(command):
    activate = 'source %s/bin/activate' % env.virtenv
    run(activate + ' && ' + command)


def _hg_clone():
    run('hg clone %s %s' % (REPOSITORY, env.code_root))


def test_nginx_conf():
    sudo('nginx -t -c /etc/nginx/nginx.conf')


def _upload_nginx_conf():
    ''' upload nginx conf '''
    nginx_file = '%(django_user_home)s/configs/nginx/%(project)s.conf' % env
    upload_template('conf/nginx.conf', nginx_file,
                    context=env, backup=False)
    sudo('ln -sf %s /etc/nginx/sites-enabled/' % nginx_file)
    test_nginx_conf()
    sudo('nginx -s reload')


def reload_supervisorctl():
    sudo('%(supervisorctl)s reread' % env)
    sudo('%(supervisorctl)s reload' % env)


def _upload_supervisord_conf():
    ''' upload supervisor conf '''
    supervisord_conf_file = '%(django_user_home)s/configs/supervisord/%(project)s.conf' % env
    upload_template('conf/supervisord.conf', supervisord_conf_file,
                    context=env, backup=False)
    sudo('ln -sf %s /etc/supervisor/conf.d/' % supervisord_conf_file)
    reload_supervisorctl()


def _prepare_django_project():
    with cd(env.django_project_root):
        virtenvrun('./manage.py syncdb --noinput --verbosity=1')
        if env.south_used:
            virtenvrun('./manage.py migrate --noinput --verbosity=1')
        virtenvrun('./manage.py collectstatic --noinput')


def _prepare_media_path():
    sudo('chmod -R 775 %s' % env.django_media_path)


def _upload_rungunicorn_script():
    ''' upload rungunicorn conf '''
    script_file = '%(django_user_home)s/scripts/rungunicorn_%(project)s.sh' % env
    upload_template('scripts/rungunicorn.sh', script_file,
                    context=env, backup=False)
    sudo('chmod +x %s' % script_file)


def _supervisor_restart():
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = sudo('%(supervisorctl)s restart %(project)s' % env)
    if 'ERROR' in res:
        print red_bg("%s NOT STARTED!" % env.project)
    else:
        print green_bg("%s correctly started!" % env.project)


def setup():
    require('project', provided_by=PROVIDING_PROJECT)
    require('hosts', provided_by=PROVIDING_PROJECT)
    require('user', provided_by=PROVIDING_PROJECT)
    if env.ask_confirmation:
        if not console.confirm("Are you sure you want to setup %s?" % red_bg(env.project.upper()), default=False):
            abort("Aborting at user request.")
    puts(green_bg('Start setup...'))
    start_time = datetime.now()

    _verify_sudo
    _install_dependencies()
    _create_django_user()
    _setup_directories()
    _hg_clone()
    _install_virtualenv()
    _create_virtualenv()
    _install_gunicorn()
    _install_requirements()
    _upload_nginx_conf()
    _upload_rungunicorn_script()
    _upload_supervisord_conf()

    end_time = datetime.now()
    finish_message = '[%s] Correctly finished in %i seconds' % \
    (green_bg(end_time.strftime('%H:%M:%S')), (end_time - start_time).seconds)
    puts(finish_message)


def deploy():
    _verify_sudo()
    if env.ask_confirmation:
        if not console.confirm("Are you sure you want to deploy in %s?" % red_bg(env.project.upper()), default=False):
            abort("Aborting at user request.")
    puts(green_bg('Start setup...'))
    start_time = datetime.now()

    hg_pull()
    _install_requirements()
    _upload_nginx_conf()
    _upload_rungunicorn_script()
    _prepare_django_project()
    _prepare_media_path()
    _supervisor_restart()

    end_time = datetime.now()
    finish_message = '[%s] Correctly deployed in %i seconds' % \
    (green_bg(end_time.strftime('%H:%M:%S')), (end_time - start_time).seconds)
    puts(finish_message)
