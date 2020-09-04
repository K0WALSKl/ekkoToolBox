import os
import signal
import sys

from Color import *
from SSHService import SSHService
from Parameters import Parameters


def get_status(parameters: Parameters) -> bool:
    ssh = SSHService(parameters)
    print_warning("Le résultat se trouve dans la colonne 'STATUS'")
    print_bold(ssh.execute_command())
    return True


def get_table(table: str, ssh: SSHService) -> str:
    return ssh.execute_specific_command(
        "docker exec db mongo test --eval 'db." + table + ".find().pretty()' | awk '{if(NR>4)print}'")


def search_table(table: str, ssh: SSHService, query: str) -> str:
    ssh.execute_specific_command(
        "docker exec db mongo test --eval 'db." + table + ".find().pretty()' | awk '{if(NR>4)print}'")


def print_all_tables(ssh: SSHService):
    print_bold_underline("ANNONCES")
    print_api(get_table("announces", ssh))
    print_bold_underline("USERS")
    print_api(get_table("users", ssh))


def print_db(parameters: Parameters) -> bool:
    ssh = SSHService(parameters)
    print("Param : ")
    parameters.print_parameters()
    if len(parameters.arguments) == 0:
        return print_all_tables(ssh)
    if parameters.parameters[0] == "announces" or parameters.parameters[0] == "users":
        return print_api(get_table(parameters.parameters[0]))
    return True


def has_valid_container_name(arguments):
    for arg in arguments:
        if arg == "api" or arg == "db" or arg == "client_web":
            return True
    return False


def print_logs(parameters: Parameters) -> bool:
    ssh = SSHService(parameters)

    if len(parameters.arguments) != 0 and has_valid_container_name(parameters.arguments):
        container_name = parameters.get_container_name_from_argument()
        print("Print des logs du container " + container_name)
        print_bold_warning("Ctrl + C pour arrêter de lire les logs en live")
        # Pour éviter un sale message d'erreur quand on Ctrl + c
        try:
            ssh.execute_specific_command("docker logs " + parameters.arguments[0] + " -f")
        except KeyboardInterrupt:
            sys.exit(0)

    else:
        print("Print des logs de tous les containers")
        print_bold_underline("\nAPI")
        ssh.execute_specific_command("docker logs api")
        print_bold_underline("\nDB")
        ssh.execute_specific_command("docker logs db")
        print_bold_underline("\nCLIENT WEB")
        ssh.execute_specific_command("docker logs client_web")
        res = ssh.execute_command()
    return res != ""


def refresh_documentation(parameters: Parameters) -> bool:
    ssh = SSHService(parameters)

    print("Lancement du refresh des documentations")
    result = ssh.execute_command()
    if result == "":
        return False
    return True


def restart_server(parameters: Parameters) -> bool:
    ssh = SSHService(parameters)
    print(
        "Lancement du redémarrage du serveur de " + (
            "production" if parameters.environment == "prod" else "pré-production"))
    print_warning("Cette commande met du temps.")
    result = ssh.execute_command()
    print_bold(result)
    return not result == ""


def start_server(parameters: Parameters) -> bool:
    ssh = SSHService(parameters)
    print("Lancemeent du démarrage du serveur de " + (
        "production" if parameters.environment == "prod" else "pré-production"))
    print_warning("Cette commande met du temps.")
    result = ssh.execute_command()
    print_bold(result)
    return not result == ""
