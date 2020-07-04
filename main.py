import subprocess
import socket
import re

ip_regex = r'192\.168\.0\.[0-9]+'
mac_regex = r'[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}'
name_regex = r'\(.+\)'

def get_names(nmap_output: str) -> list:
    names = []
    for line in nmap_output.split('\n'):
        if 'MAC' in line:
            names.extend(re.findall(name_regex, line))
    return names





if __name__ == '__main__':
    result = subprocess.run(['nmap', '-sn', '192.168.0.0/24'], capture_output=True)
    try:
        nmap_output = result.stdout.decode('utf-8')
        ips = re.findall(ip_regex, nmap_output)
        macs = re.findall(mac_regex, nmap_output)

        names = get_names(nmap_output)

        guests = list(zip(ips, macs, names))
        for g in guests:
            print(g)
    except Exception as exc:
        print(exc)