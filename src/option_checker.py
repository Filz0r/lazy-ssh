#import asyncio
from src.args import short_checker, long_checker
#
# The script functions with args and long args, args start with - and long args start with --
# if the arguments provided don't meet this requirement then send them over to an other funciton
# that checks if the user is trying to connect to a known ssh connection, if it's not known, show the help menu
#
from src.connections import connect

def option_checker(args):
    obj = argument_converter(args)

    if isinstance(obj, str):
        first_arg = obj
        option = ''
        if first_arg.startswith('-') and '--' not in first_arg:
            # send to short checker
            option = short_checker(first_arg)
        elif first_arg.startswith('--'):
            # send to long checker
            option = long_checker(first_arg)
        else:
            if option == '':
                return connect(first_arg)
            else:
                print('you need to privide an valid argument!')

    elif isinstance(obj, tuple) and len(obj) == 2:
        (first_arg, second_arg) = obj
        if first_arg.startswith('-') and '--' not in first_arg or second_arg.startswith('-') and '--' not in second_arg:
            # basically I'm doing this check in order to allow users to pass flags
            # and hostnames or ip terminations without an order
            if first_arg.startswith('-'):
                option = short_checker(first_arg)
                return connect(second_arg, option)
            elif second_arg.startswith('-'):
                option = short_checker(second_arg)
                return connect(first_arg, option)
            else:
                print('this is that mad error you must not forget to handle')
        elif first_arg.startswith('--') or second_arg.startswith('--'):
            # basically I'm doing this check in order to allow users to pass flags
            # and hostnames or ip terminations without an order
            if first_arg.startswith('--'):
                return long_checker(first_arg)
            elif second_arg.startswith('--'):
                return long_checker(second_arg)
            else:
                print('this is yet an other mad error you must not forget to handle')
        else:
            # try to ping that argument, if it fails, warn the user about it and
            # send the help menu
            print('you need to privide an argument')

    elif isinstance(obj, tuple) and len(obj) == 4:
        targets = list(obj)
        for args in obj:
            if args.startswith('-') and '--' not in args:
                option = args
        targets.remove(option)
        options = short_checker(option)
        return connect(targets, options)


def argument_converter(args):
    # this needs further development for now you can only pass 2 arguments to the script
    # but maybe this is a good thing, only time will tell
    # args[0] is the command you typed in the shell to run the script
    # either lzh or /path/to/script/lzh.py, if you run it like this:
    # 'python3 lzh.py --help' it should probably break its not intended to work like this.
    passed_args = args[1:]
    arg_size = len(passed_args)
    if arg_size == 1:
        try:
            # try to convert argument into string
            first_arg = str(passed_args[0])
            # return it as a string
            return first_arg
        except:
            print('There was an error trying to convert your arguments!')
    elif arg_size == 2:
        try:
            #tries to convert the arguments into strings
            first_arg = str(passed_args[0])
            second_arg = str(passed_args[1])
            # returns them as tuples
            return first_arg, second_arg
        except:
            print('There was an error trying to convert your arguments!')
    elif arg_size == 4:
            first_arg = str(passed_args[0])
            second_arg = str(passed_args[1])
            third_arg = str(passed_args[2])
            fourth_arg = str(passed_args[3])
            # returns them as tuples
            return first_arg, second_arg, third_arg, fourth_arg
    else:
        # this will need to open the help menu later down the line
        print(passed_args, arg_size)
        print('idiot you need to provide arguments')

