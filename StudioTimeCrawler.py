import random
import time

from Color import *
import os
import os.path
from os import path
from library.selenium import webdriver
from library.selenium.webdriver.firefox.options import Options
from Globals import browser_file_path, browsers, materiels_list, link_files, studio_time_ads_links_list
import re
import base64


def get_description_without_html_tags(description_with_html_tags) -> str:
    raw_description = ""

    for line in description_with_html_tags:
        raw_description += line.get_attribute('innerHTML')
    cleanregex = re.compile('<.*?>')
    cleaned_description = re.sub(cleanregex, '', raw_description)
    cleaned_description.replace("... Show moreShow less", "")
    cleaned_description.replace("Show more", "")
    return cleaned_description


def generate_materiels():
    global materiels_list
    return [
        random.choice(materiels_list)
        , random.choice(materiels_list)
        , random.choice(materiels_list)
        , random.choice(materiels_list)
        , random.choice(materiels_list)]


def find_classes_that_starts_with(xpath, driver):
    return driver.find_elements_by_xpath(xpath)


def find_href_that_starts_with(xpath, driver):
    return driver.find_elements_by_xpath(xpath)


def get_ad_links_from_webpage(elements):
    links = []

    for elem in elements:
        link = elem.get_attribute('href')
        print(link)
        if link and len(link) > 35 and link.find("https://www.studiotime.io/l/") != -1:
            links.append(link)
    return links


def get_price_from_studio(driver) -> int:
    price_array = find_classes_that_starts_with(
        "//*[starts-with(@class, 'ListingPage__desktopPriceValue__')]", driver
    )
    price = price_array[0].get_attribute("innerHTML").replace("$", "").split(".")[0]
    return int(price)


def get_picture_from_studio(driver):
    photo_array = find_classes_that_starts_with(
        "//*[starts-with(@class, 'ListingPage__rootForImage__')]", driver
    )
    img = base64.b64decode(photo_array[0].screenshot_as_base64)
    return img


def get_random_full_address():
    lines = open('addr.csv').read().splitlines()
    return random.choice(lines)


def get_amenities_from_studio(driver):
    ad_sections_array = find_classes_that_starts_with(
    "//*[starts-with(@class, 'section__root__')]", driver)

    for section in ad_sections_array:
        html_section = section.get_attribute('outerHTML')
        print(html_section)
    return 'Kitchen, Toilets'


class StudioTimeCrawler:
    def __init__(self):
        self.driver_loaded = False

    def extract_infos_from_random_studio(self):
        # get_chosen_browser()
        driver = get_selenium_driver()
        # studio_link = "https://www.studiotime.io/l/lafx-recording-studio/5aa916c5-b841-4064-b6ab-d7f1a470a498"
        studio_link = random.choice(studio_time_ads_links_list)
        print_bold_warning(studio_link)
        driver.get(studio_link)
        title = self.get_title_from_studio(driver)
        description = self.get_description_from_studio(driver)
        studio_type = "Home studio"# A modifier si on veut autre chose
        availability_type = self.generate_availability_type()
        availability = self.generate_availability(availability_type)
        start_hour = self.generate_start_hour(availability_type)
        end_hour = self.generate_end_hour(start_hour, availability_type)
        time_of_notice = self.generate_time_of_notice()
        references = "https://soundcloud.fr/"
        amenities = get_amenities_from_studio(driver)
        materiel = generate_materiels()
        full_address = get_random_full_address().split(',')
        print(str(full_address))
        address = full_address[0] + " " + full_address[1]
        city = full_address[3]
        country = "France"
        price = get_price_from_studio(driver)
        audio_engineer = {'active': False, 'price': 0}
        post_prod = {'active': False, 'price': 0}
        photo = get_picture_from_studio(driver)
        materiel = generate_materiels()
        driver.quit()
        return {
            'title': title,
            'description': description,
            'studio_type': studio_type,
            'availability_type': availability_type,
            'availability': availability,
            'time_of_notice': time_of_notice,
            'references': references,
            'amenities': amenities,
            'materiel': materiel,
            'address': address,
            'city': city,
            'country': country,
            'price': price,
            'audio_engineer': audio_engineer,
            'post_prod': post_prod,
            'photo': photo,
            'start_hour': start_hour,
            'end_hour': end_hour
        }
        # return [title, description, studio_type, availability_type, availability, time_of_notice, references,
        #         amenities, materiel, address, city, country, price, audio_engineer, post_prod, photo,
        #         start_hour, end_hour]

    def generate_end_hour(self, start_hour, availability_type):
        if availability_type == "daily":
            return random.randint(start_hour, 23)
        return ""

    def generate_start_hour(self, availability_type):
        if availability_type == "daily":
            return random.randint(1, 20)
        return ""

    def generate_availability(self, availability_type):
        if availability_type == "daily":
            availability = []
            days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
            for i in range(3):
                availability.append(random.choice(days))
            return availability

    def generate_availability_type(self):
        return random.choice(["on_demand", "daily", "always"])

    def generate_time_of_notice(self):
        return random.choice(["Pas de préavis", "1 Semaine", "3 Jours", "2 heures", "24 heures"])

    def click_show_more_if_exists(self, driver):
        links_show_more = find_href_that_starts_with(
            "//*[starts-with(@href, 'more')]", driver)
        if len(links_show_more) > 0:
            link = links_show_more[0]
        return link

    def get_title_from_studio(self, driver):
        titles = find_classes_that_starts_with(
            "//*[starts-with(@class, 'ListingPage__richTitle')]", driver)
        title = titles[0].get_attribute('innerHTML').replace("<!-- -->", "")
        return title

    def get_description_from_studio(self, driver):
        link = self.click_show_more_if_exists(driver)
        description_with_html_tags = find_classes_that_starts_with(
            "//*[starts-with(@class, 'ListingPage__description__')]", driver
        )
        description = get_description_without_html_tags(description_with_html_tags)
        return description

    def generate_disponibilites(self):
        pass

    def get_services_from_studio(self, driver):
        pass

    def get_random_ad(self):
        pass

    def get_all_ads_links(self):
        global link_files

        get_chosen_browser()
        base_url = "https://www.studiotime.io"
        driver = get_selenium_driver()
        all_links = open(link_files, "w")

        for i in range(27):
            if i == 0:
                url = base_url + "/s/all?address=%C3%89tats-Unis&bounds=49.38%2C-66.94%2C25.82%2C-124.39"
            else:
                url = base_url + "/s/all?address=%C3%89tats-Unis&bounds=49.38%2C-66.94%2C25.82%2C-124.39&page=" + str(i - 1)

            print_warning(url)
            driver.get(url)
            time.sleep(3)
            find_classes_that_starts_with(
                "//*[starts-with(@class, 'ListingCard__root__')]", driver)
            studio_links = get_ad_links_from_webpage(driver.find_elements_by_tag_name('a'))
            print(studio_links)
            all_links.write("%s" % str(studio_links))
        all_links.close()




