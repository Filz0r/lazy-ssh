def help_text():
    menu = '''HELP AS ARRIVED, I THINK!
Available options:  -h(elp)     -> Provides this menu!
                    -k(ey)      -> Overwrites the saved/default ssh key when connecting
                    -u(ser)     -> Overwrites the saved/default user when connecting
                    -n(ame)     -> Tells lzh that the hostname already exists when providing arguments
                    -a(dd)      -> Adds the provided IP/FQDN with the defaults
                    -p(ort)     -> Connects with a port different from the default ssh listening port
                    -c(opy-key) -> Copies the default public key to the provided host
                    -init       -> Runs the initial configuration of lzh

Usage examples: 
    - lzh -n host1 -u admin -k /path/to/key   <- Connects to host1 with a key and user different than the saved
    - lzh -a host2.domain.tld -k /path/to/key <- Adds host2 with the defaults, but overwrites the default key
    - lzh -p host2:2222 -u root               <- Connects to host2 on port 2222 with the root user
'''
    return menu