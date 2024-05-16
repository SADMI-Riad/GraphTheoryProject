# Graph Theory Application

## Description

Cette application de théorie des graphes est conçue pour aider les utilisateurs à créer, visualiser et manipuler des graphes. Elle permet de créer des sommets et des arcs, d'exécuter des algorithmes classiques tels que l'algorithme de Welsh-Powell pour le coloriage de graphes, l'algorithme de Prim pour trouver l'arbre couvrant minimum et l'algorithme de Dijkstra pour trouver le plus court chemin. Une fonctionnalité spéciale permet d'animer l'algorithme de Welsh-Powell pour visualiser le processus de coloriage.

## Fonctionnalités

- Création de sommets et d'arcs dans un graphe.
- Visualisation de l'ensemble stable maximal.
- Exécution et animation de l'algorithme de Welsh-Powell pour le coloriage de graphes.
- Exécution de l'algorithme de Prim pour trouver l'arbre couvrant minimum.
- Exécution de l'algorithme de Dijkstra pour trouver le plus court chemin.

## Installation

1. Clonez le dépôt du projet :
    ```sh
    git clone <URL_du_dépôt>
    cd <nom_du_dossier>
    ```

2. Installez les dépendances nécessaires :
    ```sh
    pip install -r requirements.txt
    ```

    Le fichier `requirements.txt` doit contenir les lignes suivantes :
    ```
    matplotlib
    networkx
    PyQt5
    ```

## Utilisation

1. Exécutez l'application principale :
    ```sh
    python main.py
    ```

2. Utilisez l'interface graphique pour :
   - Créer des sommets en cliquant sur le canevas.
   - Terminer la création des sommets en cliquant sur "Fin création sommets".
   - Ajouter des arcs en cliquant sur deux sommets et en entrant le poids de l'arc.
   - Terminer la création des arcs en cliquant sur "Fin création arcs".
   - Trouver l'ensemble stable maximal en cliquant sur "Trouver ensemble stable maximal".
   - Animer l'algorithme de Welsh-Powell en cliquant sur "Animer Welsh-Powell".
   - Exécuter l'algorithme de Prim en cliquant sur "Exécuter Prim".
   - Exécuter l'algorithme de Dijkstra en cliquant sur "Exécuter Dijkstra".

## Structure du Projet

- `main.py` : Point d'entrée principal de l'application.
- `gui.py` : Contient les classes pour l'interface graphique principale.
- `graph_operations.py` : Contient les fonctions pour dessiner et mettre à jour le graphe.
- `coloration.py` : Implémentation de l'algorithme de Welsh-Powell pour le coloriage de graphes.
- `prim.py` : Implémentation de l'algorithme de Prim pour trouver l'arbre couvrant minimum.
- `Dijkstra.py` : Implémentation de l'algorithme de Dijkstra pour trouver le plus court chemin.
- `Animation_window.py` : Contient la classe pour animer l'algorithme de Welsh-Powell.


## Exemple d'utilisation

# Creation des sommets et des arcs 
![Alt text](https://github.com/SADMI-Riad/GraphTheoryProject/blob/mohanned/images/GraphExemple1.png)

# Animation Welsh and Powell Algorithm (Coloration)
![Alt text](https://github.com/SADMI-Riad/GraphTheoryProject/blob/mohanned/images/WelshPowell.png)

## Auteurs

- Sadmi Mohammed Riad
- Mezghenna Mohanned


