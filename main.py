from tkinter.font import families
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from math import *
from InquirerPy import prompt
import os

# commande permettant de clear la console
clear = lambda: os.system('cls')

lienWikipedia = "https://fr.wikipedia.org"
lienPageRandom = lienWikipedia + "/wiki/Sp%C3%A9cial:Page_au_hasard"

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
        badLinks = ["/wiki/Aide", "/wiki/Projet", "/wiki/API", "/wiki/Wikip", "/wiki/Fichier", "action=edit", "https://www.wikidata", "https://fr.wiktionary.org/", "https://www.mediawiki.org/wiki/"]
        for para in soup.find_all('p'):
            #récupérer tout les liens dans les paragraphes
            for link in para.find_all('a'):
                if (link.text != "" and link.text[0] != "["):
                    result = any(ele in link['href'] for ele in badLinks)
                    if result == False:
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


# affiche le contenu passé en paramètre en gras et avec des sauts de ligne avant et après
def afficherMessage(message):
    clear()
    print()
    print('\033[1m' + message + '\033[0m')
    print()


# change l'affichage et les infos avec celles de la nouvelle page
def changementDePage(page):
    global titrePageActuelle
    titrePageActuelle = page['title']
    global liensPageActuelle
    liensPageActuelle = page['links']
    global nbLiensPageActuelle
    nbLiensPageActuelle = len(page['links'])
    global numTour
    numTour +=1
    pagination()
    clear()

# redéfini les infos de pagination
def pagination():
    # variables utiles à la pagination des liens d'une page
    global nbPagesPagination
    nbPagesPagination = nbLiensPageActuelle / 20
    if nbPagesPagination < 1:
        global paginationSuivante
        paginationSuivante = False
        global paginationPrecedente
        paginationPrecedente = False
    else:
        paginationSuivante = True
        paginationPrecedente = False
    global paginationDebut
    paginationDebut = 0
    global paginationFin
    paginationFin = 20
    global pageAffichee
    pageAffichee = 1
    global index
    index = paginationDebut + 1



#numéro du tour actuel
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


pagination()
clear()

# tant que le joueur n'est pas sur la bonne page on joue
while titrePageActuelle != titrePageCible:
    # header
    print('*'*10 + " WikiGame " + "*"*4 + " Tour " + str(numTour))
    print("Départ: " + titrePageDepart)
    print("Cible: " + titrePageCible)
    print("Actuellement: " + titrePageActuelle)
    print("-"*6 + " Page " + str(pageAffichee) + "-"*6)


    # options correspond aux liens hypertextes
    options = []

    # ajout dans l'objet du lien son numéro dans la liste
    for link in liensPageActuelle[paginationDebut:paginationFin]:
        strLinkCount = "0"+str(index) if len(str(index)) == 1 else str(index)
        link['numero'] = strLinkCount
        options.append(str(strLinkCount) + " " + str(link['libelle']))
        index += 1

    if paginationPrecedente == True:
        options.append('-- Page précédente --')

    if paginationSuivante == True:
        options.append('++ Page suivante ++')

    questions = [
        {
            "type": "list",
            "message": "Votre choix:",
            "choices": options,
        }
    ]
    result = prompt(questions)

    linkChoice = result[0]

    
    # traitement de l'input

    if linkChoice[:2] == "++":
        if paginationSuivante == True:
            afficherMessage('Page suivante !')
            paginationDebut += 20
            paginationFin += 20
            paginationPrecedente = True
            pageAffichee += 1

            # si on attend la dernière page
            if pageAffichee == ceil(nbPagesPagination):
                paginationSuivante = False
        else:
            afficherMessage("Il n'y a pas d'autre choix !")

        index = index = paginationDebut + 1

    elif linkChoice[:2] == "--":
        if paginationPrecedente == True:
            afficherMessage('Page précédente !')
            paginationDebut = paginationDebut - 20
            paginationFin = paginationFin - 20
            paginationSuivante = True
            pageAffichee = pageAffichee - 1

            # si on arrive sur la première page
            if pageAffichee == 1:
                paginationPrecedente = False
        else:
            afficherMessage("Vous êtes déjà sur la première page")
        
        index = paginationDebut + 1

    elif checkInputInteger(linkChoice[:2]) == False:
        afficherMessage("Il faut saisir un nombre !")
        index = paginationDebut + 1

    elif len(linkChoice[:2]) > 2:
        afficherMessage("Entrée incorrecte")
        index = paginationDebut + 1

    else:
        questions = [{"type": "confirm", "message": "Confirm ?", "default": True}]
        result = prompt(questions)
        confirm = result[0]

        if confirm == True:
            result = False

            # recherche de l'élément de la liste ayant le numéro entré par le joueur
            for link in liensPageActuelle[paginationDebut:paginationFin]:
                if linkChoice[:2] == link['numero']:
                    print("Vous avez choisi " + link["lien"])
                    nouvellePage = getInfosPage(lienWikipedia + link["lien"])

                    # si la prochaine page ne contient aucun lien on reste sur la page actuelle
                    if len(nouvellePage['links']) == 0:
                        afficherMessage('La page choisie ne contient aucun lien !')
                        result = True
                        index = paginationDebut + 1
                        break
                    else:
                        changementDePage(nouvellePage)
                        result = True
                        break
            
            # si aucune correspondance dans la liste
            if result == False:
                afficherMessage("Saisie incorrect !")
                index = paginationDebut + 1
        else:
            afficherMessage('Retour à la sélection')
            index = paginationDebut + 1

# message de victoire
phrase = "Vous avez gagné en " + str(numTour - 1)
print( phrase + " coup" if numTour - 1 == 1 else phrase + " coups")  