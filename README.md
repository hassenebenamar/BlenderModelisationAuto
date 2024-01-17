# Blender Modelisation Auto

## Ce projet s'inscrit dans le cadre de mon TAI de 5ème année d'ingénieur.

## Table des matières

- [Introduction](#Introduction)
- [Technologies](#Technologies)
- [Méthode](#Méthode)
- [Utilisation](#Utilisation)

## Introduction

Le projet se déroule dans le cadre de l'étude de modèle d'apprentissage automatique vision-language (LLM-VM). Afin d'évaluer ce genre de modèles, on utilise généralement des images réelles. 
Cette manière d'évaluer a pour inconvénient de dépendre de données ne pouvant être contrôlées (ex : biais présent dans les données).

Il existe déjà des jeux de données synthétiques en libre accès comme CLEVR mais ces derniers ne sont pas réalistes.

<img src="https://cdn.discordapp.com/attachments/1183508687923453956/1197284426502119524/clevr.jpg?ex=65bab503&is=65a84003&hm=d9193f0ca3edb7d69f54d64b62cd2b442666d0b1909a9bcc1c390ad9e6689e74&" alt="CLEVR">

Le but de ce projet est donc de créer de manière semi-automatique un jeu de données constitué d'images de synthèse annotées, réalisées à l'aide de Python et d'un logiciel de modélisation 3D, ici Blender. 

## Technologies

- Blender (Version 3.4)
- Python

## Méthode

Afin de créer le jeu de données d'images réalistes, le projet est réparti en plusieurs étapes :

- Création de scènes 3D dans Blender pour couvrir différents types d'environnements (example de scène 3D ci-dessous : chambre à coucher)

<img src="https://cdn.discordapp.com/attachments/1183508687923453956/1197285682947829790/blender_scene_room.png?ex=65bab62f&is=65a8412f&hm=897b44a8e1a7c089926ac6c02ec7a34f5eaead91278bd40bbf31d7a96603f0d6&" alt="blender-scene-room">

- Implémentation de scripts Python et utilisation de l'API Python de Blender pour interagir avec les objets 3D et modifier leurs attributs.

- Rendu et annotation des images (exemple de rendu et annotation des images ci-dessous : scène de salle à manger et cuisine).

<img src="https://cdn.discordapp.com/attachments/1183508687923453956/1197287473798185060/kitchen_render_1_lightPower_4000.0.png?ex=65bab7da&is=65a842da&hm=b232294d6068065fb240ccf342d0a739c7cbef50f6b9c70410726de314f6affe&" alt="kitchen-render">
<img src="https://cdn.discordapp.com/attachments/1183508687923453956/1197287956256411648/image.png?ex=65bab84d&is=65a8434d&hm=334fa938fb3991e1f742dddbbf358332f7fb0671a065819a8bdba4bc410b7309&" alt="annotation" width=65%>

## Utilisation

Afin de lancer le projet, il suffit d'avoir Blender installé sur sa machine. (Version 3.4).
Des scènes sont disponibles dans le dossier "scenes" et tous les modèles utilisés sont dans le dossier "models".

Lorsque la scène est chargée, il suffit de cliquer sur l'onglet 'Scripting' dans Blender pour faire apparaître cette interface.

<img src="https://cdn.discordapp.com/attachments/1183508687923453956/1197289927931613184/scripting_window.jpg?ex=65baba23&is=65a84523&hm=397df62c98c166206f49c6e6e4a60c907f23599f8638c2cf411da4d9f7bf548f&" alt="scripting window">

Vous pourrez ensuite charger le script correspondant à la scène contenu dans le dossier "scripts" et le lancer via le button play (cercle vert dans la capture ci-dessus).
#### Il est important de préciser que le script Python peut être édité en dehors de Blender mais il ne peut être lancé qu'à partir de la fenêtre de scripting ci-dessus.
Il ne reste qu'à changer les paths par rapport à votre machine et de décider des noms des fichiers pour le processus d'enregistrement (la constante OUTPUT_DIR ainsi que les variables render_file_path et json_file_path).

