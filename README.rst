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


How to use fagungis?
====================

Configuration
-------------

First of all you must configure your project/server settings. To do this we
have prepared for you an example file in **projects/example.py** so you can
create a copy of this file and modify it according to your needs. Also don't
forget to include it in **projects/__init__.py** file.

Do you need an example?
~~~~~~~~~~~~~~~~~~~~~~~

Ok, let's assume you want to configure your django project called "projectus".
So, what we know about it?
we know:

* the project is called **projectus**

* the hg repository is **https://bitbucket.org/DNX/projectus**

* the ip of the server where you want to host it is: 88.88.88.88

* you want to use the domain **www.projectus.org** which point to 88.88.88.88


Ok, it's enough to configure and deploy your project, let's do it!
Clone projects/example.py:

  cp projects/example.py projects/projectus.py

Import projectus tasks, so put in projects/__init__.py:

  from projectus import *

Now apply some changes to earlier cloned projectus.py file:

* change task name:

  # from:
  @task
  def example():
  # to:
  @task
  def projectus():

* change project name:

  # from:
  env.project = 'example_production'
  # to:
  env.project = 'projectus'

* change repository:

  # from:
  env.repository = 'https://bitbucket.org/DNX/example'
  # to:
  env.repository = 'https://bitbucket.org/DNX/projectus'

* change server ip:

  # from:
  env.hosts = ['root@192.168.1.1', ]
  # to:
  env.hosts = ['root@88.88.88.88', ]

* change nginx server name:

  # from:
  env.nginx_server_name = 'example.com'
  # to:
  env.nginx_server_name = 'projectus.org'


Setup your project
------------------

Assuming you've configured your project now you are ready to launch the setup:

  fab projectus setup

during this process you can see all the output of the commands launched on
the server. At some point you may be asked for some information as django
user password(if django user did not exist before) or repository password to
clone your project.
At the end of this task you must view a message saying that the setup
successful ended.
Now you can go on with the deployment of the project.
**Please** test manualy the setup at least at the first time following
this guide: https://bitbucket.org/DNX/django-fagungis/wiki/Setup_test

Deploy the project
------------------

After you've run the setup you're ready to deploy your project. This is as
simple as typing:

  fab projectus deploy

As for setup you may be asked for some info during the deployment.
At the end you must view a message saying that the deployment successful
ended.
Now navigate to http://projectus.org in your browser and assure that
everything is O.K.


How to test fagungis?
=====================

**Please** test all operations manualy, at least at the first time, following
this guide: https://bitbucket.org/DNX/django-fagungis/wiki/Setup_test

This will increase your confidence in using **fagungis**.