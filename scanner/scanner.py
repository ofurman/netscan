import subprocess
import re

ip_regex = r'192\.168\.0\.[0-9]+'
mac_regex = r'[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}'
name_regex = r'\(.+\)'

class Scanner:
    """Class that scanning network and looking for new guests
    """

    def __init__(self, local_network_addr: str = '192.168.0.0', mask: str = '/24'):
        self.net_addr = local_network_addr + mask

    def _get_names(self, nmap_output: str) -> list:
        """Extract names from nmap output
        Args:
            nmap_output (str): nmap output
        Returns:
            list: list of dns names
        """
        names = []
        for line in nmap_output.split('\n'):
            if 'MAC' in line:
                names.extend(re.findall(name_regex, line))
        return names

    def get_guests(self) -> dict:
        """Looking for all devices in the network
        Returns:
            list[tuple[ip,mac,dns_name]]: [description]
        """

        result = subprocess.run(['nmap', '-sn', self.net_addr], capture_output=True)
        try:
            nmap_output = result.stdout.decode('utf-8')
            ips = re.findall(ip_regex, nmap_output)
            macs = re.findall(mac_regex, nmap_output)

            names = self._get_names(nmap_output)

            guests = dict(zip(macs, names))
            return guests
        except Exception as exc:
            return exc


if __name__ == "__main__":
    s = Guests()
    g = s.get_guests()
    print(g)
