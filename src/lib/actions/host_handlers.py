from src.config import default_range, default_user, default_key
from src.config import hosts as hostFile
import socket, yaml
from src.lib.utils import ip_validator, ip_check
from src.lib.actions.connect import make_connection

# this file is where all the functions used to handle hosts and connections
# are stored, these get used in multiple files, so instead of spliting them into
# individual files inside this directory, I put them all in the same file,
# as a reminder to myself that this file will most likely need to be reworked
# in future releases of this program, mostly because I use 2 functions to do basically
# the same thing, host_entry_builder, does the same thing as host_entry_builder_verbose
# the only difference is that one accepts options and the other does not.
# the first one handles all the options and is only ran when the -a flag is passed to lzh
# you might get the 'you need to pass the -a flag before the hostname/IP for this functionality to work'
# message when using LZH, this means that the program thinks that you are trying to add a host, when you
# could actually be trying to connect to an other host with options being passed, if this is the case
# pass the -n before the name used to connect to that machine.
# The second one is what runs when you input '$lzh 192.168.1.100' and 192.168.1.100 is not inside the hosts file
# it does what the function name says it does, it adds the host in a verbose way asking you informations about that
# host, just keep in mind that you can only either store the default key or no ssh key at all when using this functionality
# unlike the other, that expects you to be using an ssh key by default.


def get_host_info(hosts, target):
    if target in hosts:
        ip = hosts[target]['ip']
        username = hosts[target]['username']
        key = hosts[target]['key']
        ssh_key = hosts[target]['ssh-key']
        result = {'ip': ip, 'user': username, 'key': key, 'key_path': ssh_key}
        return result
    else:
        print(
            'This target is not inside the hosts file, initiating add new host functionality'
        )
        return set_host_info(target)


def set_host_info(arguments, internal_options=None):
    if internal_options != None:
        return host_entry_builder(arguments, internal_options)
    else:
        argument = str(arguments[0])
        try:
            ip = int(argument)
            if isinstance(ip, int):
                true_ip = default_range + str(ip)
                return host_entry_builder_verbose(None, true_ip)
            else:
                print('I broke :(')
                exit()
        except:
            print(
                'This host is not an IP termination, it\'ll be added as the hostname in the hosts file'
            )
            question = input('Please provide an IP or IP termination: ')
            true_ip = ip_check(question)
            return host_entry_builder_verbose(argument, true_ip)


def host_entry_builder(targets, internal_options=''):
    host_to_add = dict()
    i = 0
    if '-a' not in internal_options:
        print(
            'you need to pass the -a flag before the hostname/IP for this functionality to work'
        )
        return exit()

    while i < len(internal_options):
        if '-a' in internal_options[i]:
            name_index = internal_options.index('-a')
            name = targets[name_index]
            host_to_add['name'] = name
        if '-u' in internal_options[i]:
            user_index = internal_options.index('-u')
            user = targets[user_index]
            host_to_add['username'] = user
        if '-k' in internal_options[i]:
            key_index = internal_options.index('-k')
            key = targets[key_index]
            ssh_key = key
            host_to_add['key'] = True
            host_to_add['ssh-key'] = ssh_key
        i += 1
    try:
        ip = int(host_to_add['name'])
        if isinstance(ip, int):
            question = input('Please provide the FQDN for this machine: ')
            name = question.split('.')[0]
            host_to_add['ip'] = default_range + str(ip)
            host_to_add['name'] = name
            host_to_add['hostname'] = question
    except:
        ip_test = ip_validator(host_to_add['name'])
        if ip_test == True:
            question = input('Please provide the FQDN for this machine: ')
            name = question.split('.')[0]
            host_to_add['ip'] = host_to_add['name']
            host_to_add['name'] = name
            host_to_add['hostname'] = question
        else:
            question1 = input('Is this the FQDN? [Y/n]: ')
            if question1.upper() == 'Y':
                hostname = name
                name = hostname.split('.')[0]
            elif question1.upper() == 'N':
                question = input('Please provide the FQDN: ')
                hostname = question
            else:
                hostname = name
                name = hostname.split('.')[0]

            question2 = input(
                'Please provide the IP address or termination for this machine: '
            )
            ip = ip_check(question2)
            host_to_add['ip'] = ip
            host_to_add['name'] = name
            host_to_add['hostname'] = hostname
    if 'key' not in host_to_add:
        host_to_add['key'] = False
        host_to_add['ssh-key'] = None
    if 'username' not in host_to_add:
        host_to_add['username'] = default_user

    name = host_to_add['name']
    del host_to_add['name']

    with open(hostFile, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        added_hosts = data_loaded['added_hosts']
        known_info = data_loaded['known_info']
        with open(hostFile, 'w') as stream:
            added_hosts[name] = host_to_add
            if name not in known_info['hosts']:
                known_info['hosts'].append(name)
            if host_to_add['ssh-key'] != None and host_to_add[
                    'ssh-key'] not in known_info['keys']:
                known_info['keys'].append(host_to_add['ssh-key'])
            if host_to_add['username'] not in known_info['users']:
                known_info['users'].append(host_to_add['username'])

            yaml.dump(data_loaded, stream)
            stream.close()
        stream.close()
    print(
        f"You have added {name} to your hosts file you can now connect to that machine using lzh!"
    )
    return exit()


def host_entry_builder_verbose(argument, ip_addr):
    print(argument, ip_addr)
    ip = ip_addr
    ip_check = ip_validator(ip)
    if ip_check == True:
        hostname = input('What is the FQDN of this machine?(hostname): ')
        if len(hostname) < 1:
            print('You need to provide a FQDN, please try again')
            return exit()
        if argument == None: argument = hostname.split('.')[0]
        username = input('Do you want to use the default user? [Y/n]')
        if username.upper() == 'Y':
            username = default_user
        elif username.upper() == 'N':
            username = input('What is the username?: ')
        else:
            username = default_user

        key = input('Do you want to login with the default ssh key?[Y/n]: ')
        if key.upper() == 'Y':
            key = True
            ssh_key = default_key
        elif key.upper() == 'N':
            key = False
            ssh_key = None
        else:
            key = True
            ssh_key = default_key

        obj_to_add = {
            'hostname': hostname,
            'ip': ip,
            'username': username,
            'key': key,
            'ssh-key': ssh_key,
        }
        print(obj_to_add)
        with open(hostFile, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
            added_hosts = data_loaded['added_hosts']
            known_info = data_loaded['known_info']
            if added_hosts == None:
                data_loaded['added_hosts'] = dict()
            if known_info['hosts'] == None or known_info[
                    'users'] == None or known_info['keys'] == None:
                data_loaded['known_info']['hosts'] = list()
                data_loaded['known_info']['users'] = list()
                data_loaded['known_info']['keys'] = list()
            with open(hostFile, 'w') as stream:
                data_loaded['added_hosts'][argument] = obj_to_add
                print(added_hosts)
                print(data_loaded)
                if argument not in data_loaded['known_info']['hosts']:
                    data_loaded['known_info']['hosts'].append(argument)

                yaml.dump(data_loaded, stream)
                stream.close()
            stream.close()
        print(
            f"You have added {hostname} to your hosts file you can now connect to that machine using lzh!"
        )
        return exit()

    else:
        print('You did not provide an valid IP, please try again')
        exit()