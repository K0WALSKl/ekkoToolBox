from Color import *
from Globals import short_flags_list, flags_list, required_argument_numbers_list


# Parse et contient les arguments donnés
class Parameters:
    def __init__(self, parameters):
        self.parameters = parameters
        self.command = self.get_command_from_parameters()
        self.environment = self.get_environment_from_parameters()
        self.arguments = self.get_arguments_from_parameters()
        self.number = self.get_number_form_parameters()

    # Récupère la commande (new-ad ou new-user etc)
    def get_command_from_parameters(self) -> str:
        for parameter in self.parameters:
            for flag in flags_list:
                if parameter == flag:
                    return parameter
            for flag in short_flags_list:
                if parameter == flag:
                    return parameter
        return ""

    # Récupère les arguments de la commande (username, mail etc)
    def get_arguments_from_parameters(self):
        args = []

        for i, parameter in enumerate(self.parameters):
            if i > 0 and parameter != self.command and parameter != "-n" and not parameter.isnumeric() and parameter != "prod" and parameter != "preprod":
                args.append(parameter)
        return args

    # Récupère le nombre d'occurence (ex: new-ad x 5)
    def get_number_form_parameters(self):
        for i, parameter in enumerate(self.parameters):
            if parameter == "-n" and (self.parameters[i + 1]).isnumeric():
                return int(self.parameters[i + 1])
        return 1

    # Récupère l'index utilisé par le tableau de fonctions
    def get_function_index(self) -> int:
        global flags_list, short_flags_list

        for i, flag in enumerate(flags_list):
            if self.command == flag:
                return i
        for i, flag in enumerate(short_flags_list):
            if self.command == flag:
                return i
        return -1

    # Récupère l'environnement sur lequel on souhaite agir (prod ou preprod)
    def get_environment_from_parameters(self):
        if self.command == "--get-ip" or self.command == "-gi":
            return "NOT_NECESSARY"
        for parameter in self.parameters:
            if parameter == "prod" or parameter == "preprod":
                return parameter
        return "prod"

    # Print l'instance de la classe Parameters
    def print_parameters(self):
        print(Color.PURPLE + "Given : " + str(self.parameters))
        print(Color.PURPLE + "\tCommand :\t" + self.command)
        print(Color.PURPLE + "\tEnvironment :\t" + self.environment)
        print(Color.PURPLE + "\tArguments :\t" + str(self.arguments))
        print(Color.PURPLE + "\tOccurences :\t" + str(self.number) + Color.END)

    # Check si les paramètres données sont OK
    def has_valid_parameters(self):
        if self.command == "":
            print_error("Pas de commande valide (--new-user etc)")
            return False

        if len(self.parameters) < required_argument_numbers_list[self.get_function_index()]:
            print_error("Il manque un paramètre apparemment")
            return False
        return True

    def get_container_name_from_argument(self):
        for arg in self.arguments:
            if arg == "api" or arg == "db" or arg == "client_web":
                return arg
