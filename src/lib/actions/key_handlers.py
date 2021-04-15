import yaml
from subprocess import run

from src.config import default_pub_key, default_user, hosts
from src.lib.actions.host_handlers import get_host_info

# copies the default ssh public key to the provided KNOWN host
# meaning that you need to have that host added to the hosts file
# before running this option, this is a Linux only functionality,
# because the 'ssh-copy-id' program is Linux only, other than this,
# lzh will probably work in any OS that can use python.

# by default it passes the default pub key and to the default user into the provided
# hostname, if you want to copy an other public key or add the default key to an other user
# you can pass the -u and -k flags for that
def key_copy(command):
    with open(hosts) as stream:
        data_loaded = yaml.safe_load(stream)
        hosts_data = data_loaded['added_hosts']

    options = command['options']
    targets = command['targets']
    target_host_index = options.index('-c')
    target_host = targets[target_host_index]

    if '-k' in options:
        key_to_copy_index = options.index('-k')
        key_to_copy = targets[key_to_copy_index]
    else:
        key_to_copy = default_pub_key

    if '-u' in options:
        user_index = options.index('-u')
        user = targets[user_index]
    else:
        user = default_user

    host_info = get_host_info(hosts_data, target_host)
    host_ip = host_info['ip']
    cmd_to_send = f'ssh-copy-id -i {key_to_copy} {user}@{host_ip}'
    splited_cmd = cmd_to_send.split()
    # if trying to debug this feature, comment the line bellow, and uncoment the final
    # line, and see what the string looks like and try to run that command in 
    # a terminal to see what it tells you
    run(splited_cmd)
    #print(command_to_send)