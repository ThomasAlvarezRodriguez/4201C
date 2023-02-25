import json
import scrapy
from urllib.parse import urljoin
import re

class AmazonSearchProductSpider(scrapy.Spider): 
    name = "SSD-HDD" # Nom du spider, il est utilisé pour lancer le spider avec la commande: scrapy crawl SSD-HDD
    custom_settings = { # Paramètres custom pour le spider, dans notre cas on va utiliser le pipeline pour exporter les données dans un fichier csv
        'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv',}}
        }

    def start_requests(self): # Fonction qui va générer les requêtes pour récupérer les résultats de la recherche
        keyword_list = ['SSD','HDD'] # Liste des mots clés à rechercher sur Amazon
        for keyword in keyword_list: # Pour chaque mot clé on va générer une requête pour récupérer les résultats de la recherche
            amazon_search_url = f'https://www.amazon.fr/s?k={keyword}&page=1' # On génère l'url de la recherche en fonction du mot clé
            yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page': 1}) # On génère la requête et on passe le mot clé et le numéro de page en paramètre

    def discover_product_urls(self, response): # Fonction qui va récupérer les urls des produits
        page = response.meta['page'] # On récupère le numéro de page
        keyword = response.meta['keyword']  # On récupère le mot clé

        ## Discover Product URLs
        search_products = response.css("div.s-result-item[data-component-type=s-search-result]") # On récupère les produits de la page
        for product in search_products: # Pour chaque produit on va récupérer l'url du produit
            relative_url = product.css("h2>a::attr(href)").get()
            product_url = urljoin('https://www.amazon.fr/', relative_url).split("?")[0]
            yield scrapy.Request(url=product_url, callback=self.parse_product_data, meta={'keyword': keyword, 'page': page}) # On génère la requête et on passe le mot clé et le numéro de page en paramètre
            
        ## Get All Pages
        if page == 1:
            available_pages = response.xpath(
                '//a[has-class("s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
            ).getall()

            for page_num in available_pages:
                amazon_search_url = f'https://www.amazon.fr/s?k={keyword}&page={page_num}'
                yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page': page_num})


    def parse_product_data(self, response): # Fonction qui va récupérer les données du produit
        keyword = response.meta['keyword']
        price = response.css('.a-price span[aria-hidden="true"] ::text').get("")
        if not price: # Si le prix n'est pas trouvé on va chercher le prix dans un autre élément
            price = response.css('.a-price .a-offscreen ::text').get("") 
        yield { # On retourne les données du produit
            "name": response.css("#productTitle::text").get("").strip(),
            "asin": response.css("input#ASIN::attr(value)").get(),
            "price": price,
            "stars": response.css("i[data-hook=average-star-rating] ::text").get("").strip(),
            "rating_count": response.css("div[data-hook=total-review-count] ::text").get("").strip(),
            "keyword": keyword,
            "url": response.url,
            "description": response.css("#productDescription p::text").get("")
        }