import socket

import IPy             # pip install ipy
import geoip2.database # pip install geoip2


def is_reversed_ip(ip):
    reversed = [
        '10.0.0.0/8',
        '172.16.0.0/12',
        '192.168.0.0/16'
    ]

    try:
        for block in reversed:
            ip_block = IPy.IP(block)
            if ip in ip_block:
                return True
    except Exception:
        return False

    return False

def ipchk(ip):

    ipv6 = False
    ipfamliy = socket.AF_INET

    ip = ip.strip()

    if ':' in ip:
        ipv6 = True
        ipfamliy = socket.AF_INET6

    # ip/mask format
    if '/' in ip:
        data = ip.split('/')
        if len(data) != 2:
            return False, "Invalid ip address %s" % ip
        ip = data[0]
        mask = data[1]

    try:
        socket.inet_pton(ipfamliy, ip)
    except Exception as e:
        return False, "Invalid ip address %s" % ip


    return True, "success"


def geoip2Load():
    reader = geoip2.database.Reader('conf/geoip2/GeoLite2-Country.mmdb')
    return reader


def geoip2Search(reader, ip):
    try:
        response = reader.country(ip)
    except Exception as e:
        return 'N/A'

    return '[%s]%s' % (response.country.iso_code, response.country.name)


def geoip2Close(reader):
    reader.close()

if __name__ == '__main__':
    reader = geoip2Load()
    adr = geoip2Search(reader, '10.30.1.20')
    print(adr)

    adr = geoip2Search(reader, '223.71.139.100')
    print(adr)

