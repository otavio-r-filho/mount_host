import os
import argparse
import json

def read_hosts():
    '''
    '''
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
    
    print("Host name:", end="")
    host_name = input()
     # Checking for conflicts
    if host_name in hosts_data:
        print("Host already in the database! Nothing added!")
        return
    print("Host address:", end="")
    host_address = input()
    print("User:", end="")
    user = input()
    print("Remote path:", end="")
    remote_path = input()
    print("Mount point:", end="")
    mount_point = input()
    if mount_point_conflict(mount_point, hosts_data):
        print("Mount point conflict! Nothing added!")
        return
    
    hosts_data[host_name] = {
        "HostAddress": host_address,
        "User": user,
        "RemotePath": remote_path,
        "MountPoint": mount_point
    }
    save_hosts(hosts_data)
    
    print("Host successfully added!")
    list_hosts()
    
def remove_host():
    '''
    '''
    hosts_data = read_hosts()
    
    print("Host name:", end="")
    host_name = input()
    if host_name not in hosts_data:
        print("Host not present! Nothing removed!")
        return
    
    del hosts_data[host_name]
    save_hosts(hosts_data)
    list_hosts()
    
def edit_host():
    '''
    '''
    hosts_data = read_hosts()
    
    print("Host name:", end="")
    host_name = input()
    if host_name not in hosts_data:
        print("Host not present!")
        return
    
    print("Address: {0}. Leave blank to not alter:".format(hosts_data[host_name]["HostAddress"]), end="")
    new_address = input()
    if new_address:
        hosts_data[host_name]["HostAddress"] = new_address
        
    print("User: {0}. Leave blank to not alter:".format(hosts_data[host_name]["User"]), end="")
    new_user = input()
    if new_user:
        hosts_data[host_name]["User"] = new_user
        
    print("Remote path: {0}. Leave blank to not alter:".format(hosts_data[host_name]["RemotePath"]), end="")
    new_remote_path = input()
    if new_remote_path:
        hosts_data[host_name]["RemotePath"] = new_remote_path
        
    print("Mount point: {0}. Leave blank to not alter:".format(hosts_data[host_name]["MountPoint"]), end="")
    new_mount_point = input()
    if new_mount_point:
        hosts_data[host_name]["MountPoint"] = new_mount_point

    save_hosts(hosts_data)
    list_hosts()
    
    
    
    
if __name__ == "__main__":
    # Create the server file if does not exist
    if not os.path.isfile(".sshHosts.json"):
        fhosts = open(".sshHosts.json", mode="a+")
        hosts_data = dict()
        json.dump(hosts_data, fhosts)
        fhosts.close()

    mount_points = {
        "ogun": {
            "server": "ogun:/home/otavio",
            "path": "~/Ogun/"
        },
        "ogun_scratch": {
            "server": "ogun:/scratch/otavio",
            "path": "~/Ogun\ scratch/"
        },
        "remtitan": {
            "server": "remtitan:/home/otavio",
            "path": "~/Titan/"
        },
        "titan": {
            "server": "titan:/scratch/otavio",
            "path": "~/Titan/"
        },
        "remogun": {
            "server": "remogun:/home/otavio",
            "path": "~/Ogun/"
        },
        "remogun_scratch": {
            "server": "remogun:/scratch/otavio",
            "path": "~/Ogun\ scratch/"
        },
        "repsol":{
            "server": "repsol1:/home/otavio",
            "path": "~/Repsol"
        },
        "repsol_scratch":{
            "server": "repsol1:/scratch/otavio",
            "path": "~/Repsol\ scratch"
        },
        "repsol_local":{
            "server": "repsollocal:/home/otavio",
            "path": "~/Repsol"
        }
    }

    parser = argparse.ArgumentParser(description="Monta os clusters em pastas remotas")

    parser.add_argument("acao", metavar="montar/desmontar", type=str,
        help="Ação a ser executada. Possíveis valores são: [montar, desmontar]")

    parser.add_argument("cluster", metavar="nome cluster" ,type=str, default="ogun",
        help="Nome do servidor que devera ser montado. Possiveis valores são: [ogun, ogun_scratch, yemoja, yemoja_scratch].Default: ogun")
    
    args = parser.parse_args()

    action = args.acao
    clster = args.cluster

    if action == "montar":
        cmmd = "mkdir -p " + mount_points[clster]["path"]
        os.system(cmmd)
        cmmd = "sshfs -o reconnect {0} {1}".format(mount_points[clster]["server"], mount_points[clster]["path"])
        os.system(cmmd)
    elif action == "desmontar":
        cmmd = "fusermount -u " + mount_points[clster]["path"]
        if not bool(os.system(cmmd)):
            cmmd = "rm -rf " + mount_points[clster]["path"]
            os.system(cmmd)
    else:
        raise ValueError("Acao desconhecida. Possiveis ações são: [montar/demontar]")
