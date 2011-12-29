#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Unix',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Topic :: Software Development',
    'Topic :: Software Development :: Build Tools',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: System :: Clustering',
    'Topic :: System :: Software Distribution',
    'Topic :: System :: Systems Administration',
]

setup(
    name="django-fagungis",
    version=__import__('fagungis').__version__,
    url='https://bitbucket.org/DNX/django-fagungis/wiki/Home',
    download_url='http://bitbucket.org/DNX/django-fagungis/downloads',
    license='BSD License',
    description="DJANGO + FAbric + GUnicorn + NGInx + Supervisor deployment",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author='Darii Denis',
    author_email='info@ddenis.com',
    keywords='django fabric gunicorn nginx supervisor',
    packages=find_packages(),
    namespace_packages=['fagungis'],
    include_package_data=True,
    zip_safe=False,
    classifiers=CLASSIFIERS,
    install_requires=[
        'Fabric>=1.3',
    ],
)
