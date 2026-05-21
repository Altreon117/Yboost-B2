"""
app.py
──────
Point d'entrée de l'application Streamlit — Projet Yboost.

Orchestrateur pur : aucune logique métier ni CSS ici.

Lancement :
    streamlit run app.py
"""

# ── 1. Patch NumPy AVANT tout autre import ────────────────────────────────────
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from utils.patch_numpy import apply as patch_numpy
patch_numpy()

# ── 2. Imports standard ───────────────────────────────────────────────────────
import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd

# ── 3. Modules du projet ──────────────────────────────────────────────────────
from config import APP_TITLE, TRANCHES
from model  import load_model, predict_day, compute_kpis
from ui     import (
    inject_css,
    render_sidebar,
    render_header,
    render_kpis,
    render_chart_main,
    render_heatmap,
    render_chart_periodes,
    render_top8,
    render_footer,
)

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION STREAMLIT
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM
# ─────────────────────────────────────────────────────────────────────────────
inject_css()

# ─────────────────────────────────────────────────────────────────────────────
# CHARGEMENT DU MODÈLE
# ─────────────────────────────────────────────────────────────────────────────
scaler, modele, colonnes = load_model()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — récupération des paramètres utilisateur
# ─────────────────────────────────────────────────────────────────────────────
params = render_sidebar()

# ─────────────────────────────────────────────────────────────────────────────
# CALCUL DES PRÉDICTIONS
# ─────────────────────────────────────────────────────────────────────────────
predictions = predict_day(
    scaler   = scaler,
    modele   = modele,
    colonnes = colonnes,
    gare     = params["gare"],
    cat_jour = params["cat_jour"],
    meteo    = params["meteo"],
    temp_moy = params["temp_moy"],
    pluie_mm = params["pluie_mm"],
    vent_ms  = params["vent_ms"],
)

kpis    = compute_kpis(predictions)
df_pred = pd.DataFrame({"Tranche_Horaire": TRANCHES, "Affluence": predictions})

# ─────────────────────────────────────────────────────────────────────────────
# RENDU DE L'INTERFACE
# ─────────────────────────────────────────────────────────────────────────────
render_header(gare=params["gare"], jour_texte=params["jour_texte"])

st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

render_kpis(kpis)
render_chart_main(vals=kpis["vals"], moy_horaire=kpis["moy_horaire"])
render_heatmap(vals=kpis["vals"])

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
col_left, col_right = st.columns([3, 2], gap="medium")
with col_left:
    render_chart_periodes(kpis["periodes"])
with col_right:
    render_top8(df_pred=df_pred, max_val=kpis["pic_val"])

render_footer(nb_features=len(colonnes), nb_gares=len(params))

st.markdown("</div>", unsafe_allow_html=True)
