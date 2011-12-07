===========================================================================
django-fagungis: DJANGO + FAbric + GUnicorn + NGInx + Supervisor deployment
===========================================================================

Introduction
============

django-fagungis allow you to easy setup and deploy your django project on
your linux server.
django-fagungis will install and configure for you:

* nginx

* gunicorn

* supervisor

* virtualenv

Installation
============

There are a few different ways to install Fagungis:

Using pip
---------
If you have pip install available on your system, just type::

    pip install django-fagungis

If you've already got an old version of Fagungis, and want to upgrade, use::

    pip install -U django-fagungis

Installing from a directory
---------------------------
If you've obtained a copy of Fagungis using either Mercurial or a downloadable
archive, you'll need to install the copy you have system-wide. Try running::

    python setup.py develop

If that fails, you don't have ``setuptools`` or an equivalent installed;
either install them, or run::

    python setup.py install


How to use fagungis?
====================

If you have already installed Fagungis, you must proceed with the
configuration of your project.

Configuration
-------------

First of all you must configure your project task settings. To do this we
have prepared for you an example file in **path/to/fagungis/example_fabfile.py**
so you can create a copy of this file and modify it according to your
needs.

You can find also an online version of **example_fabfile.py** here: https://bitbucket.org/DNX/django-fagungis/src/tip/fagungis/example_fabfile.py

Please pay attention to not have any tasks in your fabfile.py called:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

* setup

* deploy

* test_configuration

or

* hg_pull

because these names are reserved by Fagungis.

Test your configuration first!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Fagungis come with its own automatic configuration tests. Each time you run
**setup** or **deploy** task, configuration tests are called.
Anyway, you can manually run these tests for your project configuration::

    fab project_name test_configuration

If you run **test_configuration** manually, you'll observe some output about all your project settings.

Do you need an example?
~~~~~~~~~~~~~~~~~~~~~~~

Ok, let's assume you want to configure your django project called "projectus".
So, what we know about it?
we know:

* the project is called **projectus**

* the hg repository is **https://bitbucket.org/DNX/projectus**

* the ip of the server where you want to host it is: **88.88.88.88**

* you want to use the domain **www.projectus.org** which point to 88.88.88.88


Ok, it's enough to configure and deploy your project, let's do it!
Clone example_fabfile.py::

    cp path/to/fagungis/example_fabfile.py path/to/projectus/fabfile.py

or::

    wget -O fabfile.py https://bitbucket.org/DNX/django-fagungis/raw/tip/fagungis/example_fabfile.py


Now apply some changes to earlier cloned fabfile.py file in your project root:

* change task name::

    # from:
    @task
    def example():
    # to:
    @task
    def projectus():

* change project name::

    # from:
    env.project = 'example_production'
    # to:
    env.project = 'projectus'

* change repository::

    # from:
    env.repository = 'https://bitbucket.org/DNX/example'
    # to:
    env.repository = 'https://bitbucket.org/DNX/projectus'

* change server ip::

    # from:
    env.hosts = ['root@192.168.1.1', ]
    # to:
    env.hosts = ['root@88.88.88.88', ]

* change nginx server name::

    # from:
    env.nginx_server_name = 'example.com'
    # to:
    env.nginx_server_name = 'projectus.org'

not, let's test our configuration::

    fab projectus test_configuration

you must see a message::

    Configuration tests passed!


Setup your project
------------------

Assuming you've configured your project now you are ready to launch the setup::

    fab projectus setup

during this process you can see all the output of the commands launched on
the server. At some point you may be asked for some information as django
user password(if django user did not exist before) or repository password to
clone your project.
At the end of this task you must view a message saying that the setup
successful ended.
Now you can go on with the deployment of the project.
**Please** test manualy the setup at least at the first time following
this guide:: https://bitbucket.org/DNX/django-fagungis/wiki/Setup_test

Deploy the project
------------------

After you've run the setup you're ready to deploy your project. This is as
simple as typing::

    fab projectus deploy

As for setup you may be asked for some info during the deployment.
At the end you must view a message saying that the deployment successful
ended.
Now navigate to **http://projectus.org** in your browser and assure that
everything is O.K.


How to test fagungis?
=====================

**Please** test all operations manualy, at least at the first time, following
this guide:

https://bitbucket.org/DNX/django-fagungis/wiki/Setup_test

This will increase your confidence in using **fagungis**.