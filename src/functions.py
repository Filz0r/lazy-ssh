# I mean I think this is what I'm going to do with it, just to keep it
# more tiddy and easier to update and add modules later, rather 
# have 100 imports in here than 1000 lines
def help():
    option = '-h'
    functionality = 'internal'
    return option, functionality

def add():
    option = '-a'
    functionality = 'internal'
    return option, functionality

def debug_short():
    option = '-v'
    functionality = 'external'
    return option, functionality

# this one might be a mess because of the multiple options capability
# maybe implementing it as a -- command only might work, idk i'll look into it
def debug_long():
    option = '-vvv'
    functionality = 'external'
    return option, functionality

def default_user():
    option = '-u'
    functionality = 'internal'
    return option, functionality

def default_key():
    option = '-k'
    functionality = 'internal'
    return option, functionality

def default_range():
    option = '-r'
    functionality = 'internal'
    return option, functionality

def no_key():
    option = '-n'
    functionality = 'internal'
    return option, functionality

def port():
    option = '-p'
    functionality = 'external'
    return option, functionality

# commands like this one need to be worked for when they are called specifically
# for now only option and functionality are being passed down to the global functions
def copy_key():
    option = '-c'
    functionality = 'external'
    command = 'ssh-copy-id -i'
    return option, functionality

def install():
    return 'symlinks lzh.py to /usr/bin/lzh and creates and moves itself to the /etc/lzh folder'
