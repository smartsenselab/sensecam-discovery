"""This module is used to find the ip related to each camera on the same network."""
import re
import netifaces
from typing import List

from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery


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

