Ce projet nécessite l'installation de Python et de certaines librairies. 
La commande:  pip install -r requirements.txt permet d'installer les librairies nécessaires au bon fonctionnement du projet.

Il faut également installer MongoDB pour pouvoir stocker les données sur le port par défaut (27017).
Vous pouvez télécharger MongoDB ici : https://www.mongodb.com/try/download/community

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
Ce sont des fichiers nécessaires pour que les spiders fonctionnent et contourner la protection anti scraping d'Amazon.

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

Ce fichier a pour but de traiter les données des fichiers csv pour obtenir de meilleures informations. 
Le traitement consiste à extraire les capacités de stockage, harmoniser les capacités en les mettant en Go, supprimer les lignes sans capacité de stockage, convertir les colonnes "stars" et "rating_count" en float et enfin insérer les données dans une collection MongoDB.

Traitement.py utilise les librairies pandas, numpy, re et pymongo. Il lit les fichiers Data.csv et traitement.csv, et stocke les noms des produits dans une liste nom.

On utilise regex_capacite pour extraire la capacité de stockage de la colonne "name". La fonction extraire_capacite est utilisée pour appliquer l'expression régulière à la colonne "name" et créer une nouvelle colonne "capacity", globalement on obtient la capacité de stockage pour chaque produit en fonction de son nom.

Les capacités de stockage sont harmonisées en utilisant la fonction harmoniser_capacite qui convertit les capacités en Go, en multipliant par 1000 pour les capacités en To ou TB.

Le fichier supprime les virgules et les espaces insécables des colonnes "name", "stars" et "rating_count" en utilisant la méthode str.replace() de pandas. Les valeurs "nan" sont remplacées par "Inconnu" en utilisant la méthode replace() de pandas, Étant donnée qu'il n'y avait pas beaucoup de valeurs "Iconnues" (3 ou 4), nous avons décidé de les supprimer. 
Les données des fichiers Data.csv et traitement.csv sont combinées en utilisant la méthode merge() de pandas, en utilisant la colonne "asin" comme clé. Les doublons sont ensuite supprimés et la colonne "price" de Data est remplacé par celle de traitement, car elle est plus complète.
La colonne "stars" est modifiée pour garder seulement les trois premiers caractères afin de ne garder que les nombres, de même on ne garde que les chiffres de la colonne "rating_count". 
On convertit les colonnes "stars" et "rating_count" en float afin de pouvoir les utiliser pour les calculs. puis on sauvegarde les données dans un fichier csv. "DataTraite.csv."

On entame ensuite une connexion à MongoDB en utilisant la méthode MongoClient() de pymongo.
Les données sont ensuite insérées dans une collection MongoDB en utilisant la méthode insert_many() de pymongo. cette collection est appelée "SSD-HDD" et est stockée dans une base de données "4201C".

Fichier App.py :

Ce fichier contient le code de l'application Flask.

Cette application permet de visualiser les données obtenues par le scraping et le traitement des données.

L'application comporte plusieurs pages : une page d'accueil, une page contenant un tableau, une page avec des graphiques, une page avec les chiffres clés et une page avec les 10 meilleurs produits.

La fonction index() est le point d'entrée de l'application et est exécutée lorsque l'utilisateur accède à l'URL de l'application : 
- Si la requête est de type GET, la fonction extrait la valeur du paramètre "page" de l'URL et affiche la page correspondante. 
- Si la requête est de type POST, la fonction extrait la valeur du paramètre "page" du formulaire et redirige vers la page correspondante.

Selon la page demandée, la fonction index() effectue différentes actions pour extraire les données MongoDB appropriées. 

- Par exemple, pour la page de tableau, la fonction récupère les données de la collection "SSD-HDD" de la base de données MongoDB, puis les affiche dans un tableau HTML. 
- Pour la page de graphiques, la fonction extrait les données pour tracer différents graphiques de prix et de capacités de stockage en utilisant la bibliothèque Plotly. 
- Pour la page textuelle, la fonction effectue des calculs sur les données et affiche les résultats textuels. 
- Pour la page top_10, la fonction affiche les 10 meilleurs produits selon le nombre de notes.

La fonction index() utilise la fonction render_template() pour générer des pages HTML dynamiques à partir de fichiers de modèles. 
Les fichiers de modèle contiennent du code HTML, ainsi que des variables qui sont remplacées par les données lors de la génération de la page. 
Ils sont stockés dans le répertoire "templates" de l'application Flask.

Enfin, la fonction index() exécute l'application Flask en appelant la fonction app.run(). Cela permet à l'application de répondre aux requêtes des utilisateurs et de générer des pages web dynamiques en temps réel.