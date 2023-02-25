import scrapy
from urllib.parse import urljoin

class AmazonSearchSpider(scrapy.Spider): 
    name = "amazon_search" # Nom du spider, il est utilisé pour lancer le spider avec la commande: scrapy crawl amazon_search

    custom_settings = { # Paramètres custom pour le spider, dans notre cas on va utiliser le pipeline pour exporter les données dans un fichier csv
        'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv',}}
        }

    def start_requests(self):
        keyword_list = ['SSD','HDD'] # Liste des mots clés à rechercher sur Amazon 
        for keyword in keyword_list: # Pour chaque mot clé on va générer une requête pour récupérer les résultats de la recherche
            amazon_search_url = f'https://www.amazon.fr/s?k={keyword}&page=1' # Url de la recherche
            yield scrapy.Request(url=amazon_search_url, callback=self.parse_search_results, meta={'keyword': keyword, 'page': 1}) # On envoie la requête avec le callback qui va parser les résultats de la recherche

    def parse_search_results(self, response): # Fonction qui va parser les résultats de la recherche
        page = response.meta['page'] # On récupère la page courante
        keyword = response.meta['keyword']  # On récupère le mot clé de la recherche

        ## Extract Overview Product Data
        search_products = response.css("div.s-result-item[data-component-type=s-search-result]") # On récupère les produits de la page courante
        for product in search_products: # Pour chaque produit on va extraire les données
            relative_url = product.css("h2>a::attr(href)").get() # On récupère l'url relative du produit
            asin = relative_url.split('/')[3] if len(relative_url.split('/')) >= 4 else None # On récupère l'asin du produit
            product_url = urljoin('https://www.amazon.fr/', relative_url).split("?")[0] # On récupère l'url absolue du produit
            yield  { # On retourne un dictionnaire avec les données extraites
                    "keyword": keyword, 
                    "asin": asin,
                    "url": product_url,
                    "ad": True if "/slredirect/" in product_url else False, 
                    "title": product.css("h2>a>span::text").get(),
                    "price": product.css(".a-price[data-a-size=xl] .a-offscreen::text").get(),
                    "real_price": product.css(".a-price[data-a-size=b] .a-offscreen::text").get(),
                    "rating": (product.css("span[aria-label~=stars]::attr(aria-label)").re(r"(\d+\.*\d*) out") or [None])[0],
                    "rating_count": product.css("span[aria-label~=stars] + span::attr(aria-label)").get(),
                    "thumbnail_url": product.xpath("//img[has-class('s-image')]/@src").get(),
                    
                }


        ## Get All Pages
        if page == 1: 
            available_pages = response.xpath(  # On récupère les pages disponibles
                '//a[has-class("s-pagination-item")][not(has-class("s-pagination-separator"))]/text()' 
            ).getall() 

            for page_num in available_pages: # Pour chaque page on va générer une requête pour récupérer les résultats de la recherche
                amazon_search_url = f'https://www.amazon.fr/s?k={keyword}&page={page_num}' # Url de la recherche
                yield scrapy.Request(url=amazon_search_url, callback=self.parse_search_results, meta={'keyword': keyword, 'page': page_num}) # On envoie la requête avec le callback qui va parser les résultats de la recherche


        
    

