from subprocess import run

# making the connections with the gathered information, this is function is responsible for making
# all connections, notice how port is set to 22 by default, this means that unless you specify
# a port when trying to connect, lzh will try to connect on the default ssh port, port 22

# host info must always be passed to this function, the other options are optional, and
# are used to handle options that are passed to lzh, lzh then builds a string that
# consists on the command that you would usually pass to ssh according to the options
# that are passed to lzh


def make_connection(host_info,
                    internal_options=None,
                    external_options=None,
                    port=22,
                    command=None):
    if command != None:
        command_targets = command['targets']
        command_options = command['options']
        if '-k' in command_options:
            key_index = command_options.index('-k')
            host_info['key_path'] = command_targets[key_index]
        if '-u' in command_options:
            user_index = command_options.index('-u')
            host_info['user'] = command_targets[user_index]

    if host_info['key_path'] != None and port == 22:
        final_comand = f"ssh {host_info['user']}@{host_info['ip']} -i {host_info['key_path']} "
    elif host_info['key_path'] != None and port != 22:
        final_comand = f"ssh -i {host_info['key_path']} {host_info['user']}@{host_info['ip']} -p {port}"
    else:
        final_comand = f"ssh {host_info['user']}@{host_info['ip']}"

    if '-d' in command_options:
        final_comand = final_comand + ' -v'
    elif '-ddd' in command_options:
        final_comand = final_comand + ' -vvv'
    # keep this here for debugging reasons, it's easier to find out what's breaking the program this way
    # print(final_comand)
    splited_cmd = final_comand.split()
    return run(splited_cmd)
