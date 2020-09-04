from Color import *
from User import User
from os import path
from Parameters import Parameters


# Récupère les credentials contenu dans le fichier stored_user.txt
# Return un tableau sous la forme [username, email, password] (str[])
def get_stored_user() -> list:
    filepath = "stored_user.txt"
    user_credentials = ["", "", ""]

    if not path.exists(filepath):
        print_warning("Pas de fichier user.")
        return user_credentials
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            user_credentials[cnt - 1] = line.strip()
            line = fp.readline()
            cnt += 1
    return user_credentials


# Check si les paramètres données pour la création de l'user
def has_valid_parameters(parameters):
    if len(parameters.arguments) != 3:
        return True
    if len(parameters.arguments) < 3:
        print(Color.RED + Color.BOLD + "Pas assez de paramètres" + Color.END)
        return False

    if len(parameters.arguments[0]) <= 1:
        print(Color.RED + Color.BOLD + "L'username est trop court" + Color.END)
        return False

    if parameters.arguments[1].find("@") == -1:
        print(Color.RED + Color.BOLD + "Pas de @ dans le mail ?" + Color.END)
        return False

    if len(parameters.arguments[2]) < 8:
        print(Color.RED + Color.BOLD + "Le mdp est trop court (" + str(len(parameters.arguments[2])) + " < 8)" + Color.END)
        return False

    return True


# Point d'entrée fonction création user
def new_user(parameter):
    if not has_valid_parameters(parameter):
        print("Création d'un nouvel user impossible.")
        return False
    if len(parameter.arguments) == 3:
        create_user_and_profile(parameter)
    else:
        create_random_user(parameter)
        # if res is False: TODO Pour un exit sexy
        #     return False
    return True


# Créer un utilisateur et profil aléatoire si la commande --new-user n'a pas d'argument
def create_random_user(parameter):
    print("Création d'un nouvel utilisateur aléatoire")
    user = User(None, None, None, parameter)
    parameter.arguments.append(user.username)
    parameter.arguments.append(user.email)
    parameter.arguments.append(user.password)
    user.api_create_user()
    identity = user.fetch_identity()
    user.api_create_profile([
        user.username
        , get_lastname_from_email(user)
        , identity[2]
        , identity[3]
        , identity[4]])
    parameter.arguments = []
    user.store_user()


# Créer un user avec les paramètres donnés et génère un profil aléatoire (user != profile)
def create_user_and_profile(parameter: Parameters):
    print("Création d'un nouvel utilisateur")
    user = User(parameter.arguments[0], parameter.arguments[1], parameter.arguments[2], parameter)
    user.api_create_user()
    user.api_create_profile()
    user.store_user()


# Utilisé lors de la création de user + profile aléatoire.
# L'email d'un user aléatoire est prenom.nom@gmail.com
# Ici on récupère ce qui se situe entre le premier "." et enlève @gmail
def get_lastname_from_email(new_user):
    return new_user.email.split(".")[1].replace("@gmail", "")



