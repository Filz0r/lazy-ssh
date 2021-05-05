import socket
from src.config import default_range


# Utility functions built to remove repeting myself when trying to handle arguments and options
# right now it mostly does ip address handling, but I still need to make sure I'm using these
# functions whenever possible, before seeing if I need to add any more stuff to here that is.
def ip_validator(ip):
    try:
        if socket.inet_aton(ip):
            return True
        else:
            return False
    except:
        return False


def ip_check(arg):
    try:
        ip = int(arg)
        full_ip = default_range + str(ip)
        if ip_validator(full_ip) == True:
            return full_ip
        else:
            print('you need to provide a valid IP termination!')
            return exit()
    except:
        if ip_validator(arg) == True:
            ip = arg
            return ip
        else:
            print('You need to provide a valid IP!')
            return exit()
