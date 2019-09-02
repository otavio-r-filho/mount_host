import os
import argparse
import json
import sys

def read_hosts():
    '''
    '''
    if not os.path.isfile(".sshHosts.json"):
        fhosts = open(".sshHosts.json", mode="a+")
        hosts_data = dict()
        json.dump(hosts_data, fhosts)
        fhosts.close()
    else:
        fhosts = open(".sshHosts.json", "r")
        hosts_data = json.load(fhosts)
        fhosts.close()
    return hosts_data

def save_hosts(hosts_data):
    '''
    '''
    fhosts = open(".sshHosts.json", mode="w")
    json.dump(hosts_data, fhosts)
    fhosts.close()

def list_hosts(indent=2):
    '''
    '''
    hosts_data = read_hosts()    
    indentation = "".join([" "] * indent)
    BOLD  = "\033[;1m"
    RED   = "\033[1;31m"
    BLUE = "\033[1;34m"
    RESET = "\033[0;0m"
    
    if not bool(hosts_data):
        print("There are no hosts!")
    else:
        hosts_names = list(hosts_data.keys())
        for host_name in hosts_names:
            print("{0}{1}{2}{3}".format(BOLD,RED,host_name,RESET))
            print("{0}Address: {1}".format(indentation,hosts_data[host_name]["HostAddress"]))
            print("{0}User: {1}".format(indentation,hosts_data[host_name]["User"]))
            print("{0}Remote dir: {1}".format(indentation,hosts_data[host_name]["RemotePath"]))
            print("{0}Mount point: {1}".format(indentation,hosts_data[host_name]["MountPoint"]))
            print()
        
def mount_point_conflict(mount_point, hosts_data):
    '''
    '''
    for host_name, host_data in hosts_data.items():
        if mount_point == host_data["MountPoint"]: return True
    return False

def add_host():
    '''
    '''
    hosts_data = read_hosts()
    
    print("Host name: ", end="")
    host_name = input()
     # Checking for conflicts
    if host_name in hosts_data:
        print("Host already in the database! Nothing added!")
        return
    print("Host address: ", end="")
    host_address = input()
    print("User: ", end="")
    user = input()
    print("Password: ", end="")
    password = input()
    print("Remote path: ", end="")
    remote_path = input()
    print("Mount point: ", end="")
    mount_point = input()
#    if mount_point_conflict(mount_point, hosts_data):
#        print("Mount point conflict! Nothing added!")
#        return
    print(password)
    hosts_data[host_name] = {
        "HostAddress": host_address,
        "User": user,
        "RemotePath": remote_path,
        "MountPoint": mount_point
    }
    if password:
        hosts_data[host_name]["Password"] = password
    save_hosts(hosts_data)
    
    print("Host successfully added!")
    list_hosts()
    
def remove_host(host_name = None):
    '''
    '''
    hosts_data = read_hosts()
    
    if host_name is None:
        print("Host name: ", end="")
        host_name = input()
    if host_name not in hosts_data:
        print("Host not present! Nothing removed!")
        return
    
    del hosts_data[host_name]
    save_hosts(hosts_data)
    list_hosts()
    
def edit_host(host_name = None):
    '''
    '''
    hosts_data = read_hosts()
    if host_name is None:
        print("Host name: ", end="")
        host_name = input()
    if host_name not in hosts_data:
        print("Host not present!")
        return
    
    print("Address: {0}. Leave blank to not alter: ".format(hosts_data[host_name]["HostAddress"]), end="")
    new_address = input()
    if new_address:
        hosts_data[host_name]["HostAddress"] = new_address
        
    print("User: {0}. Leave blank to not alter: ".format(hosts_data[host_name]["User"]), end="")
    new_user = input()
    if new_user:
        hosts_data[host_name]["User"] = new_user
        
    print("Password: ****. Leave blank to not alter: ", end="")
    new_password = input()
    if new_password:
        hosts_data[host_name]["User"] = new_password
        
    print("Remote path: {0}. Leave blank to not alter: ".format(hosts_data[host_name]["RemotePath"]), end="")
    new_remote_path = input()
    if new_remote_path:
        hosts_data[host_name]["RemotePath"] = new_remote_path
        
    print("Mount point: {0}. Leave blank to not alter: ".format(hosts_data[host_name]["MountPoint"]), end="")
    new_mount_point = input()
    if new_mount_point:
        hosts_data[host_name]["MountPoint"] = new_mount_point

    save_hosts(hosts_data)
    list_hosts()
    
