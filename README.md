Description technique de chaque fichier du projet ainsi que leur utilisation :

Dossier amazon/spiders :

Ce dossier comporte les spiders scrapy permettant l'extraction de données.

amazon_search.py : 

La classe AmazonSearchSpider hérite de la classe scrapy.Spider et définit un nom de spider (name) ainsi que des paramètres personnalisés (custom_settings) pour exporter les données extraites en format CSV.

La méthode start_requests génère une série de requêtes pour chaque mot-clé de recherche spécifié dans une liste (keyword_list), en utilisant une URL de recherche Amazon standard avec le mot-clé et la première page.

La méthode parse_search_results est le callback qui sera appelé pour chaque requête de recherche envoyée dans start_requests. Cette méthode parse les résultats de recherche de la page courante et extrait les informations souhaitées pour chaque produit (telles que l'ASIN, le titre, le prix, la note, etc.). Les données extraites sont ensuite retournées sous forme de dictionnaire.

Après avoir extrait les informations pour chaque produit sur la page courante, la méthode parse_search_results vérifie si la page courante est la première page de résultats de recherche. Si c'est le cas, elle récupère tous les numéros de page disponibles pour cette recherche à partir de l'élément HTML correspondant et génère des requêtes pour chaque page suivante en utilisant les mêmes paramètres que la requête initiale.