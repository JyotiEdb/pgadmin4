#########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2024, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import builtins
import os
import sys
import platform
from codecs import open
from importlib.machinery import SourceFileLoader

from setuptools import setup


# Load a source file
def load_source(name, path):
    if not os.path.exists(path):
        print("ERROR: Could not find %s" % path)
        sys.exit(1)

    return SourceFileLoader(name, path).load_module()


# Ensure the global server mode is set.
builtins.SERVER_MODE = None

# Get the requirements list for the current version of Python
req_file = '../requirements.txt'

with open(req_file, 'r') as req_lines:
    all_requires = req_lines.read().splitlines()

requires = []
kerberos_extras = []
# Ensure the Wheel will use psycopg-binary, not the source distro, and stick
# gssapi in it's own list
for index, req in enumerate(all_requires):
    if 'psycopg[c]' in req:
        # Starting from Psycopg 3.1.20, ARM64 macOS binary packages are no
        # longer available for macOS versions before 14.0.
        _req = req.replace('psycopg[c]', 'psycopg[binary]')
        req = "psycopg[binary] == 3.1.19; sys_platform == 'darwin' and" \
              " platform_machine == 'arm64' and platform_release < '23.0' \n"\
              + _req + ";  (sys_platform == 'darwin' and" \
                       " platform_machine == 'arm64' and" \
                       " platform_release >= '23.0') or" \
                       " (sys_platform == 'darwin' and" \
                       " platform_machine != 'arm64'" \
                       ") or sys_platform != 'darwin'"

    if 'gssapi' in req:
        kerberos_extras.append(req)
    else:
        requires.append(req)

# Get the version
path = '../web/'
if not os.path.exists(path):
    print("ERROR: Could not find %s" % path)
    sys.exit(1)
sys.path.append(path)
import config

setup(
    name='pgadmin4',

    version=config.APP_VERSION,

    description='PostgreSQL Tools',
    long_description='pgAdmin is the most popular and feature rich Open '
                     'Source administration and development platform for '
                     'PostgreSQL, the most advanced Open Source database in '
                     'the world.\n\npgAdmin may be used on Linux, Unix, '
                     'macOS and Windows to manage PostgreSQL and EDB '
                     'Advanced Server 10 and above.',

    url='https://www.pgadmin.org/',

    author='The pgAdmin Development Team',
    author_email='pgadmin-hackers@postgresql.org',

    license='PostgreSQL Licence',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        # Supported programming languages
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],

    keywords='pgadmin4,postgresql,postgres',

    packages=["pgadmin4"],

    include_package_data=True,

    install_requires=requires,

    extras_require={
        "kerberos": kerberos_extras,
    },

    entry_points={
        'console_scripts': ['pgadmin4=pgadmin4.pgAdmin4:main',
                            'pgadmin4-cli=pgadmin4.setup:main'],
    },

)
