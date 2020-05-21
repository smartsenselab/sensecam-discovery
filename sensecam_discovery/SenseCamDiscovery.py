"""This module is used to get the ip and the information related to
each camera on the same network."""
import re
import netifaces
from typing import List

from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from onvif import ONVIFCamera

def discover(scope = None) -> List:
    """Discover cameras on network using onvif discovery.

    Returns:
        List: List of ips found in network.
    """
    # Get the scopes from the IPs returned by the bash command `hostname -I`.
    if (scope == None):
        ips = list()
        for iface in netifaces.interfaces():
            if(netifaces.AF_INET in netifaces.ifaddresses(iface)):
                ips.append(netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr'])
        scope = ['.'.join(ip.split('.')[:2]) for ip in ips]
    # Run WSDiscovery to search the IP from the cameras.
    wsd = WSDiscovery()
    wsd.start()
    ret = wsd.searchServices()
    wsd.stop()
    # Get just the services from onvif cameras.
    onvif_services = [s for s in ret if str(s.getTypes()).find('onvif') >= 0]
    # Extract the IPs of the onvif cameras.
    urls = [ip for s in onvif_services for ip in s.getXAddrs()]
    ips = [ip for url in urls for ip in re.findall(r'\d+\.\d+\.\d+\.\d+', url)]
    # Return a list with the IPs that correspond to the scope.
    lst = [ip for ip in ips if any(ip.startswith(sp) for sp in scope)]
    return sorted(lst)


class Camera:
    """This class is used to get the information from all cameras discovered on this specific
    network."""

    def __init__(self, ip, user, password):
        """Constructor.

        Args:
            ip (str): Ip of the camera.
            user (str): Onvif login.
            password (str): Onvif password.
        """
        self._mycam = ONVIFCamera(ip, 80, user, password, no_cache = True)
        self._camera_media = self._mycam.create_media_service()
        self._camera_media_profile = self._camera_media.GetProfiles()[0]

    @property
    def hostname(self) -> str:
        """Find hostname of camera.

        Returns:
            str: Hostname.
        """
        resp = self._mycam.devicemgmt.GetHostname()
        return resp.Name

    @property
    def manufacturer(self) -> str:
        """Find manufacturer of camera.

        Returns:
            str: Manufacturer.
        """
        resp = self._mycam.devicemgmt.GetDeviceInformation()
        return resp.Manufacturer

    @property
    def model(self) -> str:
        """Find model of camera.

        Returns:
            str: Model.
        """
        resp = self._mycam.devicemgmt.GetDeviceInformation()
        return resp.Model

    @property
    def firmware_version(self) -> str:
        """Find firmware version of camera.

        Returns:
            str: Firmware version.
        """
        resp = self._mycam.devicemgmt.GetDeviceInformation()
        return resp.FirmwareVersion

    @property
    def mac_address(self) -> str:
        """Find serial number of camera.

        Returns:
            str: Serial number.
        """
        resp = self._mycam.devicemgmt.GetDeviceInformation()
        return resp.SerialNumber

    @property
    def hardware_id(self) -> str:
        """Find hardware id of camera.

        Returns:
            str: Hardware Id.
        """
        resp = self._mycam.devicemgmt.GetDeviceInformation()
        return resp.HardwareId

    @property
    def resolutions_available(self) -> List:
        """Find all resolutions of camera.

        Returns:
            tuple: List of resolutions (Width, Height).
        """
        request = self._camera_media.create_type('GetVideoEncoderConfigurationOptions')
        request.ProfileToken = self._camera_media_profile.token
        config = self._camera_media.GetVideoEncoderConfigurationOptions(request)
        return [(res.Width, res.Height) for res in config.H264.ResolutionsAvailable]

    @property
    def frame_rate_range(self) -> int:
        """Find the frame rate range of camera.

        Returns:
            int: FPS min.
            int: FPS max.
        """
        request = self._camera_media.create_type('GetVideoEncoderConfigurationOptions')
        request.ProfileToken = self._camera_media_profile.token
        config = self._camera_media.GetVideoEncoderConfigurationOptions(request)
        return config.H264.FrameRateRange.Min, config.H264.FrameRateRange.Max

    @property
    def date(self) -> str:
        """Find date configured on camera.

        Returns:
            str: Date in string.
        """
        datetime = self._mycam.devicemgmt.GetSystemDateAndTime()
        return datetime.UTCDateTime.Date

    @property
    def time(self) -> str:
        """Find local hour configured on camera.

        Returns:
            str: Hour in string.
        """
        datetime = self._mycam.devicemgmt.GetSystemDateAndTime()
        return datetime.UTCDateTime.Time

    @property
    def is_ptz(self) -> bool:
        """Check if camera is PTZ or not.

        Returns:
            bool: Is PTZ or not.
        """
        resp = self._mycam.devicemgmt.GetCapabilities()
        return bool(resp.PTZ)
