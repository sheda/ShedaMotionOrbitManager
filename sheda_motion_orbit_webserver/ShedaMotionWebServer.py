#!/usr/bin/python
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

import os
import shlex, subprocess

# WebServer utils
PID_FILE_PATH="/var/run"
PID_FILE_NAME="sheda_motion_orbit_webserver.pid"


class ShedaMotionWebServer:
    ## Define the init script to initialize the application
    def __init__(self,
                 logger):
        self.logger = logger

        # Check for running process
        self.pid=-1
        pid_filename = os.path.join(PID_FILE_PATH, PID_FILE_NAME)
        if os.path.isfile(pid_filename):
            pid_file = open(pid_filename, 'r') # read/write at begining
            self.pid = pid_file.read()
            self.logger.debug('pid file exist:'+pid_filename+" contain pid:"+self.pid)
            pid_file.close()
        return

    # Private Utils Methodes
    def __kill_pid(self, pid):
        """ Check For the existence of a unix pid. """
        try:
            self.logger.debug("Kill pid:" +str(pid)+ ", gid:"+ str(os.getpgid(pid)))
            os.killpg(os.getpgid(pid), 9)
        except OSError:
            return False
        else:
            return True

    def __check_pid(self, pid):
        """ Check For the existence of a unix pid. """
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True

    # Low API, should not be used directly
    # Live streaming Part
    def _check_running(self):
        if self.pid != -1:
            if (self.__check_pid(int(self.pid))):
                self.logger.debug(" . PID file exist, check running: Started")
                return True
            else:
                self.logger.debug(" . PID file exist, check running: Stopped, clean pid_file")
                pid_filename = os.path.join(PID_FILE_PATH, PID_FILE_NAME)
                if os.path.isfile(pid_filename):
                    os.remove(pid_filename)
                return False
        else:
            self.logger.debug(" . PID file doesn't exist, check running: Stopped")
            return False

    def start(self):
        running = self._check_running();
        if running :
            self.logger.info("Already Started")
            return True
        else:
            args = shlex.split("/usr/bin/python sheda_motion_orbit_webserver/manage.py runserver -v 2 0.0.0.0:8090")
            result = subprocess.Popen(args,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     preexec_fn=os.setsid,
                     shell=False)

            # Write PID file
            pid_filename = os.path.join(PID_FILE_PATH, PID_FILE_NAME)
            pid_file = open(pid_filename, 'r+' if (os.path.isfile(pid_filename)) else 'w+') # read/write at begining
            pid_file.write(str(result.pid))
            pid_file.close()

            self.logger.info(" . . Started running (pid: " + str(result.pid) + " ), wrote PID file: "+pid_filename)
            return True

    def stop(self):
        running = self._check_running();
        if running :
            if (self.__kill_pid(int(self.pid))):
                pid_filename = os.path.join(PID_FILE_PATH, PID_FILE_NAME)
                os.remove(pid_filename)
                self.logger.info("Stopped Running (pid: " + str(self.pid) + " )")
                return True
            else:
                self.logger.error("While Stopping (pid: " + str(self.pid) + " )")
                return False
        else:
            self.logger.info("Already Stopped")
            return True
