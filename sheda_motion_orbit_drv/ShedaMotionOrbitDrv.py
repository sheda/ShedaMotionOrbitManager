#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  Copyright (C) 2016, Sheda (sheda1805 at gmail.com)
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

import subprocess
import sys, os
import ConfigParser
import time

# ---------------------------------
# Common control for ShedaOrbitDrv
UVCDYNCTRLEXEC="/usr/bin/uvcdynctrl"

# The value indicates amount of movement for panning and tilt
# Max Ranges (determined with uvcdynctrl -v -c):
# Tilt = -1920 to 1920
# Pan  = -4480 to 4480
panRight = "100"
panLeft = "-100"
tiltUp = "-100"
tiltDown = "100"
maxPos = "6"

# ---------------------------------
# Common Control for ShedaMotionDrv
MOTION_CMD="/usr/bin/motion"
NOHUP_CMD="/usr/bin/nohup"
KILL_CMD="/usr/bin/kill"
WGETEXEC="/usr/bin/wget"

# CTRL Server only for control local_loop
CTRL_URL="127.0.0.1"
CTRL_PORT="8080"
MOTION_ADMIN_SRV_URL=CTRL_URL+":"+CTRL_PORT

# MOTION MANAGER
PID_FILE_PATH="/var/run"
PID_FILE_NAME="sheda_motion_orbit_manager.pid"


class ShedaOrbitDrv:
## Define the init script to initialize the application
    def __init__(self,
                 logger,
                 conf="/etc/sheda_motion_orbit_manager.conf"):
        self.logger = logger
        self.conf = ConfigParser.ConfigParser()
        self.cfg_ok = self.conf.read([conf])
        if not self.cfg_ok:
            self.panRight = panRight
            self.panLeft  = panLeft
            self.tiltUp   = tiltUp
            self.tiltDown = tiltDown
            self.max_pos  = maxPos
        else:
            self.panRight = self.conf.get("position", "panRight")
            self.panLeft  = self.conf.get("position", "panLeft")
            self.tiltUp   = self.conf.get("position", "tiltUp")
            self.tiltDown = self.conf.get("position", "tiltDown")
            self.max_pos  = self.conf.get("position", "max_pos")
        return

    # Generic Move
    def __moveGeneric(self, control, value):
        self.logger.debug("Move "+ str(control) + " "+ str(value))
        result = subprocess.Popen([UVCDYNCTRLEXEC, "-s", control, "--", value],
                 stdout=subprocess.PIPE,
                 stderr=subprocess.PIPE,
                 shell=False)
        out, err = result.communicate()
        return True

    # Generic Reset
    def __resetGeneric(self, control, value):
        result = subprocess.Popen([UVCDYNCTRLEXEC, "-s", control, value],
                 stdout=subprocess.PIPE,
                 stderr=subprocess.PIPE,
                 shell=False)
        out, err = result.communicate()
        return True

    # Tilt up
    def moveUp(self):
        return self.__moveGeneric("Tilt, Relative", self.tiltUp)

    # Tilt Down
    def moveDown(self):
        return self.__moveGeneric("Tilt, Relative", self.tiltDown)

    # Pan Right
    def moveRight(self):
        return self.__moveGeneric("Pan, Relative", self.panRight)

    # Pan Left
    def moveLeft(self):
        return self.__moveGeneric("Pan, Relative", self.panLeft)

    # Pan/Tilt to Position
    def movePosition(self, position):
        # position is str
        if ((int(position) >= 0) and (int(position) <= int(self.max_pos))):
            try:
                pan_value = self.conf.get("position", "pan_"  + str(position))
                tilt_value  = self.conf.get("position", "tilt_" + str(position))
            except:
                self.logger.error("Unknown Position in config position number:"+ str(position))
                return False
        else:
            self.logger.error("Unknown position number:"+ str(position))
            return False

        # check not None in config
        if (not tilt_value) or (not pan_value):
            return False

        # Reset
        self.resetHor()
        time.sleep(2)
        self.resetVer()
        time.sleep(2)

        self.logger.debug("Position Pan:"+ str(pan_value) + ", Tilt:"+ str(tilt_value))
        ret_code  = self.__moveGeneric("Pan, Relative", pan_value)
        time.sleep(2)
        ret_code &= self.__moveGeneric("Tilt, Relative", tilt_value)
        time.sleep(2)
        return ret_code

    # Pan Reset
    def resetHor(self):
        return self.__resetGeneric("Pan, Reset", "1")

    # Tilt Reset
    def resetVer(self):
        return self.__resetGeneric("Tilt, Reset", "1")

    # Tilt Reset
    def getPosName(self, position):
        # position is str
        if ((int(position) >= 0) and (int(position) <= int(self.max_pos))):
            try:
                return self.conf.get("position", "name_"  + str(position))
            except:
                self.logger.error("Unknown Position number "+ str(position))
                return str(position)
        else:
            self.logger.error("Unknown position number"+ str(position))
            return str(position)


