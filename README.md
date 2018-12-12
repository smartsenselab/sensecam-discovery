# SenseCam Discovery
This is a package to discover all onvif devices on your network.
## Installation
Install the package through pip:
````
pip install sensecam-discovery
````
## Execution
To execute the command that discover all cameras:
````
from sensecam_discovery import SenseCamDiscovery
SenseCamDiscovery.ws_discovery()
````
To execute the comand that shows information about the cameras:
````
from sensecam_discovery import CameraONVIF
Class = CameraONVIF(camera_ip, user, password)
````