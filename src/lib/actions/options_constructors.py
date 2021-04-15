# this literally constructs objects that are given to the options handler
# maybe doing this with classes would 
from src.lib.options.help_menu import help_text
def help_menu():
    option = '-h'
    functionality = 'internal'
    text = help_text()
    return option, functionality, text

def add():
    option = '-a'
    functionality = 'internal'
    return option, functionality

def debug_short():
    option = '-v'
    functionality = 'external'
    return option, functionality

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

def name():
    option = '-n'
    functionality = 'internal'
    return option, functionality

def port():
    option = '-p'
    functionality = 'external'
    return option, functionality

def copy_key():
    option = '-c'
    functionality = 'external'
    return option, functionality

def script_init():
    option = '-init'
    functionality = 'internal'
    return option, functionality
# does literally nothing at the moment, this is beyond the scope of this project at the moment
# but if this concept works, this is the first thing to be implemented.
def install():
    return 'symlinks lzh.py to /usr/bin/lzh and creates and moves itself to the /etc/lzh folder'
