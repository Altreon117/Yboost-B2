"""
config.py
─────────
Constantes globales du projet Yboost.
Centralise toutes les valeurs fixes : chemins, listes métier, couleurs.
"""

# ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
#Chemins
# ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
MODEL_PATH  = "models/meilleur_modele_rera.pkl"
SCALER_PATH = "models/scaler_rera.pkl"

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# Identité de l'app 
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
APP_TITLE    = "RER A · Télémétrie Opérationnelle"
APP_VERSION  = "v2.0"
PROJECT_NAME = "Yboost"

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# Palette de couleurs (reprise dans CSS et dans les figures Plotly)
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

COLORS = {
    "cyan":   "#00DCC8",
    "amber":  "#F5A623",
    "red":    "#FF4D6A",
    "green":  "#00E5A0",
    "purple": "#7B68EE",
    "bg_card":"#161D2B",
    "bg_deep":"#0C1018",
    "text_muted": "#D6D6D6",
    "text_secondary": "#7A8BA0",
}

GARES = [
    "ACHERES-GRAND-CORMIER", "ACHERES-VILLE", "AUBER", "BOISSY-SAINT-LEGER",
    "BRY-SUR-MARNE", "BUSSY-SAINT-GEORGES", "CERGY LE HAUT", "CERGY-PREFECTURE",
    "CERGY-SAINT-CHRISTOPHE", "CHAMPIGNY", "CHARLES DE GAULLE ETOILE",
    "CHATELET-LES HALLES", "CHATOU-CROISSY", "CHESSY - MARNE-LA-VALLEE",
    "CONFLANS-FIN-D'OISE", "FONTENAY-SOUS-BOIS", "GARE DE LYON",
    "HOUILLES-CARRIERES-SUR-SEINE", "JOINVILLE-LE-PONT", "LA DEFENSE-GRANDE ARCHE",
    "LA VARENNE-CHENNEVIERES", "LE PARC-DE-SAINT-MAUR", "LE VESINET-CENTRE",
    "LE VESINET-LE PECQ", "LOGNES", "MAISONS-LAFFITTE", "NANTERRE-PREFECTURE",
    "NANTERRE-UNIVERSITE", "NANTERRE-VILLE", "NATION", "NEUILLY-PLAISANCE",
    "NEUVILLE UNIVER", "NEUVILLE UNIVERSITE", "NOGENT-S-MARNE", "NOGENT-SUR-MARNE",
    "NOISIEL", "NOISY-CHAMPS", "NOISY-LE-GRAND", "NOISY-LE-GRAND-MONT D'EST",
    "POISSY", "RUEIL-MALMAIS.", "RUEIL-MALMAISON", "SAINT-GERMAIN-EN-LAYE",
    "SAINT-MAUR-CRETEIL", "SARTROUVILLE", "ST-GERMAIN", "ST-MAUR-CRET.",
    "SUCY-BONNEUIL", "TORCY", "VAL D'EUROPE", "VAL D.FONTENAY", "VAL-D'EUROPE",
    "VAL-DE-FONTENAY", "VINCENNES",
]

GARE_DEFAULT_INDEX = 11

TRANCHES = [
    "0H-1H",  "1H-2H",  "2H-3H",  "3H-4H",  "4H-5H",  "5H-6H",
    "6H-7H",  "7H-8H",  "8H-9H",  "9H-10H", "10H-11H","11H-12H",
    "12H-13H","13H-14H","14H-15H","15H-16H","16H-17H","17H-18H",
    "18H-19H","19H-20H","20H-21H","21H-22H","22H-23H","23H-0H",
]

TRANCHES_LABELS = [t.split("H-")[0] + "h" for t in TRANCHES]

JOUR_OPTIONS = ["Semaine (Lun–Ven)", "Samedi", "Dimanche / Jour Férié"]
JOUR_CODES   = {"Semaine (Lun–Ven)": "JOHV", "Samedi": "SAHV", "Dimanche / Jour Férié": "DIJFP"}

METEO_OPTIONS = [
    "Temps Calme", "Pluie Légère", "Pluvieux",
    "Venteux", "Gel/Froid Extrême", "Conditions Extrêmes",
]
METEO_ICONS = {
    "Temps Calme": "☀️", "Pluie Légère": "🌦️", "Pluvieux": "🌧️",
    "Venteux": "💨", "Gel/Froid Extrême": "❄️", "Conditions Extrêmes": "⛈️",
}

PERIODES = {
    "Nuit (0h–5h)":         (0,  5),
    "Matin (5h–12h)":       (5,  12),
    "Après-midi (12h–18h)": (12, 18),
    "Soir (18h–24h)":       (18, 24),
}
PERIODES_COLORS = [
    ("rgba(28,37,53,0.6)",  "#1C2535"),
    ("rgba(0,220,200,0.7)", "#00DCC8"),
    ("rgba(245,166,35,0.7)","#F5A623"),
    ("rgba(123,104,238,0.7)","#7B68EE"),
]
