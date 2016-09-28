# -*- coding: utf-8 -*-
#
#  Copyright (C) 2016, Sheda (sheda.dev at gmail.com)
#
#  Homepage: http://www.sheda.fr/
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup

setup(name='sheda_motion_orbit_manager',
      description='Manage motion live streaming and surveillance activity, as well as movement for Logitech Orbit Cam',
      version='0.1',
      license="GPL v3",

      author="Sheda",
      author_email="sheda.dev@gmail.com",
      url='www.sheda.fr',

      scripts=["sheda_motion_orbit_manager"],
      packages=["sheda_motion_orbit_drv"],
      # package_dir={'sheda_motion_orbit_drv' : 'sheda_motion_orbit_drv'},                                           # package "sheda_motion_orbit_drv" is located in folder sheda_motion_orbit_drv
      # package_data={'sheda_motion_orbit_drv': ['configs/sheda_motion_orbit_manager.conf', 'configs/motion.conf']}, # package "sheda_motion_orbit_drv" has a data enclosed within 'some configs files'

      # Each (directory, files) pair in the sequence specifies the installation directory and the files to install there. If directory is a relative path, it is interpreted relative to the installation
      # prefix (Python’s sys.prefix for pure-Python packages, sys.exec_prefix for packages that contain extension modules). Each file name in files is interpreted relative to the setup.py script at the
      # top of the package source distribution. No directory information from files is used to determine the final location of the installed file; only the name of the file is used.
      data_files=[('/etc', ['configs/sheda_motion_orbit_manager.conf']), # Configuration file
                  ('/etc/motion/', ['configs/motion.conf'])],

      classifiers=[
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "Environment :: Console",
        "Operating System :: POSIX",
        "Framework :: Django",
        "Programming Language :: Python",
        "Topic :: Utilities",
        ]
    )

print """

--------------------------------------------------------------------------------------------------
Don't forget to copy the udev rule file to the right folder according to your distrib
--------------------------------------------------------------------------------------------------
For example on debian/ubuntu:
$ sudo cp configs/motion.conf /etc/motion/motion.conf
$ sudo cp configs/sheda_motion_orbit_manager.conf /etc/sheda_motion_orbit_manager.conf
--------------------------------------------------------------------------------------------------
"""

