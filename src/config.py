import os
import yaml
from subprocess import run

from src.lib.actions.init_handler import init_handler

# makes the script path a aware in order to read the config and hosts file
path = os.path.realpath(__file__)
main_path = os.path.realpath(__file__)[:len(path) - 13]
# This is to check for an hosts file, if the script can't find it, it will
# be copied from the assets folder inside src
if os.path.exists(main_path + 'hosts.yaml'):
    hosts = main_path + 'hosts.yaml'
elif os.path.exists(main_path + 'hosts.yml'):
    hosts = main_path + 'hosts.yml'
else:
    cmd = f"cp {main_path+'src/assets/default_hosts.yml'} {main_path+'hosts.yml'}"
    splited_cmd = cmd.split()
    run(splited_cmd)
    hosts = main_path + 'hosts.yml'
# checks if the config.yaml exists, if it does not, it calls the
# init_handler function that builds the file, a default one is 
# also stored in the src.assets directory

if os.path.exists(main_path + 'config.yaml'):
    config = main_path + 'config.yaml'
elif os.path.exists(main_path + 'config.yml'):
    config = main_path + 'config.yml'
else:
    config = init_handler(main_path)

# reads the config file the yaml is just for the memes
# I might change this to a config.ini set up later if it proves easier to write to.
# the only reason I need this is in order to handle the hosts file later on
# since this object is smaller it was better to start from here
with open(config, 'r') as stream:
    data_loaded = yaml.safe_load(stream)
    # these are the default values that are loaded from config.yml or config.yaml
    default_key = data_loaded['default-key']
    default_pub_key = data_loaded['default-pub-key']
    default_range = data_loaded['default-range']
    default_user = data_loaded['default-user']
    config_path = data_loaded['path']
    stream.close()
# checks is the config path saved in the config file is the same as the path
# where the script runs from, if it's not update it to the correct one
if config_path != main_path:
    data_loaded['path'] = main_path
    with open(config, 'w') as stream:
        yaml.dump(data_loaded, stream)
        stream.close()
