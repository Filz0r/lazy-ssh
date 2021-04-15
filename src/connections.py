
from subprocess import run
# don't forget to clean up the import bellow, you only need to import the used vars
# but for development reasons this way is better
from src.config import default_key, default_user
from src.args import args_separator

def connect(target, options = ''):
    if isinstance(target, list) and isinstance(options, list):
        for option in options:
            args = args_separator(option)
            if args[1] == 'internal':
                internal_functionalities(target, option)
            elif args[1] == 'external':
                external_functionalities(target, option)
            else:
                print(option, 'this is the else')
    elif not isinstance(target, list) and isinstance(options, list):
        print('target is not list', target, options)
    else:
        run_functionalities(target)

def internal_functionalities(target, options=''):
    print('internal', target, options)
    
def external_functionalities(target, options=''):
    print('external', target, options)
    
def run_functionalities(target, options=''):
    if isinstance(options, str):
        command = f'ssh -i {default_key} {default_user}@{target}'
        splited_cmd = command.split()
        return run(splited_cmd)
    else:
        print('yet an other else output')



# this function handles the connection aspects of the program, basically it's
# responsible for runs the passed arguments properly
#
# the option_checker.py and args.py are responsible for making sure the arguments
# that are passed don't break the script, I could probably cram all of these in the
# same file, but for the sake of making future updates easier, I opted to do things
# this way, if anyone knows a better way of doing this, holla at me, or not, idc

    # handles the options arguments
    # without this the script crashes when no options are passed
    # the expected output is to be able to just send an ip termination or hostname
    # in order to connect, so this is necessary, but probably needs optimization.
    #if options == '':
    #    option = None
    #    functionality = 'run'
    #elif isinstance(target, list):
    #    if isinstance(options, list):
    #        for option in options:
    #            test = args_separator(option)
    #            print(test)
    #        functionality='none'
            #option, functionality = options
            
    #else:
    #    option, functionality = options
    
    # the functions present in src/functions.py alwa
    #
    #
    #if functionality == 'internal':
    #    print('internal', target, option)
    #elif functionality == 'external':
    #    print('external', target, option)
    # this handles the actual connection side of things
    # if I can implement the worker functions like I did until now
    # this means that only the statement above this block comment needs to 
    # be improved, when I get to the part of adding the flags to this final
    # output, wish me luck
    #elif functionality == 'run':
    
        