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
import sensecam_discovery
sensecam_discovery.discover()
````
To execute the comand that shows information about the cameras:
````
from sensecam_discovery import Camera
camera = Camera(camera_ip, user, password)
````