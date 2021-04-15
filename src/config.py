import os
import yaml
from time import sleep

# makes the script path a aware in order to read the config and hosts file
path = os.path.realpath(__file__)
main_path = os.path.realpath(__file__)[:len(path) - 13]
if os.path.exists(main_path + 'config.yaml'):
    config = main_path + 'config.yaml'
elif os.path.exists(main_path + 'config.yml'):
    config = main_path + 'config.yml'
else:
    print('it seems like the script can\'t find a config.yaml/yml file!')
    exit()

# reads the config file the yaml is just for the memes
# I might change this to a config.ini set up later if it proves easier to write to.
# the only reason I need this is in order to handle the hosts file later on
# since this object is smaller it was better to start from here
with open(config, 'r') as stream:
    data_loaded = yaml.safe_load(stream)
    # these are the default values that are loaded from config.yml or config.yaml
    default_key = data_loaded['default-key']
    default_pub_key = data_loaded['default-pub-key']
    dafault_range = data_loaded['default-range']
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
        
# This is to check for an hosts file, following the same logic as the config file
# but since I don't want to make the config check to complex with a multiple if statement
# I think this is one of those situations where repeating yourself is acceptable     
if os.path.exists(main_path + 'hosts.yaml'):
    hosts = main_path + 'hosts.yaml'
elif os.path.exists(main_path + 'hosts.yml'):
    hosts = main_path + 'hosts.yml'
else:
    print('it seems like the script can\'t find a hosts.yaml/yml file!')
    exit()