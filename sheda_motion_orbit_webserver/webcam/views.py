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

from django.shortcuts import render

from django.http import *
from django.template import loader

import logging, logging.handlers
from sheda_motion_orbit_drv.ShedaMotionOrbitDrv import ShedaOrbitDrv, ShedaMotionDrv

logging_filename='/var/log/sheda_motion_orbit_manager_webserver.log'

def create_logger(debug, loggername, log_file_enable, filename):
    # Logger
    logger = logging.getLogger(loggername)
    logger.setLevel(logging.DEBUG)  # Only allow debug
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(funcName)s - %(message)s')

    # STREAM CHANNEL - STDOUT
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    if debug:
        stream.setLevel(logging.DEBUG)
    else:
        stream.setLevel(logging.INFO)
    logger.addHandler(stream)

    # ROTATING CHANNEL
    if log_file_enable:
        rf = logging.handlers.RotatingFileHandler(filename, mode='a', maxBytes=1000000, backupCount=5)
        formatter_file = logging.Formatter('%(name)s - %(levelname)s - %(asctime)-15s - %(funcName)s - %(message)s')
        rf.setFormatter(formatter_file)
        if debug:
            rf.setLevel(logging.DEBUG)
        else:
            rf.setLevel(logging.INFO)
        logger.addHandler(rf)

    return logger

def get_status_init():
    import shelve
    shelve_dict = shelve.open("/tmp/sheda_orbitcam_webserver.shelve")
    if shelve_dict:
        return shelve_dict["status_init"]
    else:
        return "unk"

# Create your views here.
def control(request):

    # Logger
    logger = create_logger(False, 'ShedaMotionOrbitManagerWebserver', True, logging_filename)

    orbit_drv  = ShedaOrbitDrv(logger);
    motion_drv = ShedaMotionDrv(logger)

    status_curr = "unk"
    status_init = "unk"

    cmd = request.POST['command']

    # relative movement
    if (cmd == "Left"):
        orbit_drv.moveLeft()
        return HttpResponseNotModified()
    elif (cmd == "Right"):
        orbit_drv.moveRight()
        return HttpResponseNotModified()
    elif (cmd == "Up"):
        orbit_drv.moveUp()
        return HttpResponseNotModified()
    elif (cmd == "Down"):
        orbit_drv.moveDown()
        return HttpResponseNotModified()
    # Movement reset
    elif (cmd == "ResetV"):
        orbit_drv.resetVer()
        return HttpResponseNotModified()
    elif (cmd == "ResetH"):
        orbit_drv.resetHor()
        return HttpResponseNotModified()
    # Absolute Positions
    elif (cmd == "0"):
        orbit_drv.movePosition(cmd)
        return HttpResponseNotModified()
    elif (cmd == "1"):
        orbit_drv.movePosition(cmd)
        return HttpResponseNotModified()
    elif (cmd == "2"):
        orbit_drv.movePosition(cmd)
        return HttpResponseNotModified()
    elif (cmd == "3"):
        orbit_drv.movePosition(cmd)
        return HttpResponseNotModified()
    elif (cmd == "4"):
        orbit_drv.movePosition(cmd)
        return HttpResponseNotModified()
    elif (cmd == "5"):
        orbit_drv.movePosition(cmd)
        return HttpResponseNotModified()
    elif (cmd == "6"):
        orbit_drv.movePosition(cmd)
        return HttpResponseNotModified()
    # Motion management
    elif (cmd == "LiveOn"):
        motion_drv.start(False)
        status_curr = motion_drv.status(True)
    elif (cmd == "LiveOff"):
        motion_drv.stop(False)
        status_curr = False
    elif (cmd == "DetectionOn"):
        motion_drv.start(True)
        status_curr = motion_drv.status(True)
    elif (cmd == "DetectionOff"):
        motion_drv.stop(True)
        status_curr = motion_drv.status(True)
    elif (cmd == "StatusRefresh"):
        status_curr = motion_drv.status(True)
    else:
        return HttpResponse("Error select the right button")

    # Get Ip/Port of the livestreaming
    ip, port = motion_drv.get_livestreamn_ip_port()
    live_ip_port = "{}:{}".format(ip, port)

    positions_names = ""
    for i in range(0,7):
       positions_names+=str(i)+": "+orbit_drv.getPosName(str(i))+", "

    status_init = get_status_init()

    return render(request, 'webcam/webcam.html', {'detection_init_status': status_init, 'detection_curr_status': status_curr, 'positions_names': positions_names, 'live_ip_port': live_ip_port})

def index(request):
    # Logger
    logger = create_logger(False, 'ShedaMotionOrbitManagerWebserver', True, logging_filename)

    orbit_drv  = ShedaOrbitDrv(logger);
    motion_drv = ShedaMotionDrv(logger)

    status_init = motion_drv.status(True)

    import shelve
    shelve_dict = shelve.open("/tmp/sheda_orbitcam_webserver.shelve")
    shelve_dict["status_init"] = status_init

    if status_init:
        # Cut watch if was active to avoid movement sending notification
        motion_drv.stop(True)

    status_curr = motion_drv.status(True)

    # Get Ip/Port of the livestreaming
    ip, port = motion_drv.get_livestreamn_ip_port()
    live_ip_port = "{}:{}".format(ip, port)

    positions_names = ""
    for i in range(0,7):
       positions_names+=str(i)+": "+orbit_drv.getPosName(str(i))+", "

    return render(request, 'webcam/webcam.html', {'detection_init_status': status_init, 'detection_curr_status': status_curr, 'positions_names': positions_names, 'live_ip_port': live_ip_port })
