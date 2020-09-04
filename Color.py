# Liste des couleurs pour changer le style d'un print
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# En dessous, que des fonctions permettant un print rapide dans le style que l'on souhaite
def print_api(to_print: str):
    print(Color.CYAN + to_print + Color.END)


def print_error(to_print: str):
    print(Color.RED + to_print + Color.END)


def print_bold_error(to_print: str):
    print(Color.BOLD + Color.RED + to_print + Color.END)


def print_warning(to_print: str):
    print(Color.YELLOW + to_print + Color.END)


def print_bold_warning(to_print: str):
    print(Color.BOLD + Color.YELLOW + to_print + Color.END)


def print_success(to_print: str):
    print(Color.GREEN + to_print + Color.END)


def print_bold_success(to_print: str):
    print(Color.BOLD + Color.GREEN + to_print + Color.END)


def print_underline(to_print: str):
    print(Color.UNDERLINE + to_print + Color.END)


def print_bold(to_print: str):
    print(Color.BOLD + to_print + Color.END)


def print_bold_underline(to_print: str):
    print(Color.BOLD + Color.UNDERLINE + to_print + Color.END)