#!/usr/bin/env python3
# This script/program was built to simplify ssh connections inside an
# homelab enviroment where hosts are constantly going up and down
# because of this copying the ssh keys onto those hosts or typing 
# a password to ssh onto those boxes sometimes requires me to write rather 
# long commands, and because this script is called 'lazy-ssh', meaning I'm
# lazy when I have to type long commands, I decided to build this, not only
# to improve my efficiency in my homelab, but also to practice and learn a little
# more about Python
import sys
#loads the default configurations into the script
import src.config
# checks if the provided arguments are valid
from src.option_checker import option_checker
# import the connection function that is responsible for connecting to the servers
import src.connections
# sends the arguments into the option checker
args = sys.argv
option_checker(args)

