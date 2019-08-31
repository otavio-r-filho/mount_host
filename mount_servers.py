import os
import argparse

if __name__ == "__main__":
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
