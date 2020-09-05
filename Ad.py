import json

import User
from Color import *
from Parameters import Parameters
from StudioTimeCrawler import StudioTimeCrawler
from Globals import prod_url, preprod_url
from library import requests

# Contient toutes les infos nécessaires à la création d'une annonce
class Ad:
    def __init__(self, user: User, studio_time_crawler: StudioTimeCrawler, parameters: Parameters):
        self.base_url = parameters.get_url_from_parameter()
        self.token_user = user.token if user.token != "" else user.api_get_token()
        self.id_user = user.api_get_user_id()
        self.ad_id = ""
        new_ad_informations = studio_time_crawler.extract_infos_from_random_studio()
        self.name = new_ad_informations['title']
        self.description = new_ad_informations['description']
        self.studio_type = new_ad_informations['studio_type']
        self.availability_type = new_ad_informations['availability_type']
        self.availability = new_ad_informations['availability']
        self.start_hour = new_ad_informations['start_hour']
        self.end_hour = new_ad_informations['end_hour']
        self.time_of_notice = new_ad_informations['time_of_notice']
        self.reference = new_ad_informations['references']
        self.amenities = new_ad_informations['amenities']
        self.materiel = new_ad_informations['materiel']
        self.address = new_ad_informations['address']
        self.city = new_ad_informations['city']
        self.country = new_ad_informations['country']
        self.prix = new_ad_informations['price']
        self.audio_engineer = new_ad_informations['audio_engineer']
        self.post_production = new_ad_informations['post_prod']
        self.photo = new_ad_informations['photo']
        self.user_agreement = True
        self.minimum_booking = 3
        self.max_studio_occupancy = 3

    # Réaliser une requête sur l'API piur créer une annonce.
    # Le body est directement passé en paramètre
    def api_create_ad(self, body: json) -> bool:
        global prod_url, preprod_url

        data = json.dumps(body)
        url = self.base_url + "/create"
        # print(url)
        header = {
            'custom_auth': "authorization=Token " + self.token_user,
            'Content-Type': 'application/json'
        }
        request = requests.post(url=url, data=data, headers=header)
        res = request.json()
        print(res)

        if request.status_code == 200 and res['res'].find("Added") != -1:
            if body['bearing'] == 1:
                self.ad_id = res['_id']
            return True
        else:
            print(Color.BOLD + Color.RED + "Erreur :\n" + Color.END + Color.CYAN + str(res) + Color.END)

            return False

    # Print quelques champs (manque start et end hour)
    def print_ad(self):
        print("name : " + self.name)
        print("description : " + self.description)
        print("studio_type : " + self.studio_type)
        print("availability_type : " + self.availability_type)
        print("availability : " + str(self.availability))
        print("time_of_notice : " + self.time_of_notice)
        print("reference : " + self.reference)
        print("amenities : " + str(self.amenities))
        print("materiel : " + str(self.materiel))
        print("address : " + self.address)
        print("city : " + self.city)
        print("country : " + self.country)
        print("prix : " + str(self.prix))
        print("audio_engineer : " + str(self.audio_engineer))
        print("post_production : " + str(self.post_production))
