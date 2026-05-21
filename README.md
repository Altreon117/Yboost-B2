# 🚇 Yboost — Télémétrie RER A

Interface de prédiction d'affluence pour les gares du RER A (Île-de-France),
propulsée par un modèle **MLPRegressor** entraîné sur les données de validation.

---

## ✨ Fonctionnalités

- 📊 **Courbe horaire 24H** — affluence estimée tranche par tranche
- 🌡️ **Heatmap d'intensité** — visualisation rapide de la charge journalière
- 📈 **KPIs temps réel** — pic, total journalier, indice de concentration
- 🏆 **Top 8 tranches critiques** — classement avec barres de progression
- 🌦️ **Prise en compte météo** — température, pluie, vent
- 🗓️ **Types de jours** — Semaine / Samedi / Dimanche & Jours fériés
- 🚉 **54 gares** du RER A couvertes

---

## 🚀 Installation

```bash
# Cloner le projet
git clone <url-du-repo>
cd yboost_project

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Ajouter les modèles IA

Placer les fichiers `.pkl` (générés depuis le notebook Colab) dans `models/` :

```
models/
├── meilleur_modele_rera.pkl
└── scaler_rera.pkl
```

---

## ▶️ Lancement

```bash
streamlit run app.py
```

L'application est accessible sur `http://localhost:8501`

---

## 🧪 Tests

```bash
pytest tests/ -v
```

---

## 🏗️ Architecture

```
yboost_project/
├── app.py              → Orchestrateur (point d'entrée)
├── requirements.txt
├── src/
│   ├── config.py       → Constantes globales
│   ├── model.py        → Chargement IA + prédictions
│   ├── ui.py           → Composants visuels
│   ├── components/     → Composants réutilisables
│   └── utils/
│       └── patch_numpy.py  → Patch compatibilité NumPy
├── models/             → Fichiers .pkl (non versionnés)
├── assets/             → Ressources statiques
├── tests/              → Tests unitaires
└── docs/               → Documentation technique
```

Voir [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) pour le détail complet.

---

## ⚙️ Stack technique

| Composant     | Technologie              |
|---------------|--------------------------|
| Interface     | Streamlit                |
| Modèle IA     | scikit-learn MLPRegressor|
| Visualisation | Plotly                   |
| Data          | Pandas / NumPy           |
| Sérialisation | joblib                   |

---

## 📋 Compatibilité

Les fichiers `.pkl` ont été générés avec **scikit-learn 1.6.1** et **NumPy 2.x**
sous Google Colab. Un patch de compatibilité automatique est appliqué au démarrage
(`src/utils/patch_numpy.py`).
