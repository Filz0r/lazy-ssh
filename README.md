# Lazy-ssh
 Ever got tired of having to edit your hosts file and your bash aliases whenever you do changes in your homelab setup?

 Well, I have and because I've had enough of editing my .bashrc file every time I added or removed an host from my homelab, I decided to build a Python CLI utility that made that irrelevant!

And the best part is for the most part it *probably* works on most operating systems that run Python.

*(I will write a list of them at the end of this file, because you do need to install them yourself, because this program is still in early development stages, I haven't implemented a way for lzh to to check for them when its first ran, mostly because I already had all the dependencies needed in my computer when developing, again check the end of the readme for more info on that, ando on how to install and run lzh)* 

**DISCLAIMER:** *This readme, goes to the extent of telling you what errors, might happen when using lzh, if you have any issues with lzh that are explained in this file, I will most likely tell you to read this file, mostly because I took the time to debug and understand why they happen, and created ways for the program to warn you when it thinks you've done anything wrong, as long as you follow the "rules" mentioned throughout this file, there program will most likely work as expected, but your mileage may vary.*
 
## What does that mean?

 Well honestly I run an homelab with a couple of old laptops, while I use Pihole in my homelab, for DNS resolving my internal services and so on, I proxy all those services with NGINX in a separate server, this might not be the best implementation, whoever it allowed me to build a central spot that is responsible for redirecting all services to there, and then serve them with my own self-signed certificate, to ensure HTTPS, whether the server lives inside my LAN or not, as long as that server can resolve the IP address I put in my NGINX configs the website will be accessible as long as you are using my pihole instance as a DNS server. 
 Yeah that's cool but normally people write their hosts inside their computers hosts file for easier access to those machines, however doing this with the FQDN of my LAN servers, my computer will only resolve the IP adress I have stored inside the hosts file, making my localdomain reverse proxy pretty much useless, so I started to save the FQDN on pihole and my localdomain reverse proxy, and inside my hosts file I would store an 'pretty' hostname in my hosts file and alias that pretty hostname to my bashrc...

 I think you should know what I mean by now, everytime an IP changes I need to do changes to my .bashrc and hosts files, making me spend more time configuring my own machine everytime I change/add something to my homelab than actually making changes on those machines. This introduced a lot of redundancy in my workflow, and I don't like that, so I started to think of a way to simplify my implementation, and from there lzh happened, the main goal of this utility is for me to be able to ssh into boxes while typing the least amount of things possible, and at the same time remove the need for me to have to constantly manually edit files on my pc in order to have easy ssh access to those boxes.

## Who is lzh for?

- Lazy-ssh, or lzh for short, is for individuals like myself that have a couple of bare-metal machines in their LAN hosting virtual machines, and want to be able to access those hosts and all of those guests without having to implement a way to access those machines with hostnames, whether it be a Fully Qualified Domain Names or a short hostname.
- Lzh is also for people that have DNS resolving in their LAN, but are just tired of having to create aliases on their workstation bashrc every time they add a new server to their homelab. Lets say you want to add a new host to your bag of servers, you have 2 ways of doing that, the first is the normal way, you go to the hosts.yml that lzh creates in the root of the directory where lzh is stored, and manually write that host into there. The second and better way is to just use lzh. I programmed 2 ways of adding hosts to lzh, one that uses the default settings stored in the config.yml file that is created, that just requires you to type 2 words, lzh and either the pretty hostname you are going to use for that host or the IP address of that host, or even better just the final block of digits of the IP address, if it's inside your LAN, more on that later.
- You might have noticed that lzh uses YAML files for the config and the hosts file, because YAML, so if you like YAML, lzh uses it.

## How to use it?

For the purposes of explaining how lzh assume the values in bold as what I'm storing in my config.yml file, I'll use those to explain most of the functionalities lzh has.

When you first run lzh, you will be asked four things:

#### 1) What is your default user?
This means what's the administrator username you use the most in your environment.

Example: 

> What is your default user? **admin**

#### 2) What's the default IP range?
This means that you need to provide your sub net, but not in an traditional way, to simplify my logic a bit you don't provide the traditional `192.168.1.0/24`, what lzh expects you to input is actually something like `192.168.1.`, notice the dot at the end,
I have a good reason for this, if it ends with a dot, it was easier to test my concept like that.

Example:

>What is the default IP range for your LAN? **192.168.1.**

#### 3) What is the default ssh private key?
Yes, lzh stores the paths to your private and public keys, however, your user still needs to have the right permissions set for this file, or OpenSSH won't allow you to connect.
**You need to provide an absolute path for this**

Lzh does not create keys, there's a bunch of tutorials online on how to set that up.

Example:

>What's the default ssh private key? **~/.ssh/key**

#### 4) What is the default ssh public key?
Again this path is stored in your config, so be sure to not use keys that you use in production environments as defaults.

Example:

>What's the default ssh public key? **~/.ssh/key.pub**


Now that all the defaults are stored, you will never see that message again, unless you run `lzh -init` an option that as the ability to get you back to your starting position, so be careful using that option.

## Adding Hosts

Now we can get to the part of adding hosts to lzh, like said before, you can add hosts in multiple ways, either by writing them to your hosts file manually or by using lzh. I'm just going to focus on the lzh part in here.

Okay, so far we have set the following:

- The default user is *admin* 
- The default IP range is *192.168.1.*
- The default private key is *~/.ssh/key*
- The default public key is *~/.ssh/key.pub*

So let's say you have an host called `pihole.localdomain` with the IP of `192.168.1.100`, and it is using the default user and the default ssh key, you can add it to lzh in 3 different ways, you will almost always be asked the same questions in each of these 3 ways, each of them will ask you almost always the same thing, it really depends on how you try to add a new machine:

1) First and the longer way is `$ lzh 192.168.1.100`, we specify the full IP address and lzh will recognise that and prompt you in one way.