def browser_not_chosen():
    global browser_file_path

    if not path.exists(browser_file_path):
        return True
    return False


def choose_browser() -> int:
    value = -1

    while int(value) != 0 and int(value) != 1 and int(value) != 2 and int(value) != 3:
        print_warning("Configuration rapide de Selenium :")
        print("Quel browser utilises-tu ?")
        print("0 : Firefox")
        print("1 : Chrome V85.*")
        print("2 : Chrome V84.*")
        print("3 : Chrome V83.*")
        value = input("Tape le nombre qui correspond : ")
    return int(value)


# Sauvegarde le browser choisi dans un fichier
def save_choice(choice):
    global browser_file_path, browsers
    browsers = ["Firefox", "Chrome V.85", "Chrome V.84", "Chrome V.83"]

    file = open(browser_file_path, "w")
    file.write(browsers[choice])


def load_browser() -> str:
    global browser_file_path
    browser = ""

    with open(browser_file_path) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            browser = line.strip()
            line = fp.readline()
            cnt += 1
    return browser


def get_os():
    os_name = os.popen("uname -s").read()
    if os_name:
        if os_name.find("Linux") != -1:
            return "linux"
        else:
            return "mac"
    return "NOT_FOUND"


def copy_driver(os_name, choice):
    global browsers
    browser = "firefox" if choice == 0 else "chrome"
    driver_path = "./web_drivers/" + browser + "/" + os_name + "/" \
                  + ("geckodriver" if choice == 0 else "chromedriver")

    result = os.popen(
        "sudo cp \"" + driver_path + "\" /usr/local/bin")
    return True


def install_driver(choice) -> bool:
    os_name = get_os()
    if os_name == "NOT_FOUND":
        print("0: Linux\n1: Mac")
        os_name = input("OS Non détecté, choix manuel. Quel est l'os ? ")
        if os_name == 0:
            os_name = "linux"
        elif os_name == 1:
            os_name = "mac"
        else:
            return False

    return copy_driver(os_name, choice)


def get_chosen_browser() -> str:
    # if browser_not_chosen():
    #     choice = choose_browser()
    #     save_choice(choice)
    #     if install_driver(choice) == False:
    #         return "ERROR"
    # return load_browser()
    if browser_not_chosen():
        if install_driver(0) == False:
            return "ERROR"
        else:
            return "OK"
    return load_browser()


def get_selenium_driver():
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.headless = True
    return webdriver.Remote(
        command_executor='http://52.169.120.202:4444/wd/hub',
        options=firefox_options
    )

    # return webdriver.Firefox(options=options, executable_path='./library/geckodriver')
