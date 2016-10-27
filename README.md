# Sheda Motion Orbit Manager

ShedaMotionOrbitManager is a tool used to encapsulate using of a Logitech Orbit USB Webcam for:
-  Home security camera streaming - start/stop the live streaming, Through a WebPage
-  Home security camera motion detection - start/stop the watch, report through email with picture and video
-  Moving the USB Orbit Camera - freely(left-right/up-down) or to 7 determined positions for quick access

Utilization can be done through script comand line or by webpage access.

### Third party tools
ShedaMotionOrbitManager is writtent in python 2.7 and rely on several third party tools:
- [Django] framework for webserver
- [Motion] for camera live streaming and motion detection
- [uvcdynctrl] for Logitech Orbit Movement control
- [nohup] for background running

### Version
1.1

### License
Gnu GPLv3

### Installation

1- You need apt or any package manager to install required third party, following exemple of installatio non debian/ubuntu
```sh
$ apt-get install coreutils
$ apt-get install uvcdynctrl
$ apt-get install motion
$ apt-get install django
```

2- Verify thrid every thing well installed:

uvcdynctrl:
```sh
$ uvcdynctrl -s "Pan, Reset" -- 1
$ uvcdynctrl -s "Tilt, Reset" -- 1

$ uvcdynctrl -s "Pan, Relative" -- -500
$ uvcdynctrl -s "Pan, Relative" -- +500

$ uvcdynctrl -s "Tilt, Relative" -- -500
$ uvcdynctrl -s "Tilt, Relative" -- +500
```
motion:
```sh
$ motion
```

3- Install package
```sh
$ python setup.py install
```

4- Verify that configs files where installed, else install those:
```sh
$ sudo cp configs/motion.conf /etc/motion/motion.conf
$ sudo cp configs/sheda_motion_orbit_manager.conf /etc/sheda_motion_orbit_manager.conf
```

### Toying
This will move the camera to the watching position(see /etc/sheda_motion_orbit_manager.conf) then launch the server then launch the watch:
```sh
$ sheda_motion_orbit_manager start -w -m
```
This will stop the watch then move the camera to the off position(see /etc/sheda_motion_orbit_manager.conf).
```sh
$ sheda_motion_orbit_manager stop -w -m
```
note:  Moving to the off position can be used to physically mask camera view (should have rename this option -p for paranoid)

### More information
Interesting WebPages url/port:
- Ip where motion live stream the camera is http://127.0.0.1:8081
- Ip where motion is crontrolable is http://127.0.0.1:8080
- IP for Django WebServer is http://127.0.0.1:8090/webcam

Interesting files for webserver
- /var/run/sheda_motion_orbit_webserver.pid
- /var/log/sheda_motion_orbit_manager_webserver.log

Interesting file for script
- /var/run/sheda_motion_orbit_manager.pid
- /var/log/sheda_motion_orbit_manager.log

For more info on [sheda.fr]

### Todos

 - IP watch disable if some IP appear on the network
 - Make all IP configurables this break server

[Django]: https://www.djangoproject.com/
[Motion]:http://lavrsen.dk/foswiki/bin/view/Motion/WebHome
[uvcdynctrl]: https://packages.debian.org/sid/utils/uvcdynctrl
[nohup]: http://manpages.ubuntu.com/manpages/precise/man1/nohup.1.html
[sheda.fr]: http://www.sheda.fr