2) Then we have the *cool* way of doing it `$ lzh 100`. This means that lzh will know that your connection is inside the *default range*, if I'm not mistaken the questions will be almost the same as the first example.

3) Finally, we have the longer way of the 3, you provide before hand the pretty hostname, `$ lzh pihole`. The only reason this is longer is because lzh asks a couple more questions like the IP address or termination.

***However* you need to keep this in mind when storing hosts this way. If you want to use a ssh key that is different than the default one, this is not the way of doing this.**

**The pretty hostname is used to connect, if lzh says he can't find that host is because there's something wrong with your command, trust me, it took me a while to understand that. Basically lzh uses the pretty hostname as a way to connect to the box, if you provide an IP termination, lzh will try to see that IP termination and will look for it in the known_info section of the hosts file, and it won't find it, because that section only stores pretty hostnames. I tried to implement a way to store more than the pretty hostname, but I couldn't because each object stored inside the added_hosts block inside the hosts file is actually stored, and accessed, with the pretty hostname, and not the IP! Implementing that would actually over complicate this, so I ditched that option.**

Okay we now know how to add a host, the lazy but slower way, and we know what complications might rise from that. But every CLI needs options right? You're absolutely correct, I talked about the `-init` option before, but that's just one of many you can use. Obviously if there's a slow way there must also be fast way, right?

Yep, there is, but before that I need to make one thing clear, **when using options with lzh you need to pass the option before the argument, or you will get either one of 2 error messages, or you will get the help menu**, and I know we all love typing a command just to get an help menu back, so pleasing...

Okay I just talked about one of 2 error messages, but what triggers it? Lzh has options that can be used to overwrite the defaults, because again, lzh tries to use those whenever possible.

So one would think that by running `$ lzh pihole -k ~/.ssh/key -u admin` right? **Wrong!**

You were almost right, but like I said before you need to pass options before arguments, the option that adds that host, is `-a`. `-k and -u` are used to overwrite the default key, but lets forget about these for a bit.
First, if thing you need to know about the *-a* option is that, it loads the defaults into that host, while being modular as heck at the same time.

Using the previous example, lets try to add `pihole.localdomain` to lzh using default values, but without having to reply to a bunch of inputs. The correct input is,

 `$ lzh -a pihole.localdomain`

we can pass the FQDN, the pretty hostname, or the IP or IP termination to -a, the fastest way, is by sending the FQDN, you will be asked if that's what you provided, if yes, the pretty hostname you need to login will be `pihole` and you just need to give the IP to lzh and you're done. You can optionally pass the `-u and -k` option to lzh if you want to use an other username or private key to connect to that host. 

**This option is meant for hosts that use key based authentication only!**

## Connecting with non default values

Let's say your regular admin user account on a production server was hacked, but you have either an other user hidden using an different key or just have an different key for the root account, and you need to login as root, even if you shouldn't. Well there's also an way of doing that, with the `-n` option, this option basically tells lzh that you are trying to connect to an added host with settings different from the defaults.For example,

 `$ lzh -n pihole -u root -k ~/.ssh/root_key` 

will connect to the pihole server was mentioned before, but instead of trying to connect to the admin user, we are trying to connect to the root user with an other key, `~/.ssh/root_key`. These values will not overwrite the saved ones but still allow you to connect to an saved server using lzh.

If for example you do not pass the `-n` flag to that command, there are 2 possible outcomes, lzh tells you that annoying warning message I talked about before where lzh tells you it can't find the host and tries to manually add it, even though the host was already added, same goes for the `-n` flag, but this outcome is the more common one, when trying to pass multiple options to an already added host. However when trying to just pass one option to lzh like for example an different user, lzh would act up when inside the loop that sorts the arguments and options, so I implemented a way to break that loop, if any errors happen, **lzh will remind you to input options before arguments and tell you to look at the help menu if this happens, because you most likely forgot to pass the `-n` flag before your hostname**

