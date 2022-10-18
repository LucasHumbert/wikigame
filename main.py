from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
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


lienPageRandom = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
numTour = 1

pageDepart = getInfosPage(lienPageRandom)
titrePageDepart = pageDepart['title']

titrePageCible = getInfosPage(lienPageRandom, 1)

titrePageActuel = titrePageDepart
liensPageActuelle = pageDepart['links']


print('*'*10 + " WikiGame " + "*"*4 + " Tour " + str(numTour))

print("Départ: " + titrePageDepart)
print("Cible: " + titrePageCible)
print("Actuellement: " + titrePageActuel)