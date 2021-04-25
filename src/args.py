from src.lib.options_handler import short_checker
from src.lib.connections import connect, connect_port
from src.lib.actions.options_constructors import help_menu
from src.lib.actions.key_handlers import key_copy
from src.lib.actions.init_handler import init_handler

# this file will always be 'massive' and not modular, because it handles how arguments are
# passed to lzh. I think I fixed most of the unpredictable results with the command object
# I am aware that I use a LOT of if statements in here, but saddly as of right now, I don't know
# an other way to handle arguments, because that basically means that, when ever I add features to
# this file that don't connect to a ssh session, I need to add an exception in the if statements to handle
# that feature, however, if you read the short_checker function, you will realize that it just looks for the
# options that option_checker finds inside the selector object, that object stores the raw functions that feed
# options to lzh then the option_checker function calls those functions and grabs the flags to be passed to
# the connect functions, a rather complex way of implementing this, in my opinion, but at least this implementation
# makes sure that if you pass an unknown option to lzh the program will just break and return the help menu
# which is what most cli utilities do.

def option_checker(args):
    arguments = args[1:]
    i = 0
    command = {'options': list(), 'targets': list()}
    internal_opts = list()
    external_opts = list()
    if len(arguments) > 1:

        while i < len(arguments):
            if arguments[i].startswith('-'):
                opt = arguments[i]
                command['options'].append(opt)
                try:
                    targ = arguments[i + 1]
                    command['targets'].append(targ)
                # breaks the loop if there's an indexError, if no targets were found until then
                # the program will break before doing anything, this prevents incorrect arguments
                # being passed to the connect functions that are the returns of this function
                except IndexError:
                    break
            i += 1
        # this checks if the user passed options before arguments, as this is needed for this to work
        if len(command['targets']) == 0:
            print(
                'You need to provide the options before the targets, please check the help menu!'
            )
            return exit()

        opts = short_checker(command['options'])
        if len(opts) <= 1:
            if '-h' in opts[0]():
                opt, functionality, text = opts[0]()
                return print(text)
            elif '-p' in opts[0]():
                opt, functionality = opts[0]()
                target = command['targets'][0].split(':')[0]
                port = command['targets'][0].split(':')[1]
                targets = [target, port]
                return connect_port(targets=targets,
                                    external_options=opt,
                                    command=command)
            elif '-c' in opts[0]():
                return key_copy(command)
            else:
                opt, functionality = opts[0]()
                if functionality == 'internal':
                    return connect(targets=command['targets'],
                                   internal_options=opt,
                                   command=command)
                else:
                    return connect(command['targets'],
                                   external_options=opt,
                                   command=command)
        else:
            for funcs in opts:
                (opt, functionality) = funcs()
                if functionality == 'internal':
                    internal_opts.append(opt)
                else:
                    external_opts.append(opt)
        if '-p' in external_opts:
            opt, functionality = opts[0]()
            target = command['targets'][0].split(':')[0]
            port = command['targets'][0].split(':')[1]
            targets = [target, port]
            return connect_port(targets, internal_opts, external_opts, command)
        elif '-c' in external_opts:
                return key_copy(command)
        else:
            return connect(targets=command['targets'],
                           internal_options=internal_opts,
                           external_options=external_opts,
                           command=command)
    else:
        arg = str(arguments)[2:-2]
        if arg == '-h' or arg == '--help' or len(arguments) == 0:
            checker = short_checker(arg)
            (opt, functionality, text) = checker[0]()
            return print(text)
        elif arg == '-init':
            return init_handler(None)
        else:
            return connect(arguments, command=command)