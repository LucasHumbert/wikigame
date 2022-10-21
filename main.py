from tkinter.font import families
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from math import *
import re
import sys

# récupère le titre ainsi que les liens présents dans la page donnée en paramètre
def getInfosPage(lien, cible = 0):
    req = Request(
        url=lien, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')

    title = soup.find("h1", {"id": "firstHeading"})
    
    if (cible == 0):
        links = []
        for para in soup.find_all('p'):
            #récupérer tout les liens dans les paragraphes
            for link in para.find_all('a'):
                if (link.text != "" and link.text[0] != "["):
                    if ("/wiki/Aide" not in link['href']):
                        if ("/wiki/Projet" not in link['href']):
                            if ("/wiki/Wikip" not in link['href']):
                                if("action=edit" not in link['href']):
                                    if("https://www.wikidata" not in link['href']):
                                        links.append({'libelle': link.text, 'lien': link['href']})
        return {'title' : title.text, 'links' : links}
    else:
        return title.text

# vérification que l'input du joueur est bien un integer
def checkInputInteger(input):
    try:
        val = int(input)
        return True
    except ValueError:
        return False

lienPageRandom = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
numTour = 1

# récupération de la page de départ et de son titre
pageDepart = getInfosPage(lienPageRandom)
titrePageDepart = pageDepart['title']

# récupération de la ppage cible
titrePageCible = getInfosPage(lienPageRandom, 1)

# infos sur la page sur laquelle se trouve le joueur
titrePageActuelle = titrePageDepart
liensPageActuelle = pageDepart['links']
nbLiensPageActuelle = len(pageDepart['links'])


# variables utiles à la pagination des liens d'une page
nbPagesPagination = nbLiensPageActuelle / 20
if nbPagesPagination < 1:
    paginationSuivante = False
    paginationPrecedente = False
else:
    paginationSuivante = True
    paginationPrecedente = False
paginationDebut = 0
paginationFin = 20
pageAffichee = 1
index = paginationDebut + 1

# tant que le joueur n'est pas sur la bonne page on joue
while titrePageActuelle != titrePageCible:

    # header
    print('*'*10 + " WikiGame " + "*"*4 + " Tour " + str(numTour))
    print("Départ: " + titrePageDepart)
    print("Cible: " + titrePageCible)
    print("Actuellement: " + titrePageActuelle)
    print("-"*6 + " Page " + str(pageAffichee) + "-"*6)

    # affichage des liens en ajoutant dans l'objet son numéro dans la liste
    for link in liensPageActuelle[paginationDebut:paginationFin]:
        strLinkCount = "0"+str(index) if len(str(index)) == 1 else str(index)
        link['numero'] = strLinkCount
        index += 1
        print(strLinkCount + " - " + str(link['libelle']))

    if paginationPrecedente == True:
        print('98 - Page précédente')

    if paginationSuivante == True:
        print('99 - Page suivante')
    
    # attente du choix de l'utilisateur
    userInput = input('Votre choix: ')
    
    # traitement de l'input

    if userInput == "99":
        if paginationSuivante == True:
            print()
            print('\033[1m' + 'Page suivante !' + '\033[0m')
            print()
            paginationDebut += 20
            paginationFin += 20
            paginationPrecedente = True
            pageAffichee += 1

            # si on attend la dernière page
            if pageAffichee == ceil(nbPagesPagination):
                paginationSuivante = False
        else:
            print()
            print('\033[1m' + "Il n'y a pas d'autre choix !" + '\033[0m')
            print()
        index = index = paginationDebut + 1

    elif userInput == "98":
        if paginationPrecedente == True:
            print()
            print('\033[1m' + 'Page précédente !' + '\033[0m')
            print()
            paginationDebut = paginationDebut - 20
            paginationFin = paginationFin - 20
            paginationSuivante = True
            pageAffichee = pageAffichee - 1

            # si on arrive sur la première page
            if pageAffichee == 1:
                paginationPrecedente = False
        else:
            print()
            print('\033[1m' + "Vous êtes déjà sur la première page" + '\033[0m')
            print()
        index = paginationDebut + 1

    elif checkInputInteger(userInput) == False:
        print()
        print('\033[1m' + "Il faut siasir un nombre !" + '\033[0m')
        print()
        index = paginationDebut + 1

    elif len(userInput) > 2:
        print()
        print('\033[1m' + "Entrée incorrecte" + '\033[0m')
        print()
        index = paginationDebut + 1

    else:
        if len(userInput) == 1:
            userInput = "0" + userInput
        for link in liensPageActuelle[paginationDebut:paginationFin]:
            if userInput == link['numero']:
                print("Vous avez choisi " + link["libelle"])
    