## Using non standard ssh ports

One of the most recommended change to the security of an ssh connection to a server, besides implementing key based authentication, is changing the port where the ssh service listens, I will admit, that I the only reason why I don't implement that in my external servers, is because first, I usually lock my ssh sessions with firewall rules, by only allowing it from one IP address and second an most importantly, because that would make the ssh command even longer, I really dislike typing long commands, specially when I misspell something.

To prevent this, lzh also has the ability to specify a different listening port, other than port 22, that is. For example,
 
`$ lzh -p pihole:2222`

This will connect to the same pihole server we've been talking about but instead of using the default port 22 it will use port 2222 when trying to connect to that pihole server, you just need to specify the flag `-p` before the pretty hostname and follow that by `:$PORT`. However, right not lzh does not have a way to store the port variable, I do want to implement that, however I need to make sure lzh works on Windows, with and without WSL first. I actually need this feature for my current stack, as I do change the default listening port on some of my cloud instances, since people really do like to knock on that door in the cloud.

## Promoting key based authentication

Lzh also promotes key based authentication rather than password based authentication and also provides you the tools to enforce that on yourself, by setting an default public key in the config lzh can make use of an rather nice command, *ssh-copy-id* this Linux only command, allows you to copy an public key to an server, however by default it tries to copy the id_rsa file from your machine to that server and requires flags to copy any key that is not that default key, by now we all should know how much I hate when commands get long because of flags. So obviously lzh can also run this command for you. For example,

`$ lzh -c pihole`

Lets say we actually forgot to set the ssh key on our trusty pihole server, those 3 words above, do that for us, this will copy the default public key we set at the start to the user admin in that pihole instance, now lets say we really want to be able to login as root on that pihole server, again you should never do that obviously, and we even set it's own unique key pair just for the root account, we can pass the options `-u and -k` in here as well and add an public key pair different than the default one by passing down those flags.

## Debuging for the rescue

You know that feeling when you know that everything you are typing in an command is correct but the ssh command is just not working? Well OpenSSH has flags to debug that, so obviously lzh also has a way of passing down those flags to the ssh command for you to debug that connection, just rerun the lzh command with the flag `-d` at the end this will give you an readable output, it's the same as passing the `-v` option to OpenSSH, you can also pass the `-ddd` option to lzh to have a more verbose debug option, this passes the `-vvv` to OpenSSH.

# All jokes aside

Well just like the title mentions, all jokes aside, ssh can be a way for your server to be hacked, this is why password authentication and other changes are recommended to be applied on an Internet facing server, that anyone can talk to.

**Lzh is not an replacement to these recommendations**, and it will ever be, lzh was built as a way to simplify ssh connections, do not look at lzh as a replacement of ssh, look at it for what it actually is, an string generator that creates an valid ssh command, that uses IP addresses, and avoids spelling mistakes, and having to constantly change your aliases and hosts files.

I really took the time to think about how I could implement a way to also connect to protected servers, mostly because while I am a rather lazy person I do take the security of my Internet facing servers seriously, as should everyone, this is why lzh has the ability of using default key pairs, this way you can create your unique key pair for testing and for your LAN servers, and if you need to add an server with more security whether it be a different, stronger key or changing listening ports you can also do that, while also being able to easily set up key based authentication on ssh, all with one tool, that allows you to save those settings in one central place, your lzh hosts file.

Right now this program is still in its early stages and because of that you only get to know how to run it at the end of the readme, just to make sure that you are aware that this tool just creates a command for you and because of that stuff might not work as expected right now. And also because I wanted to list all the dependencies lzh needs in order to run in here. Oh and finally the ssh-copy-id is not available on Windows systems, and you need Homebrew to install it in macOS, and I have no idea on how to add a script to your path on Windows systems, so no instructions for that, macOS should be the same as Linux, I think.

#### Depedencies:
- Python: pyyaml, subprocess, os, socket
- Other packages: OpenSSH, ssh-copy-id 

### How to run lzh
1) Clone this repository on your machine

>$ git clone https://github.com/filz0r/lazy-ssh

2) cd into that directory and run pwd

> $ cd lazy-ssh

>$ pwd

3) You should get the path to that folder, copy that path and run

> ln -S /path/to/lzh/lzh.py ~/.local/bin/lzh

And you're done. Yes I know that you should not install programs like this, and I'm going to work on that, after making sure this at least works on Windows, but until then this project will be stale, as it does all of the basic things it needs, and fine tuning and proper installing methods come after taking my neat concept trough it's paces. You can always try to read the maze that is the comments inside the all of the python files, most of them are more comment than actual programming, explaining why things work the way they do.

Thank you for reading this boring text, and I hope you find lzh useful for your workflow!