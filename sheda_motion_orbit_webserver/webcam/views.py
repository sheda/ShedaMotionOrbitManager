from django.shortcuts import render

from django.http import *
from django.template import loader

from sheda_motion_orbit_drv.ShedaMotionOrbitDrv import ShedaOrbitDrv, ShedaMotionDrv

def get_status_init():
    import shelve
    shelve_dict = shelve.open("/tmp/sheda_orbitcam_webserver.shelve")
    if shelve_dict:
        return shelve_dict["status_init"]
    else:
        return "unk"

# Create your views here.
def control(request):
    orbit_drv  = ShedaOrbitDrv();
    motion_drv = ShedaMotionDrv()

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
        _, status_curr = motion_drv.status(True)
    elif (cmd == "LiveOff"):
        motion_drv.stop(False)
        status_curr = False
    elif (cmd == "DetectionOn"):
        motion_drv.start(True)
        _, status_curr = motion_drv.status(True)
    elif (cmd == "DetectionOff"):
        motion_drv.stop(True)
        _, status_curr = motion_drv.status(True)
    elif (cmd == "StatusRefresh"):
        _, status_curr = motion_drv.status(True)
    else:
        return HttpResponse("Error select the right button")

    positions_names = ""
    for i in range(0,7):
       positions_names+=str(i)+": "+orbit_drv.getPosName(str(i))+", "

    status_init = get_status_init()
    return render(request, 'webcam/webcam.html', {'detection_init_status': status_init, 'detection_curr_status': status_curr, 'positions_names': positions_names})

def index(request):
    orbit_drv  = ShedaOrbitDrv();
    motion_drv = ShedaMotionDrv() # verbosity to one
    _, status_init = motion_drv.status(True)

    import shelve
    shelve_dict = shelve.open("/tmp/sheda_orbitcam_webserver.shelve")
    shelve_dict["status_init"] = status_init

    if status_init:
        # Cut watch if was active to avoid movement sending notification
        motion_drv.stop(True)

    _, status_curr = motion_drv.status(True)

    positions_names = ""
    for i in range(0,7):
       positions_names+=str(i)+": "+orbit_drv.getPosName(str(i))+", "

    return render(request, 'webcam/webcam.html', {'detection_init_status': status_init, 'detection_curr_status': status_curr, 'positions_names': positions_names})
