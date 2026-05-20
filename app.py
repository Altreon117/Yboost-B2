import streamlit as st
import pickle
import os

st.title("Prédiction d'affluence RER A")

# Chemin vers le modèle à l'intérieur du conteneur Docker
chemin_modele = "models/modele_trafic.pkl"

# Pipeline de chargement sécurisé
if os.path.exists(chemin_modele):
    with open(chemin_modele, 'rb') as file:
        modele = pickle.load(file)
    st.success("Modèle d'IA chargé avec succès depuis le conteneur !")
    # Ici, l'étudiant 4 fera ses st.selectbox pour la météo, l'heure, etc.
else:
    st.warning("⏳ En attente du modèle de l'étudiant 2. Le pipeline est prêt.")