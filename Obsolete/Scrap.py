import scrapy
from urllib.parse import urljoin
import csv

# Création d'une classe qui hérite de la classe Spider de Scrapy
class Product(scrapy.Spider):
# Définition du nom du spider
    name = "Product"

# Définition des paramètres du spider
custom_settings = {
    'FEEDS': {'product_info.csv': {'format': 'csv', 'fields': ['asin', 'name', 'price', 'stars', 'rating_count']}}
}

# Définition de la méthode start_requests
def start_requests(self):
# récupération des données du fichier csv
    with open('C:/Users/eityg/Git/4201C/ASIN.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            # récupération de l'asin
            asin = row[0]
            # création de l'url
            url = f'https://www.amazon.fr/dp/{asin}'
            # création de la requête
            yield scrapy.Request(url=url, callback=self.parse)

# Définition de la méthode parse
def parse(self, response):
    # récupération de l'asin
    asin = response.url.split('/')[-1]
    # récupération du nom du produit
    name = response.css('#productTitle::text').get()
    # récupération du prix du produit
    price = response.css('#priceblock_ourprice::text').get()
    # récupération du nombre d'étoiles
    stars = response.css('#acrPopover::attr(title)').get()
    # récupération du nombre de notes
    rating_count = response.css('#acrCustomerReviewText::text').get()
    # récupération des propriétés du produit
    properties = response.css('#detailBullets_feature_div .content li')
    # création d'un dictionnaire pour stocker les propriétés
    properties_dict = {}
    # boucle sur les propriétés
    for prop in properties:
        # récupération de la propriété
        key = prop.css('span::text').get()
        # récupération de la valeur de la propriété
        value = prop.css('span + span::text').get()
        # ajout de la propriété dans le dictionnaire
        properties_dict[key] = value
    # création d'un dictionnaire pour stocker les données
    data = {
        'asin': asin,
        'name': name,
        'price': price,
        'stars': stars,
        'rating_count': rating_count,
        'properties': properties_dict
    }
    # retour des données
    yield data




