# Yboost — Télémétrie RER A

Interface de prédiction d'affluence pour les gares du RER A (Île-de-France),
propulsée par un modèle **MLPRegressor** entraîné sur les données de validation.

---

## Fonctionnalités

-  **Courbe horaire 24H** — affluence estimée tranche par tranche
-  **Heatmap d'intensité** — visualisation rapide de la charge journalière
-  **KPIs temps réel** — pic, total journalier, indice de concentration
-  **Top 8 tranches critiques** — classement avec barres de progression
-  **Prise en compte météo** — température, pluie, vent
-  **Types de jours** — Semaine / Samedi / Dimanche & Jours fériés
-  **54 gares** du RER A couvertes

---

## Architecture du Projet

L'environnement est isolé et standardisé pour intégrer les fichiers de modèle fournis par Aurel :

```text
Yboost-B2/

├── Dockerfile            # Recette de construction de l'image de production Linux
├── requirements.txt      # Dépendances Python strictes alignées sur l'environnement IA
├── app.py                # Orchestrateur de l'application (point d'entrée Streamlit)
├── assets/               # Ressources statiques et graphiques
│   └── RER_1.png         # Logo RER A
├── models/               # Fichiers de sérialisation d'Intelligence Artificielle
│   ├── meilleur_modele_rera.pkl  # Modèle prédictif MLPRegressor 
│   └── scaler_rera.pkl           # StandardScaler pour la normalisation
├── src/                  # Code source applicatif
│   ├── utils/            # Fonctions utilitaires et scripts d'aide
│   ├── config.py         # Constantes, dictionnaires et configurations globales
│   ├── model.py          # Logique de chargement des fichiers pkl et prédictions
│   └── ui.py             # Structure des vues et mise en page principale
```

---

## Spécifications Techniques & DevOps

Pour éviter "l'enfer des dépendances" et garantir une compatibilité totale entre architectures matérielles (Mac ARM / Windows x86), l'environnement a été rigoureusement aligné sur l'environnement de génération d'Aurel (Google Colab) :
* **Base Image :** `Python 3.12-slim` (requis pour décoder le BitGenerator `MT19937` de NumPy créé sous Python 3.12).
* **Axe IA Synchrone :** Les versions de `scikit-learn==1.6.1` et `numpy==2.0.2` sont verrouillées pour éviter le crash au chargement avec `joblib`.

---

## Installation & Lancement via Docker (Serveur Local)

Assurez-vous que **Docker Desktop** est démarré sur votre machine avant de lancer les commandes.

### 1. Cloner et se placer sur la bonne branche
```bash
git clone <url-du-depot>
git checkout environnement
```

### 2. Construire l'image Docker
Cette commande prépare la bulle isolée et installe toutes les bibliothèques sans utiliser de cache pour forcer l'application des bonnes versions :
```bash
docker build --no-cache -t yboost-serveur .
```

### 3. Allumer le serveur avec rechargement à chaud (Volume)
Pour permettre à **Thibaud** de développer l'interface visuelle en direct sans devoir reconstruire le conteneur à chaque modification, on lie le dossier local au conteneur.

#### Sur macOS (Terminal / Zsh) :
```bash
docker run -p 8501:8501 -v $(pwd):/app yboost-serveur
```

#### Sur Windows (PowerShell) :
```powershell
docker run -p 8501:8501 -v ${PWD}:/app yboost-serveur
```

#### Sur Windows (Invite de commandes classique - CMD) :
```cmd
docker run -p 8501:8501 -v %cd%:/app yboost-serveur
```

L'application est instantanément accessible sur **[http://localhost:8501](http://localhost:8501)**.

---
