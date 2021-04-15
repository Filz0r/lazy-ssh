import yaml
from src.config import default_key, default_user, default_range, hosts
from src.lib.actions.connect import make_connection
from src.lib.actions.host_handlers import get_host_info, set_host_info

# this file is responsible for formating and sorting out the information
# stored in the hosts file, this file is splited in 2 main objects,
# known_info and added_hosts, the first will probably be moved to a separate
# file eventually, as this works as a cache for lzh, the second is where the
# actual information for connecting to each stored host is stored, everytime
# an host is added to added_hosts, all the information in known_info is also updated
# by doing this you are able to ssh into a machine using a 'pretty' hostname
# ex: lzh host1 instead of lzh host1.domain.tld, this pretty hostname is
# also what lzh looks for in the known_info when you try to connect, if lzh
# says he can't find the name, either you are trying to connect to an host
# that actually is not added, or you are trying to pass options and lzh
# can't find the right options
# use the '-a' option when you want to add an host
# use the '-n' option if you want to connect to an host with a different username
# or ssh key


# connect is what finds the host you want to connect to
def connect(targets,
            internal_options=None,
            external_options=None,
            command=None):

    with open(hosts, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        known_info = data_loaded['known_info']
        known_hosts = data_loaded['added_hosts']
        stream.close()
    # if no option is passed
    if internal_options == None or '-n' not in internal_options:
        # call target_handler and find all known info for this host, and pass other internal options
        target = target_handler(targets, known_info, internal_options)
        # that object will be passed to get_host_info, responsible for grabbing the previously saved
        # information, if he can't find this information, lzh will prompt you to add that host
        host_info = get_host_info(known_hosts, target)
    else:
        # if the handy '-n' option is passed, lzh will know that the host will be whatever argument
        # saved inside command['targets'], with the same list index as the option '-n'
        # and will actually use that to find the host info more acuratly
        host_index = command['options'].index('-n')
        host = command['targets'][host_index]
        host_info = get_host_info(known_hosts, host)
    # after all that stuff, call the make_connection function an connect with the provided options.
    return make_connection(host_info=host_info,
                           internal_options=internal_options,
                           external_options=external_options,
                           command=command)

# literally just looks for the provided information in the known_info object.
# if it can't find any you will be asked to add a new host
def target_handler(targets, info, internal_options=None):
    known_hosts = info['hosts']
    known_users = info['users']
    known_keys = info['keys']
    if known_hosts == None:
        print(
            'This target is not inside the hosts file, initiating add new host functionality'
        )
        return set_host_info(targets, internal_options)
    else:
        actual_target = [i for i in targets if i in known_hosts]
        actual_user = [i for i in targets if i in known_users]
        actual_key = [i for i in targets if i in known_keys]
        target = str(actual_target)[2:-2]
        user = str(actual_user)[2:-2]
        key = str(actual_key)[2:-2]
        if len(user) == 0 and len(key) == 0 and len(target) > 0:
            return target
        else:
            print(
                'This target is not inside the hosts file, initiating add new host functionality'
            )
            return set_host_info(targets, internal_options)
        result = [target, user, key]
        return result

# built to handle the passing of other ports used for ssh, this does not call target_handler, as
# the target is deconstructed and found before getting here, so lzh will just look for the saved info
# and use that to connect to the machine
def connect_port(targets,
                 internal_options=None,
                 external_options=None,
                 command=None):
    target = targets[0]
    port = targets[1]
    with open(hosts, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        known_hosts = data_loaded['added_hosts']
        stream.close()
    host_info = get_host_info(known_hosts, target)
    return make_connection(host_info,
                           internal_options=internal_options,
                           external_options=external_options,
                           port=port,
                           command=command)
