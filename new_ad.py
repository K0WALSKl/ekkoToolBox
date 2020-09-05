import json
import os
from Ad import Ad
from Color import *
from new_user import *
from StudioTimeCrawler import *


# Point d'entrée de la fonction de création d'annonce
# Vérifie si on a un user pour créer l'annonce et lance la requête
# Après avoir piqué des infos chez studio time
def new_ad(parameters):
    print("Création de une ou plusieurs nouvelles annonces")
    stored_user = get_stored_user()
    user = User(stored_user[0], stored_user[1], stored_user[2], parameters)
    crawler = StudioTimeCrawler()

    # Si l'username est vide, c'est qu'il n'y a pas le fichier stored_user.txt
    # On ne peut donc pas créer d'annonce (car par d'utilisateur disponible)
    if len(user.username) == 0:
        print_bold_error("Il faut d'abord créer un nouvel utilisateur (-nu)")
        return False

    print_success("Utilisateur trouvé")
    if not user.has_token():
        res = user.api_get_token()
        if res is False:
            print_bold_error("Ce profil ne semble pas exister. Annulation")
            os.popen("mv ./stored_user.txt ./old_stored_user.txt")
            return False
    user.print_user_info()
    user.api_get_user_id()
    create_ad_all_steps(crawler, parameters, user)


def create_ad_all_steps(crawler, parameters, user):
    ad = Ad(user, crawler, parameters)

    if create_ad_first_step(ad) is False:
        return False
    if create_ad_second_step(ad) is False:
        return False
    if create_ad_third_step(ad) is False:
        return False
    if create_ad_fourth_step(ad) is False:
        return False
    if create_ad_fifth_step(ad) is False:
        return False


# Lance la requête de création d'annonce pour la 5ème étape
# Retourne True si l'annonce a bien été ajoutée
def create_ad_fifth_step(ad) -> bool:
    # print_error("MDR")
    # print(str(ad.photo))
    res = ad.api_create_ad({
        'user_agreement': True,
        'photos': "data:image/png;base64,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",
        'bearing': 5,
        'isCompleted': False,
        'id': ad.ad_id
    })
    print_success("Création d'annonce : Étape 5/5 OK")
    return res


# Lance la requête de création d'annonce pour la 4ème étape
# Retourne True si l'annonce a bien été ajoutée
def create_ad_fourth_step(ad) -> bool:
    res = ad.api_create_ad({
        'prix': ad.prix,
        'audio_engineer': ad.audio_engineer,
        'post_production': ad.post_production,
        'bearing': 4,
        'isCompleted': False,
        'id': ad.ad_id
    })
    print_success("Création d'annonce : Étape 4/5 OK")
    return res


# Lance la requête de création d'annonce pour la 3ème étape
# Retourne True si l'annonce a bien été ajoutée
def create_ad_third_step(ad) -> bool:
    res = ad.api_create_ad({
        'address': ad.address,
        'city': ad.city,
        'country': ad.country,
        'bearing': 3,
        'isCompleted': False,
        'id': ad.ad_id
    })
    print_success("Création d'annonce : Étape 3/5 OK")
    return res


# Lance la requête de création d'annonce pour la 2ème étape
# Retourne True si l'annonce a bien été ajoutée
def create_ad_second_step(ad) -> bool:
    res = ad.api_create_ad({
        'amenities': ad.amenities,
        'materiel': ad.materiel,
        'bearing': 2,
        'isCompleted': False,
        'id': ad.ad_id
    })
    print_success("Création d'annonce : Étape 2/5 OK")
    return res


# Lance la requête de création d'annonce pour la 1ere étape
# Retourne True si l'annonce a bien été ajoutée
def create_ad_first_step(ad) -> bool:
    res = ad.api_create_ad({
        'name': ad.name,
        'description': ad.description,
        'studio_type': ad.studio_type,
        'minimum_booking': ad.minimum_booking,
        'max_studio_occupancy': ad.max_studio_occupancy,
        'availability_type': ad.availability_type,
        'availability': [],
        'time_of_notice': ad.time_of_notice,
        'references': ad.reference,
        'bearing': 1,
        'isCompleted': False,
        'created': False
    })
    print_success("Création d'annonce : Étape 1/5 OK")
    return res