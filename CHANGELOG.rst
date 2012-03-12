Changelog
=============================================================

Version 0.0.14
-------------------------------------------------------------

* changed the name of nginx config file according to nginx_conf_file
* changed the name of supervisor config file according to supervisord_conf_file
* now upload supervisord_conf_file also in deploy task
* added supervisor_program_name configuration
* set nginx_client_max_body_size default to 10
* set requirements_file default to: join(env.code_root, 'requirements.txt')
* improved the feedback on _supervisor_restart
* updated README.rst about github repo
* backward compatible with 0.0.13

Version 0.0.13
-------------------------------------------------------------

* added assume "yes" as answer to all apt-get prompts
* added virtenvsudo task
* added requirements_file config, for pip requirements file location
* added python-dev and build-essential packages to requirements
* fixed the bug about supervisor and gunicorn log file permissions
* changed the default value of django_project_root in example_fabfile.py
* another bug fixes

Version 0.0.12
-------------------------------------------------------------

* fixed _setup_directories
* improved media and static ngnix configuration
* fixed gunicorn log directory permission and ownership

Version 0.0.11
-------------------------------------------------------------

* Added client_max_body_size nginx server configuration
* Added additional_packages config parameter

Version 0.0.10
-------------------------------------------------------------

* Updated documentation
* Switched to apt-get package manager
* Some bugfixes

Version 0.0.9
-------------------------------------------------------------

* Always display configuration info

Version 0.0.8
-------------------------------------------------------------

* Fixed a minor bug in test_configuration
* Formatted test_configuration task output

Version 0.0.7
-------------------------------------------------------------

* Added verbose functionality to test_configuration task

Version 0.0.6
-------------------------------------------------------------

* Declared namespace
* Cleaned MANIFEST.in

Version 0.0.5
-------------------------------------------------------------

* Restructured example_fabfile.py
* Updated README file
* Removed projects folder from MANIFEST.in

Version 0.0.4
-------------------------------------------------------------

* Prepared for pypi
* Added example_fabfile.py
* Added LICENSE file

Version 0.0.3
-------------------------------------------------------------

* Added configuration tests

Version 0.0.2
-------------------------------------------------------------

* Moved project configuration in projects folder

Version 0.0.1
-------------------------------------------------------------

* Added **setup** task
* Added **deploy** task