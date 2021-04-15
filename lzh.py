#!/usr/bin/env python3

# IF YOU ARE HAVING ISSUES RUNNING THIS, READ THE DEPEDENCIES AT THE END OF THIS FILE
# You might need to install these by yourself, in my case they were present in my machine
# when first developing this program, so I can't provide instructions on how to install them,
# but google is every computer nerd best friend.
# eventually this file will have a couple statements that check for depedencies before running
# the script, but until then, it will be more comments than code.

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
from src.args import option_checker
# sends the arguments into the option checker
args = sys.argv
option_checker(args)
# THINGS STILL TO DO:
# - add an install functionality/install script
# - add a way to store a different port inside a host, for situations like port-forwarded servers
# WARNING!!!!!
# This cli utility was built to simplify connections with ssh key protected servers
# while it may be able to connect and not use ssh keys it will always use your default
# key and user to connect to an other machine.
# Even if your computer is able to resolve thet hostname you provide, lzh does not care
# about that, you need to provide a stored hostname, if you lzh does not find that
# hostname in the hosts file it will prompt you to add it you can optionaly add them
# manually by editing the hosts.yml.

########################
###Python Depedencies###
# subprocess, should always come with python, I think
# os,  should always come with python, I think
# pyyaml, might need to be installed for the program to run
##### OS Depedencies####
# OpenSSH, available in most OS I think.
# ssh-copy-id, Linux only program, you can't run the '-c' option outside of linux
########################