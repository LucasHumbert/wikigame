# Wikigame

## Installation

Placer vous à la racine du projet et lancer la comande suivante pour installer les packages:

```
pip install -r requirements.txt
```

## Lancer le jeu 

A la racine du projet, lancer la commande

```
python main.js
```

Pour lancer les anciennes versions:

```
python old-versions/main-v*.py
```


## Règles du jeu

Le jeu récupère aléatoirement deux pages aléatoire du site [Wikipédia](https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal), le but étant, en partant de la première, de naviguer par les liens hypertextes afin d'arriver à la deuxième. Tout cela en faisant le moins de coups possible.

### Exemple

Je part de la page [Python](https://fr.wikipedia.org/wiki/Python_(langage)) et je doit aller à la page [République démocratique du Congo](https://fr.wikipedia.org/wiki/R%C3%A9publique_d%C3%A9mocratique_du_Congo)

- Je choisi le lien Pays Bas
- Puis Afrique du Sud
- Puis Afrique
- Et République démocratique du Congo
  
Gagné en 4 coups
