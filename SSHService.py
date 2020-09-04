from Parameters import Parameters
import os


class SSHService:
    def __init__(self, parameters: Parameters):
        if parameters.environment == "prod":
            self.address = "x2021ekko1616160161000.northeurope.cloudapp.azure.com"
            self.port = 50061
            self.user = "ekkoeip"
        else:
            self.address = "52.169.120.202"
            self.port = 54100
            self.user = "gwendhal"
        self.command = parameters.command = self.get_command_from_parameter(parameters.command)

    # Génère la commande que l'on effectuera sur le serveur. --get-status ne fais en réalité qu'envoyer la
    # commande "docker ps -a" en SSH
    @staticmethod
    def get_command_from_parameter(command: str) -> str:
        if command == "--get-status" or command == "-gs":
            return "docker ps -a"
        elif command == "--print_db" or command == "-pd":
            return ""
        elif command == "--refresh-doc" or command == "-rd":
            return "cd ekko \
                && git fetch origin \
                && sleep 1 \
                && git checkout server -- www/documentation/ \
                && git checkout client_web -- ekkoWeb/documentation \
                && git checkout client_mobile -- Ekko/doc/api \
                && sudo rm -rf /var/www/html/* \
                && sudo chown -R ekkoeip:ekkoeip /var/www/html/ \
                && mkdir /var/www/html/client_mobile \
                && mkdir /var/www/html/client_web \
                && cd /var/www/html \
                && ln -s ~/ekko/www/documentation/* . \
                && ln -s ~/ekko/ekkoWeb/documentation/* ./client_web/ \
                && ln -s ~/ekko/Ekko/doc/api/* ./client_mobile/"
        elif command == "--restart-server" or command == "-rs":
            return "./restart_server.sh"
        elif command == "--start-server" or command == "-ss":
            return "./start_server.sh"
        elif command == "--print_logs" or command == "-pl":
            return "docker logs api && docker logs db && docker logs client_web"
        return ""

    # Exécute la commande par défaut en fonciton de l'instance de la classe "@Parameters"
    def execute_command(self) -> str:
        if self.command == "":
            return ""
        return os.popen('ssh ' + self.user + '@' + self.address + ' -p ' + str(self.port) + ' "' + self.command + '"').read()

    # Exécute une commande spécifique en cas de paramètre plus complexe
    def execute_specific_command(self, command: str):
        if command == "":
            return ""
        return os.popen("ssh " + self.user + "@" + self.address + " -p " + str(self.port) + " \"" + command + "\"").read()