class ShedaMotionDrv:
    ## Define the init script to initialize the application
    def __init__(self,
                 logger,
                 conf="/etc/sheda_motion_orbit_manager.conf"):
        self.logger = logger

        # Get position for watching
        self.conf_name = conf
        self.conf = ConfigParser.ConfigParser()
        self.cfg_ok = self.conf.read([self.conf_name])

        # Check for running process
        self.pid=-1
        pid_filename = os.path.join(PID_FILE_PATH, PID_FILE_NAME)
        if os.path.isfile(pid_filename):
            pid_file = open(pid_filename, 'r') # read/write at begining
            self.pid = pid_file.read()
            self.logger.debug('pid file exist:'+pid_filename+" contain pid:"+self.pid)
            pid_file.close()
        return

    # Public API
    def start(self, watch, move=False):
        self.logger.info("START command with watch: " + str(watch) + ", and move: "+str(move))
        position_reached = False

        # 1 - Running
        running = self._check_running()
        if not running:
            self.logger.debug(" . Not running")
            # First move the camera
            if move:
                if self.cfg_ok:
                    position = self.conf.get("watch", "on_position")
                    if position:
                        self.logger.info(" . Move to on_position: "+str(position))
                        orbit_drv=ShedaOrbitDrv(self.conf_name)
                        orbit_drv.movePosition(position) # timing to wait postion arrival already set
                        position_reached = True
            # Then Start running
            self.logger.info(" . Start Run")
            self._start_running()
            time.sleep(0.5)
        else:
            self.logger.info(" . Already running")

        # 2 - Watch
        if watch:
            self.logger.debug(" . The Watch requested")
            watching = self._check_watching()
            if not watching:
                self.logger.debug(" . not watching")
                # First move the camera if not already done
                if move and not position_reached:
                    if self.cfg_ok:
                        position = self.conf.get("watch", "on_position")
                        if position:
                            self.logger.info(" . Move to on_position: "+str(position))
                            orbit_drv=ShedaOrbitDrv(self.conf_name)
                            orbit_drv.movePosition(position)
                # Then start the watch
                self.logger.info(" . Start the watch")
                self._start_watching()
            else:
                self.logger.info(" . Already watching")
        else:
            self.logger.debug(" . The Watch Not requested")
            watching = self._check_watching()
            if watching:
                self.logger.debug(" . but watching")
                self.logger.info(" . Stop the watch")
                self._stop_watching()
        return True

    def status(self, watch=False):
        self.logger.info("STATUS command with watch: " + str(watch))
        running = self._check_running()
        if not running:
            return running
        else:
            watching = self._check_watching()
            if not watch:
                return True
            else:
                return watching

    def stop(self, watch, move=False):
        self.logger.info("STOP command with watch: " + str(watch) + ", and move: "+str(move))
        running = self._check_running()
        if not running:
            self.logger.info(" . Not running")
            return True
        else:
            if watch:
                self.logger.debug(" . Stop only the watch")
                watching = self._check_watching()
                if watching:
                    self.logger.info(" . Stop the watch")
                    self._stop_watching()
                else:
                    self.logger.info(" . The Watch already stopped")
            else:
                self.logger.info(" . Stop running")
                self._stop_running()

            # Then move to the off postion
            if move:
                if self.cfg_ok:
                    position = self.conf.get("watch", "off_position")
                    if position:
                        self.logger.info(" . Move to off_position: "+str(position))
                        orbit_drv=ShedaOrbitDrv(self.conf_name)
                        orbit_drv.movePosition(position)
            return True

    # Private Utils Methodes
    def __kill_pid(self, pid):
        """ Check For the existence of a unix pid. """
        try:
            os.kill(pid, 9)
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
                self.logger.debug(" . . PID file exist, check running: Started")
                return True
            else:
                self.logger.debug(" . . PID file exist, check running: Stopped, clean pid_file")
                pid_filename = os.path.join(PID_FILE_PATH, PID_FILE_NAME)
                if os.path.isfile(pid_filename):
                    os.remove(pid_filename)
                return False
        else:
            self.logger.debug(" . . PID file doesn't exist, check running: Stopped")
            return False


    def _start_running(self):
        proc = subprocess.Popen([NOHUP_CMD, MOTION_CMD, "2>&1"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=False)
        # Write PID file
        pid_filename = os.path.join(PID_FILE_PATH, PID_FILE_NAME)
        pid_file = open(pid_filename, 'w+' if (self.pid==-1) else 'r+') # read/write at begining
        pid_file.write(str(proc.pid))
        pid_file.close()
        self.logger.debug(" . . Started running (pid: " + str(proc.pid) + " ), wrote PID file: "+pid_filename)

        return True

    def _stop_running(self):
        if (self.__kill_pid(int(self.pid))):
            pid_filename = os.path.join(PID_FILE_PATH, PID_FILE_NAME)
            os.remove(pid_filename)
            self.logger.debug(" . Stopped Running (pid: " + str(self.pid) + " )")
        else:
            self.logger.error(" . While Stopping (pid: " + str(self.pid) + " )")

        return True

    # WATCH PART
    def _check_watching(self):
        import requests
        req = requests.get("http://"+MOTION_ADMIN_SRV_URL+"/0/detection/status")
        status = req.status_code
        body = str(req.text)
        self.logger.debug((body,str(status)))
        if (status == 200) and (body.find("Detection status ACTIVE") != -1):
            self.logger.info(" . The Watch is Active")
            return True
        else:
            self.logger.info(" . The Watch is Not Active")
            return False

    def _start_watching(self):
        # Start Motion
        import requests
        req = requests.get("http://"+MOTION_ADMIN_SRV_URL+"/0/detection/start")
        status = req.status_code
        body = str(req.text)
        self.logger.debug((body,str(status))
        self.logger.info( " . Watch Activated")
        return (status == 200)

    def _stop_watching(self):
        import requests
        req = requests.get("http://"+MOTION_ADMIN_SRV_URL+"/0/detection/pause")
        self.logger.debug(str(req))
        status = req.status_code
        body = str(req.text)
        self.logger.debug((body,str(status))
        self.logger.info( " . Watch Desactivated")
        return True
