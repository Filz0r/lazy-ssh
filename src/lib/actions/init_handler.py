import yaml
import os
from subprocess import run


# this not only is ran when the program is first ran, but also gives the ability to
# update the default settings
def init_handler(path=None):
    # this if statement is for when the user tries to run the -init option, I thought
    # it would be nice to have that feature built in, in case someone actually needs it
    # the reason why this block only has if statements is simple, if the user does not
    # give the expected input you just grab the path statement, and it shouldn't trigger
    # an circular import exception and it should still save the file in the expected place
    if path == None:
        from src.config import main_path as path
        question = input('Do you want to overwrite the hosts file?[y/N] ')
        if question.upper == 'Y':
            question = input('Are you sure about this?[y/N] ')
            if question.upper == 'Y':
                cmd = f"cp {path+'src/assets/default_hosts.yml'} {path+'hosts.yml'}"
                splited_cmd = cmd.split()
                run(splited_cmd)
    print('''Welcome to LZH!
This message appears when you first run LZH, or whenever you want to change the defaults.
Please follow these rules when setting up your config, this is essential for lzh to work properly:
1- The default range must end with an dot (Ex: 192.168.0.)
2- If you want to pass options to lzh, they need to be provided before the arguments or the program will break!
---->WARNING<----
This program was developed to simplify ssh connections inside an internal enviroment, it assumes that you know how
to properly lock your ssh server, rather than just relying on lzh's ability to copy a key to a server, you should also
block ssh from accepting passwords, and disable root login, while you might not need such implementations for an homelab
you do need them for internet facing servers.
Please secure your servers properly when using lzh for connections outside your lab enviroment.
If you don't want to configure all your connections manually, you can write your hosts file, you can check
the documentation for more information about this.
''')
    default_user = input('what\'s the default user?: ')
    default_range = input('what\'s the default IP range for your LAN?: ')
    default_key = input('what\'s the default ssh private key?: ')
    default_pub_key = input('what\'s the default ssh public key?: ')

    obj_to_save = {
        'initiated': True,
        'default-key': default_key,
        'default-pub-key': default_pub_key,
        'default-range': default_range,
        'default-user': default_user,
        'installed': False,
        'path': path
    }
    write_confirmation = input(f'''
default ip range: {default_range}
default user: {default_user}
default private key: {default_key}
default public key: {default_pub_key}
Do you want to save these settings?: [y/N]''')
    if write_confirmation.upper() == 'Y':
        with open(path + 'config.yml', 'w') as stream:
            yaml.dump(obj_to_save, stream)
            stream.close()
        with open(path + 'hosts.yml', 'r') as stream:
            data_loaded = yaml.safe_load(stream)
            # this block handles the editing of the hosts file
            # to add the known info to that file, if the file is at the
            # blank state, this block will convert everything into working
            # structure, this wouldn't be needed if I built the sample files better
            # BUT this way, I also made sure that even if someone tries to run it
            # without the proper structure, the program will convert that structure
            # into something it can work with, beware of file permissions, if you want
            # to use this as a system app before an install script is built,
            # and instalation functionalities are implemented on the program itself
            # this comment will stay like this until such features are implemented
            if data_loaded['known_info']['keys'] != None:

                if default_key not in data_loaded['known_info']['keys']:
                    data_loaded['known_info']['keys'].append(default_key)
                if default_user not in data_loaded['known_info']['users']:
                    data_loaded['known_info']['users'].append(default_user)

                with open(path + 'hosts.yml', 'w') as stream:
                    yaml.dump(data_loaded, stream)
                    stream.close()
            else:
                if data_loaded['known_info']['keys'] == None:
                    data_loaded['known_info']['keys'] = list()

                if data_loaded['known_info']['users'] == None:
                    data_loaded['known_info']['users'] = list()

                if data_loaded['known_info']['hosts'] == None:
                    data_loaded['known_info']['hosts'] = list()

                data_loaded['known_info']['keys'].append(default_key)
                data_loaded['known_info']['users'].append(default_user)

                with open(path + 'hosts.yml', 'w') as stream:
                    yaml.dump(data_loaded, stream)
                    stream.close()
        stream.close()

    else:
        print(
            'You need to confirm or the file will not be saved, please try again!'
        )
        return exit()
    return path + 'config.yml'