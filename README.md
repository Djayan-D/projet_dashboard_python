---
title: "Tableau de bord des ventes - Supermarché"
author: "DAËRON Djayan"
date: "2024-2025"
format: html
---

# Tableau de bord des ventes - Supermarché

Ce projet est une application interactive développée avec **Dash**, **Plotly**, et **Pandas** pour visualiser les données de ventes d'un supermarché. L'application permet d'explorer les ventes par ville, genre, et période.

## 🚀 Fonctionnalités principales

- **Filtres interactifs** :
  - Sélection des villes
  - Sélection du genre des clients
- **Indicateurs clés** :
  - Montant total des achats
  - Nombre total d'achats (factures)
- **Visualisations dynamiques** :
  - Histogramme des montants totaux des achats
  - Graphique en barres du nombre de factures
  - Courbe d'évolution des ventes par mois

## 📂 Structure du projet

```python
.
├── supermarket_sales.csv  # Fichier de données
├── app.py                 # Code source de l'application
├── requirements.txt       # Packages nécessaires
├── README.md              # Documentation du projet
```

## 🛠️ Installation et exécution

### 1️⃣ Prérequis
Assurez-vous d'avoir **Python 3.x** et **pip** installés sur votre machine.

### 2️⃣ Installation des dépendances
Exécutez la commande suivante pour installer les bibliothèques nécessaires :

```python
pip install dash pandas plotly
```

### 3️⃣ Exécution de l'application
Lancez l'application avec la commande :

```python
python app.py
```

L'application est accessible sur `https://projet-dashboard-python.onrender.com/` (très lent au chargement car version gratuite).

## 📊 Détails des graphiques

- **Histogramme des montants des achats** : Montre la répartition des ventes en fonction des filtres sélectionnés.
- **Graphique en barres du nombre de factures** : Affiche le nombre total d'achats par ville et/ou genre.
- **Courbe d'évolution des ventes** : Analyse la tendance des ventes au fil du temps.

## 📌 Remarque
- Le projet utilise une palette de couleurs personnalisée pour améliorer la lisibilité.
- La sélection de "Tout sélectionner" dans les filtres ajuste automatiquement les visualisations.

## 👨‍💻 Auteur
Projet développé par **DAËRON Djayan** dans le cadre du **M1 ECAP 2024-2025** sous la supervision de **SANE Abdoul Razac**.

## 📜 Licence
Ce projet est sous licence MIT. Vous êtes libre de l'utiliser et de le modifier selon vos besoins.

---

🎯 Amusez-vous bien avec ce tableau de bord interactif ! 🚀
