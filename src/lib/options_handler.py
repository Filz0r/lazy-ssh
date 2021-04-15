# yes import everything from the functions file, the selector object
# works like an switch statement, that is then stored in a list and
# passed to the args function
from src.lib.actions.options_constructors import help_menu, default_key, add, debug_long, debug_short, copy_key, default_user, default_range, name, script_init, port


def short_checker(args):
    # these are all the available options the program accepts, its a list of functions
    # similar to a switch statement, the functions just return the flag and the
    # functionality of the option for the most part, more complex options also return
    # extra options, but these options are more specific and most likely don't result in a
    # connection made, so they are easier to track if they create any issue.
    selector = {
        # help menu
        '-h': help_menu,
        # adds a new host to the hosts file
        '-a': add,
        # debugs the ssh connection passing the -v flag to ssh
        '-d': debug_short,
        # long debug to for ssh connections passing the -vvv flag
        '-ddd': debug_long,
        # handles the user part of lzh, the caller function could
        # have a better name but for now they will stay like this
        '-u': default_user,
        # like the -u flag the -k handles the key aspects of the arguments passed
        '-k': default_key,
        # this will actually set the default range for lzh to work, for example
        # the command "lzh 12" will connect to IP 192.168.0.12 if
        # the default range is 192.168.0. usage is "lzh -r 192.168.0." notice the
        # dot at the end of the argument this is required for it to work.
        '-r': default_range,
        # sets the name of the host to be used
        '-n': name,
        # usage is "lzh -p localdomain:2222 -u admin -k /path/to/key" to connect to
        # port 2222 on the stored localdomain IP adress neat for servers that only
        # have ssh enabled with port forwarding trough an other host, or even if the ssh
        # server just listens on an diferent port. I might add a away to store this in the
        # future but for now you still need to provide the user and key you use when port
        # forwarding if it's not the same as the default key, storing this would make it
        # possible to ssh into production servers that are more protected, but again
        # this is beyond the scope if the early stage of the project.
        '-p': port,
        # copy the default key to the IP termination/hostname you provide with the default user
        # you cannot pass aditional flags to this command right now, I might work on that.
        '-c': copy_key,
        # change the default values of the config file, these can also be manualy edited in the config.yml file
        '-init': script_init
    }
    # create a list to store all the actual functions that are stored inside
    funcs = list()
    # loops trough the arguments
    for arg in args:
        # if the arg exists inside the selector object
        if arg in selector:
            # append that to funcs
            funcs.append(selector[arg])
        else:
            # if not call the send the help menu to the user warning him that
            # the flag he passed was invalid this might be helpfull if anyone
            # wants to use this wacky thing, I mean at least they get an help menu
            err_funcs = list()
            err_funcs.append(help_menu)
            return err_funcs
    return funcs
