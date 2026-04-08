# 🧠 Automate Fini — Projet Scolaire

## 📚 Contexte

Ce projet a été réalisé dans le cadre d’un cours d’informatique sur les **automates finis**.

L’objectif est de développer un programme en Python permettant de lire, analyser et transformer des automates à partir de fichiers texte, en appliquant les concepts fondamentaux de la théorie des langages formels.

---

## ⚙️ Fonctionnalités

Le programme permet de :

### 📥 Lecture et représentation

* Lire un automate depuis un fichier `.txt`
* Gérer :

  * les états
  * les états initiaux et finaux
  * les transitions
  * les epsilon-transitions (`£`)

---

### 🔍 Analyse des automates

* Vérifier si un automate est :

  * déterministe
  * complet
  * standard
  * minimal

---

### 🔁 Transformations

* Déterminisation (méthode des sous-ensembles)
* Complétion (ajout d’un état poubelle)
* Standardisation
* Complémentaire
* Minimisation (algorithme de Moore)

---

### 🧪 Simulation

* Reconnaissance de mots
* Gestion des epsilon-transitions via fermeture transitive

---

## 🧩 Format du fichier d’entrée

Un automate est défini dans un fichier texte structuré comme suit :

```text
nombre_de_symboles
nombre_d_etats
nombre_etats_initiaux etats_initiaux...
nombre_etats_finaux etats_finaux...
nombre_de_transitions
etat_depart symbole etat_arrivee
...
```

### Exemple :

```text
2
3
1 0
1 2
3
0 a 1
1 b 2
2 a 2
```

---

## 🧠 Représentation interne

Les transitions sont stockées sous forme de dictionnaire Python :

```python
{
    (etat, symbole): [liste des états suivants]
}
```

---

## 🚀 Objectif pédagogique

Ce projet permet de :

* comprendre en profondeur le fonctionnement des automates finis
* implémenter des algorithmes classiques (déterminisation, minimisation…)
* manipuler des structures de données complexes
* appliquer des concepts de théorie des langages en Python

---

## 🔮 Extensions possibles

* Interface graphique
* Visualisation des automates (graphes)
* Intégration dans des pipelines de traitement de données
* Optimisation des performances

---

## 👨‍💻 Auteur

Projet réalisé dans un cadre académique (école d’ingénieur).


## 👨‍💻 Auteur

- Tiffany VONGCHANH
- Karl junior FEKOUA
- Anissa MOHAMED
- Mariette RAGAZZI
- Thoma PENITOT

Projet réalisé dans un cadre académique (école d’ingénieur).
