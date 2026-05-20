import streamlit as st
import joblib
import os

st.title("🚇 Prédiction d'affluence RER A")

# Chemins vers les fichiers d'Aurel
chemin_modele = "models/meilleur_modele_rera.pkl"
chemin_scaler = "models/scaler_rera.pkl"

# Fonction pour charger un fichier exporté avec joblib
def charger_fichier_ia(chemin):
    if os.path.exists(chemin):
        # joblib lit directement le fichier sans avoir besoin de faire un 'open()'
        return joblib.load(chemin)
    return None

# Chargement du Scaler et du Modèle
modele = charger_fichier_ia(chemin_modele)
scaler = charger_fichier_ia(chemin_scaler)

# Vérification pour l'interface
if modele and scaler:
    st.success("✅ Modèle d'IA et Scaler chargés avec succès via Joblib !")
    st.write("Le pipeline est prêt ! Thibaud peut maintenant ajouter les filtres (Météo, Heure, etc.) et coder la fonction de prédiction.")
else:
    st.error("❌ Fichiers introuvables. Vérifie qu'ils sont bien dans le dossier 'models/'.")