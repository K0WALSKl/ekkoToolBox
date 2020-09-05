from library import requests
from Color import *
from Globals import hobbies_list
import random
import json
import time


# Cette classe contient les infos de l'utilisateur ainsi que
# les méthodes en rapport aux utilisateurs
class User:
    # Constructeur. Si des arguments sont donnés, on génère un user à partir des arguments (username, mail, pwd).
    # Si la classe est appelée sans paramètres ( user = User() ), on génère aléatoirement un nouveau user + profil
    def __init__(self, username=None, email=None, password=None, parameter=None):
        if username is not None:
            self.username = username
            self.email = email
            self.password = password
            self.token = ""
        else:
            credentials = self.generate_random_profile()
            self.username = credentials[0]
            self.email = credentials[1]
            self.password = "azeqsdazeqsd"
        if parameter:
            self.base_url = parameter.get_url_from_parameter()

    # Fais une requête HTTP vers l'API pour créer un user
    # Si l'user est OK, les identifiants seront stockés dans
    # un fichier pour pouvoir lancer les autres requêtes (new-ad etc)
    # avec cet user
    def api_create_user(self) -> bool:
        url = self.base_url + "/subscribeUser"
        data = {
            'username': self.username,
            'email': self.email,
            'password': self.password,
        }

        request = requests.post(url=url, data=data)
        res = request.json()

        if request.status_code == 200 and res['authUser']['status'] is True:
            print_bold_success("Nouvel utilisateur créée")
            self.token = res['authUser']['token']
        elif request.status_code == 200 and res['authUser']['status'] is False:
            print_bold_warning("Cet utilisateur existe déjà. User par défaut remplacé")
            self.token = res['authUser']['token']
            self.store_user()
        else:
            print_bold_error("Erreur")
            print_api(str(res))
            return False
        return True

    # Lance une requête POST de connexion à l'API pour récupérer un token
    def api_get_token(self):
        url = self.base_url + "/authUser"
        data = {
            'email': self.email,
            'password': self.password,
        }

        request = requests.post(url=url, data=data)
        res = request.json()

        if request.status_code == 200:
            try:
                self.token = res['authUser']['token']
            except KeyError:
                return False
        else:
            print_bold_error("Erreur :")
            print_api(str(res))
        print_success("Token acquis")

    # Réalise une requête GET pour récupérer un nom et prénom aléatoire
    # Et remplis les champs nécessaires à la création d'un profile
    def fetch_identity(self):
        URL = "https://randomuser.me/api/"

        try:
            request = requests.get(URL)
            res = request.json()
        except json.decoder.JSONDecodeError:
            print_error("Problème de call API génération de profil. Pause de 3 secondes...")
            time.sleep(3)
            request = requests.get(URL)
            res = request.json()

        # Evite les prénoms et noms qui utilise des caractères non ascii
        while len(res["results"][0]["name"]['first'].encode('ascii', 'ignore').decode('utf-8')) == 0 or \
                len(res["results"][0]["name"]['last'].encode('ascii', 'ignore').decode('utf-8')) == 0:
            time.sleep(1)
            request = requests.get(URL)
            res = request.json()

        firstname = res["results"][0]["name"]['first']
        firstname = firstname.encode('ascii', 'ignore').decode('utf-8')
        lastname = res["results"][0]["name"]['last']
        lastname = lastname.encode('ascii', 'ignore').decode('utf-8')
        hobbies = self.choose_hobbies()
        website = "https://www.soundcloud.com/" + firstname + "_" + lastname
        summary = "Bonjour, je m'appelle " + firstname + " " + lastname + ", " + "j'aime tout ce qui est " \
                  + hobbies[0] + " et " + hobbies[1] + "."
        if len(firstname) == 0 or len(lastname) == 0:
            return []
        return [firstname, lastname, hobbies, website, summary]

    # Réalise la requête de création de profile
    def api_create_profile(self, generated_profile=None):
        print("Création du profile...")
        profile = self.fetch_identity() if generated_profile is None else generated_profile
        url = self.base_url + "/profile"
        DATA = {
            'firstName': profile[0],
            'lastName': profile[1],
            'hobbies': [
                profile[2][0],
                profile[2][1]
            ],
            'email': self.email,
            'website': profile[3],
            'summary': profile[4]
        }
        HEADER = {
            'custom_auth': "authorization=Token " + self.token
        }

        request = requests.post(url=url, data=DATA, headers=HEADER)
        res = request.json()
        if request.status_code == 200:
            print_bold_success("Profile créée")
            print(Color.CYAN + json.dumps(DATA, indent=4) + Color.END)
            return True
        else:
            print_bold_error("Impossible de créer le profile")
            print(Color.CYAN + json.dumps(res, indent=4) + Color.END)
            return False

    # Récupère l'ID de l'utilisateur en fonction de son Token
    def api_get_user_id(self):
        url = self.base_url + "/profile"
        HEADER = {
            'custom_auth': "authorization=Token " + self.token
        }
        request = requests.get(url, headers=HEADER)
        return request.json()["user_id"]

    # Print les infos contenus dans la classe de l'user (mémoire vive)
    def print_user_info(self):
        print("\nUsername : " + Color.BOLD + self.username + Color.END)
        print("Email : " + Color.BOLD + self.email + Color.END)
        print("Password : " + Color.BOLD + self.password + Color.END)
        if self.token == "":
            print("Token : " + Color.RED + Color.BOLD + "None\n" + Color.END)
        else:
            print("Token : " + Color.GREEN + Color.BOLD + self.token + "\n" + Color.END)

    # sauvegarde les identifiants dans un fichier (stored_user.txt)
    def store_user(self):
        filepath = "stored_user.txt"
        file = open(filepath, "w")
        file.write(self.username + "\n" + self.email + "\n" + self.password + "\n")

    # Vérifie si l'instance de la classe User a un token (généralement pas de token)
    def has_token(self):
        return self.token != ""

    # Récupère 2 hobbies aléatoire depuis le tableau de hobbies
    def choose_hobbies(self):
        return [random.choice(hobbies_list),
                random.choice(hobbies_list)]

    # Génère un user aléatoire (username, email). password = azeqsdazeqsd par défaut
    def generate_random_profile(self):
        print("Création d'un profil aléatoire")
        creds = self.fetch_identity()
        return [creds[0], creds[0] + "." + creds[1] + "@gmail.com"]