def mount_host(host_name = None):
    '''
    '''
    hosts_data = read_hosts()
    if not hosts_data:
        print("There are no hosts!")
        return
    if host_name is None:
        print("Host name:", end="")
        host_name = input()
    if host_name not in hosts_data:
        print("Host not found!")
        return
    
    cmmd = "mkdir -p " + hosts_data[host_name]["MountPoint"]
    os.system(cmmd)
    cmmd = "sshfs -o ssh_command='ssh -o ServerAliveInterval=40' {0}@{1}:{2} {3}".format(
            hosts_data[host_name]["User"],
            hosts_data[host_name]["HostAddress"],
            hosts_data[host_name]["RemotePath"],
            hosts_data[host_name]["MountPoint"])    
    
def umount_host(host_name = None):
    '''
    '''
    hosts_data = read_hosts()
    if not hosts_data:
        print("There are no hosts!")
        return
    if host_name is None:
        print("Host name:", end="")
        host_name = input()
    if host_name not in hosts_data:
        print("Host not found!")
        return
    
    cmmd = "fusermount -u " + hosts_data[host_name]["MountPoint"]
    if not bool(os.system(cmmd)):
        cmmd = "rm -rf " + hosts_data[host_name]["MountPoint"]
        os.system(cmmd)
    
if __name__ == "__main__":
    actions = {
        "list_hosts": list_hosts,
        "add_host": add_host,
        "remove_host": remove_host,
        "edit_host": edit_host,
        "mount": mount_host,
        "umount": umount_host
    }
    
    action_names = {
        "-l": "list_hosts",
        "--list-hosts": "list_hosts",
        "--add-host": "add_host",
        "-a": "add_host",
        "--remove-host": "remove_host",
        "-r": "remove_host",
        "--edit-host": "edit_host",
        "-e": "edit_host",
        "--mount": "mount",
        "-m": "mount",
        "--umount": "umount",
        "-u": "umount"
    }

    parser = argparse.ArgumentParser(description="Mount hosts via sshfs and fuse as remote file systems")
    mutex_grp1 = parser.add_mutually_exclusive_group(required = True)

    mutex_grp1.add_argument("--list-hosts", "-l",
                            action = "store_const",
                            const="list",
                            help="List all available hosts")
    mutex_grp1.add_argument("--add-host", "-a",
                            metavar="host name",
                            nargs="?",
                            default="None",
                            type=str,
                            help="Adds a host to the database")
    mutex_grp1.add_argument("--remove-host", "-r",
                            metavar="host name",
                            nargs="?",
                            default="None",
                            type=str,
                            help="Removes a host from the database")
    mutex_grp1.add_argument("--edit-host", "-e",
                            metavar="host name",
                            nargs="?",
                            default="None",
                            type=str,
                            help="Removes a host from the database")    
    mutex_grp1.add_argument("--mount", "-m", 
                            metavar="host name",
                            nargs="?",
                            default="None",
                            type=str,
                            help="Mounts the host as remote file system")
    mutex_grp1.add_argument("--umount", "-u", 
                            metavar="host name", 
                            nargs="?",
                            default="None",
                            type=str, 
                            help="Unmount the selected host")
    args = vars(parser.parse_args())
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg is not None:
        action_name = action_names[arg]
        action_val = args[action_name]
        
    if action_name == "list_hosts" or action_name == "add_host":
        actions[action_name]()
    else:
        actions[action_name](action_val)