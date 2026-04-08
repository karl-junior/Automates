# Automata Simulator — Projet d’Automates Finis

## 📚 Contexte
Ce projet a été réalisé dans le cadre d’un cours de mathematiques sur les automates finis.

L’objectif est de concevoir un programme capable de :

- lire un automate depuis un fichier
- analyser ses propriétés
- manipuler ses transitions
- reconnaître des mots

Au-delà de l’aspect académique, ce projet illustre comment un automate peut être utilisé dans des situations concrètes, notamment pour valider des données séquentielles. 

## ⚙️ Fonctinnalités

Le programme permet de :

- Lire un automate depuis un fichier .txt
- Vérifier si un automate est : déterministe, complet
- Manipuler les transitions sous forme structurée
- Tester la reconnaissance de mots
- Utiliser l’automate comme validateur de séquences

## ⚡ Démonstration rapide ( Automate45.txt )

📄 Données d’entrée (data.txt)
- ADTS
- ATS
- DATS
- ADTS

## 🧠 Règle métier

Une séquence valide doit respecter l’ordre :

A → D → T → S

## ✅ Résultat
VALID:
- ADTS
- ADTS

INVALID:
- ATS
- DATS

## 💡 Interprétation
ADTS → séquence correcte
ATS → étape manquante
DATS → ordre incorrect

L’automate agit ici comme un filtre de qualité des données.

## 🧩 Structure du projet

L’automate est représenté avec :

des états (entiers)
un alphabet
des transitions sous forme de dictionnaire :
{
    (etat, symbole): [liste des états suivants]
}
Cas d’usage : Qualité des données

Dans des systèmes réels, les données suivent souvent des séquences logiques (logs, événements, parcours utilisateur…).

Un automate permet de :

- détecter des incohérences
- valider la structure des données
- éviter des erreurs dans les traitements en aval (analyse, machine learning…)

Exemple : vérifier qu’un processus métier respecte un ordre précis.

## 🚀 Perspectives

Ce projet peut être étendu avec :

- déterminisation d’automates
- minimisation
- complétion
- intégration dans un pipeline de traitement de données

## 👨‍💻 Auteur

- Tiffany VONGCHANH
- Karl junior FEKOUA
- Anissa MOHAMED
- Mariette RAGAZZI
- Thoma PENITOT

Projet réalisé dans un cadre académique (école d’ingénieur).
