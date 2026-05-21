"""
model.py
────────
Chargement du modèle IA et calcul des prédictions horaires.

Séparé de app.py pour pouvoir tester la logique métier
indépendamment de l'interface Streamlit.
"""

import pandas as pd
import numpy as np
import joblib
import streamlit as st

from config import MODEL_PATH, SCALER_PATH, TRANCHES



@st.cache_resource(show_spinner="Chargement du modèle IA…")
def load_model():
    """
    Charge le scaler et le modèle MLPRegressor depuis le dossier models/.
    Retourne (scaler, modele, colonnes) ou lève une exception Streamlit si échec.
    """
    try:
        scaler  = joblib.load(SCALER_PATH)
        modele  = joblib.load(MODEL_PATH)
        colonnes = scaler.feature_names_in_
        return scaler, modele, colonnes
    except Exception as e:
        st.error(f" Impossible de charger les fichiers IA : {e}")
        st.stop()




def predict_day(
    scaler,
    modele,
    colonnes: np.ndarray,
    gare: str,
    cat_jour: str,
    meteo: str,
    temp_moy: float,
    pluie_mm: float,
    vent_ms: float,
) -> list[int]:
    """
    Calcule les prédictions d'affluence pour les 24 tranches horaires.

    Paramètres
    ----------
    scaler, modele, colonnes : objets retournés par load_model()
    gare        : nom de la gare (ex: "CHATELET-LES HALLES")
    cat_jour    : code jour du modèle ("JOHV" / "SAHV" / "DIJFP")
    meteo       : libellé météo (ex: "Temps Calme")
    temp_moy    : température moyenne en °C
    pluie_mm    : précipitations en mm
    vent_ms     : rafales de vent en m/s

    Retourne
    --------
    Liste de 24 entiers (validations estimées par tranche, ≥ 0)
    """
    resultats = []

    for tranche in TRANCHES:
        df_input = pd.DataFrame(0, index=[0], columns=colonnes)

        _set(df_input, colonnes, "TEMP_MOYENNE_C",              temp_moy)
        _set(df_input, colonnes, "PLUIE_MM",                    pluie_mm)
        _set(df_input, colonnes, "VENT_RAFALE_MS",              vent_ms)

        _set(df_input, colonnes, f"LIBELLE_ARRET_{gare}",       1)
        _set(df_input, colonnes, f"CAT_JOUR_{cat_jour}",        1)
        _set(df_input, colonnes, f"METEO_GLOBALE_{meteo}",      1)
        _set(df_input, colonnes, f"TRNC_HORR_60_{tranche}",     1)

        pred = modele.predict(scaler.transform(df_input))[0]
        resultats.append(max(0, int(pred)))

    return resultats


def compute_kpis(predictions: list[int]) -> dict:
    """
    Calcule les indicateurs clés à partir des prédictions journalières.

    Retourne un dict avec :
      pic_val, pic_heure, total_jour, moy_horaire,
      charge_ratio, heures_pic, vals, periodes
    """
    from config import TRANCHES, PERIODES

    vals        = predictions
    pic_idx     = int(np.argmax(vals))
    pic_val     = vals[pic_idx]
    pic_heure   = TRANCHES[pic_idx]
    total_jour  = sum(vals)
    moy_horaire = int(np.mean(vals))
    charge_ratio = int((pic_val / max(total_jour, 1)) * 100)

    seuil_75    = np.percentile(vals, 75)
    heures_pic  = sum(1 for v in vals if v > seuil_75)

    periodes = {
        label: sum(vals[debut:fin])
        for label, (debut, fin) in PERIODES.items()
    }

    return {
        "pic_val":      pic_val,
        "pic_heure":    pic_heure,
        "total_jour":   total_jour,
        "moy_horaire":  moy_horaire,
        "charge_ratio": charge_ratio,
        "heures_pic":   heures_pic,
        "vals":         vals,
        "periodes":     periodes,
    }


def _set(df, colonnes, col_name: str, value):
    """Écrit une valeur dans df seulement si la colonne existe dans le modèle."""
    if col_name in colonnes:
        df[col_name] = value
