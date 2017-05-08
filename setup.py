"""
Flask-Common
-------------

A Flask extension with lots of common time-savers (file-serving, favicons, etc).
"""
import os
import sys
from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='Flask-Common',
    version='0.1.0',
    url='https://github.com/kennethreitz/flask-common',
    license='BSD',
    author='Kenneth Reitz',
    author_email='me@kennethreitz.org',
    description='A Flask extension with lots of common time-savers (file-serving, favicons, etc).',
    long_description=__doc__,
    py_modules=['flask_common'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Gunicorn',
        'WhiteNoise',
        'crayons',
        'maya',
        'flask_cache'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)