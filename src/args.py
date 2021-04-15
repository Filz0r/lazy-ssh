# yes import everything from the functions file, the selector var
# works like an switch statement
from src.functions import *

print(options.functionality, external_options.functionality)
def short_checker(arg):
    # these are all the available options the program accepts
    selector = {
        '-h': help(),
        '-a': add(),
        '-d': debug_short(),
        '-ddd': debug_long(),
        '-u': default_user(),
        '-k': default_key(),
        '-r': default_range(),
        '-n': no_key(),
        '-p': port(),
        '-c': copy_key()
    }
    # remove the - from the argument and save it as options
    options = arg[1:]
    # if options not one then sort out the individual flags
    if len(options) != 1:
        # these are the flags that we are going to check
        options_to_pass = list()
        # this is the final object to pass down to the 
        list_to_pass = list()
        # uhh its a i variable duuuh
        i = 0
        # for each letter in the options string
        for letter in options:
            # append it to the options to pass list
            options_to_pass.append(letter)
        # while i is smallar than the length of options to pass
        while i < len(options_to_pass):
            # create an isolated flag like -u, -k, -r if -ukr is passed
            argTopass = '-' + options_to_pass[i]
            # increment i
            i+= 1
            # calls the selector that mathes the current option in the loop
            # this gets the functionality and option tuple
            func = selector.get(argTopass)
            # append that tuple to the list to pass down to connect()
            list_to_pass.append(func)
        # after the loop is done return the list to connect
        return list_to_pass # then it will call the args_separator() function that
                            # is at the end of this file, that internaly sorts them out
    else:    
        func = selector.get(arg, lambda: "this is an invalid argument")
        return func()


def long_checker(arg):
    selector = {
        '--help': help(),
        '--add-host': add(),
        '--debug-short': debug_short(),
        '--debug-long': debug_long(), # possible issue with multi option commands
        '--default-user': default_user(),
        '--default-key': default_key(),
        '--default-range': default_range(),
        '--no-key': no_key(),
        '--port': port(),
        '--copy-key': copy_key(),
        '--install': install(),    # still needs to be fixed    
    }
    func = selector.get(arg, lambda: "this should also pop the help menu")
    return func()

# this is what handles multiple options being passed,
# by doing this I'm able to loop trough multiple arguments
def args_separator(args):
    if args[0] == '-u':
        return default_user()
    if args[0] == '-k':
        return default_key()
    if args[0] == '-r':
        return default_range()
    if args[0] == '-h':
        return help()
    if args[0] == '-a':
        return add()
    if args[0] == '-v':
        return debug_short()
    if args[0] == '-vvv':
        return debug_long()
    if args[0] == '-n':
        return no_key()
    if args[0] == '-p':
        return port()
    if args[0] == '-c':
        return copy_key()
    return 'False', 'false'