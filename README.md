# SenseCam Discovery - Camera Discovery Package

SenseCam Discovery is a Python tool that is used to discover all Onvif cameras available on a specific network. The purpose is to easily provide an accessible way to find out which IP each camera has, and then use this IP to get all information for this camera, such as hostname, manufacturer, model, firmware version, MAC address, hardware ID, all resolutions available, frame rate range, date, time and if it’s PTZ or not.

## Installation
Install the package through pip:
````
pip install sensecam-discovery
````
## Execution
To execute the command that discover all cameras:
````
import sensecam_discovery
sensecam_discovery.discover()
````
To execute the comand that shows information about the cameras:
````
from sensecam_discovery import Camera
camera = Camera(camera_ip, user, password)
````