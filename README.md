Description technique de chaque fichier du projet ainsi que leur utilisation :

Dossier amazon/spiders :

Ce dossier comporte les spiders scrapy permettant l'extraction de données.

Les spiders utilisés sont des versions modifiées basées sur le tutoriel présent sur ce git : 
https://github.com/python-scrapy-playbook/amazon-python-scrapy-scraper

amazon_search.py : 

La classe AmazonSearchSpider hérite de la classe scrapy.Spider et définit un nom de spider ainsi que des paramètres personnalisés pour exporter les données extraites en format CSV.

La méthode start_requests génère une série de requêtes pour chaque mot-clé de recherche spécifié dans une liste, en utilisant une URL de recherche Amazon avec le mot-clé et la première page.

La méthode parse_search_results est le callback qui sera appelé pour chaque requête de recherche envoyée dans start_requests. Cette méthode parse les résultats de recherche de la page courante et extrait les informations souhaitées pour chaque produit. Les données extraites sont ensuite retournées sous forme de dictionnaire.

Après avoir extrait les informations pour chaque produit sur la page courante, la méthode parse_search_results vérifie si la page courante est la première page de résultats de recherche. Si c'est le cas, elle récupère tous les numéros de page disponibles pour cette recherche à partir de l'élément HTML correspondant et génère des requêtes pour chaque page suivante en utilisant les mêmes paramètres que la requête initiale.

amazon_search_product.py :

C'est un spider similaire à amazon_search, mais récupère en plus les données de chaque produit en allant sur sa page au lieu de rester sur la page de résultats de recherche. Il sera plus complet, mais plus lent et a plus de chances d'omettre des résultats. Les scrapers pourraient être plus optimisés, mais la sécurité d'Amazon complique la tâche et nous obtenons déjà assez de données.

La fonction start_requests génère des requêtes pour récupérer les résultats de la recherche Amazon pour chaque mot-clé spécifié dans la liste keyword_list. Chaque requête est générée en fonction du mot-clé et de la page, et est transmise à la fonction discover_product_urls().

La fonction discover_products_urls récupère les URL des produits pour chaque page de résultats de recherche. Elle utilise la méthode css pour extraire les éléments HTML qui contiennent les données du produit, notamment l'URL relative du produit. L'URL absolue est ensuite construite en utilisant la fonction urljoin, puis chaque URL est transmise à la fonction parse_product_data().

parse_product_data(): Cette fonction récupère les données du produit à partir de chaque URL de produit. Elle utilise la méthode css pour extraire les éléments HTML contenant le nom, l'ASIN, le prix, les étoiles, le nombre d'avis, le mot-clé, l'URL et la description du produit. Les données sont ensuite stockées dans un dictionnaire et renvoyées.

Dossier amazon :

Ce dossier, en plus de contenir le dossier spiders, contient plusieurs fichiers python : items, middlewares, pipelines, settings.
Ce sont des fichiers nécessaires pour que les spiders fonctionnent.

Dossier Obsolete : 

Contient des fichiers n'étant plus utilisés dans le code final. Il y a dedans des versions intermédiaires, des fausses pistes et des approches différentes de celle qui a finalement été adoptée. Nous le conservons car il son contenu nous a permis d'obtenir la compréhension nécessaire au reste du projet. 

Dossier static : 

Contient la fiche de style css, utilisée par les .html de l'application Flask afin de styliser les pages.

Dossier templates : 

Contient les html affichant les pages de l'application Flask.

Les fichiers .csv : 

Data.csv est le résultat de la combinaison de deux fichiers (dans Obsolete) obtenus par scraping et traités par DataPrep.py (également dans Obsolete). 
Traitement.csv est un fichier qui ne contient que l'ASIN et le prix des produits car certains produits n'avaient pas de prix. Ce fichier permet de récupérer les données manquantes. Il est obtenu par un mélange de scraping et de contrôle manuel. 
DataTraite.csv correspond au fichier Data.csv lourdement modifié par Traitement.py

Traitement.py :

