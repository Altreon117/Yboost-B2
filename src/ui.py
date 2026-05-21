"""
ui.py
─────
Toutes les fonctions de rendu de l'interface.

Chaque section de la page est une fonction indépendante,
appelée dans app.py dans l'ordre d'affichage.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import base64
import os

from config import COLORS, GARES, GARE_DEFAULT_INDEX, JOUR_OPTIONS, JOUR_CODES
from config import METEO_OPTIONS, METEO_ICONS, TRANCHES_LABELS, APP_VERSION, PROJECT_NAME
from config import PERIODES_COLORS


# ═══════════════════════════════════════════════════════════════
# UTILITAIRE IMAGE
# ═══════════════════════════════════════════════════════════════

def _img_b64(relative_path: str) -> str:
    """Charge une image et retourne son contenu en base64 (data URI)."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(root, relative_path)
    try:
        with open(full_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        ext = os.path.splitext(full_path)[1].lstrip(".")
        mime = "image/png" if ext == "png" else f"image/{ext}"
        return f"data:{mime};base64,{data}"
    except FileNotFoundError:
        return ""


# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# CSS — Design System complet (AVEC MEDIA QUERIES RESPONSIVES)
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

def inject_css():
    """Injecte le design system CSS global (polices, tokens, composants)."""
    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800'
        '&family=JetBrains+Mono:wght@300;400;500&display=swap" rel="stylesheet">',
        unsafe_allow_html=True,
    )
    st.markdown("""<style>
/* ── TOKENS ── */
:root {
    --bg-void:       #080B10;
    --bg-deep:       #0C1018;
    --bg-panel:      #111620;
    --bg-card:       #161D2B;
    --bg-hover:      #1C2535;
    --border-subtle: rgba(255,255,255,0.06);
    --border-mid:    rgba(255,255,255,0.10);
    --border-accent: rgba(0,220,200,0.30);
    --cyan:          #00DCC8;
    --cyan-dim:      rgba(0,220,200,0.12);
    --cyan-glow:     rgba(0,220,200,0.25);
    --amber:         #F5A623;
    --red:           #FF4D6A;
    --green:         #00E5A0;
    --green-dim:     rgba(0,229,160,0.10);
    --text-primary:  #E8EDF5;
    --text-secondary:#A8B8CC;
    --text-muted:    #6B7E96;
    --font-display:  'Syne', sans-serif;
    --font-mono:     'JetBrains Mono', monospace;
    --radius-md:     8px;
    --radius-lg:     12px;
}

/* ── BASE ── */
html, body, [class*="css"], .stApp {
    background-color: var(--bg-void) !important;
    font-family: var(--font-display) !important;
    color: var(--text-primary) !important;
}
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-void); }
::-webkit-scrollbar-thumb { background: var(--text-muted); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--cyan); }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: var(--bg-deep) !important;
    border-right: 1px solid var(--border-subtle) !important;
    padding-top: 0 !important;
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }
section[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.18em !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
    margin-top: 1.5rem !important;
    margin-bottom: 0.4rem !important;
}

/* ── INPUTS ── */
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-mid) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-display) !important;
    font-size: 0.85rem !important;
}
.stSelectbox > div > div:hover { border-color: var(--cyan) !important; }
.stSelectbox > div > div:focus-within {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 2px var(--cyan-glow) !important;
}
.stSelectbox label, .stSlider label {
    font-family: var(--font-mono) !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.12em !important;
    color: var(--text-secondary) !important;
    text-transform: uppercase !important;
}
div[data-testid="stSlider"] > div > div > div > div { background: var(--cyan) !important; }
div[data-testid="stSlider"] > div > div > div { background: var(--border-mid) !important; }
hr { border-color: var(--border-subtle) !important; margin: 1rem 0 !important; }

/* ── LAYOUT ── */
.main .block-container { padding: 0 !important; max-width: 100% !important; }
.main-wrapper { padding: 1.5rem 2rem; }

/* ── KPI GRID ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1px;
    background: var(--border-subtle);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    overflow: hidden;
    margin-bottom: 1.5rem;
}
.kpi-cell {
    background: var(--bg-card);
    padding: 1.4rem 1.8rem;
    position: relative;
    overflow: hidden;
    transition: background 0.2s;
}
.kpi-cell:hover { background: var(--bg-hover); }
.kpi-cell::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.kpi-cell.cyan::before  { background: var(--cyan);  box-shadow: 0 0 12px var(--cyan); }
.kpi-cell.amber::before { background: var(--amber); box-shadow: 0 0 12px var(--amber); }
.kpi-cell.green::before { background: var(--green); box-shadow: 0 0 12px var(--green); }
.kpi-label {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 6px;
}
.kpi-dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s infinite;
}
.cyan .kpi-dot  { background: var(--cyan);  box-shadow: 0 0 6px var(--cyan); }
.amber .kpi-dot { background: var(--amber); box-shadow: 0 0 6px var(--amber); }
.green .kpi-dot { background: var(--green); box-shadow: 0 0 6px var(--green); }
.kpi-value {
    font-family: var(--font-mono);
    font-size: 2.4rem;
    font-weight: 500;
    line-height: 1;
    letter-spacing: -0.02em;
}
.cyan  .kpi-value { color: var(--cyan); }
.amber .kpi-value { color: var(--amber); }
.green .kpi-value { color: var(--green); }
.kpi-sub { font-family: var(--font-mono); font-size: 0.65rem; color: var(--text-muted); margin-top: 0.4rem; }

/* ── CHART CONTAINER ── */
.chart-container {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 1.5rem 1.5rem 0.5rem 1.5rem;
}
.chart-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.2rem;
}
.chart-title  { font-family: var(--font-display); font-size: 0.85rem; font-weight: 600; color: var(--text-primary); }
.chart-sub    { font-family: var(--font-mono); font-size: 0.62rem; color: var(--text-muted); margin-top: 2px; letter-spacing: 0.08em; }
.chart-badge  { font-family: var(--font-mono); font-size: 0.6rem; letter-spacing: 0.12em; padding: 3px 8px; border-radius: 3px; text-transform: uppercase; }
.badge-live   { background: var(--green-dim); color: var(--green); border: 1px solid rgba(0,229,160,0.2); }

/* ── HEADER ── */
.app-header {
    background: var(--bg-deep);
    border-bottom: 1px solid var(--border-subtle);
    padding: 1.2rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    overflow: hidden;
}
.app-header::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity: 0.4;
}
.header-left { display: flex; align-items: center; gap: 14px; }
.header-icon {
    width: 38px; height: 38px;
    background: var(--cyan-dim);
    border: 1px solid var(--border-accent);
    border-radius: var(--radius-md);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
}
.header-title { font-family: var(--font-display); font-size: 1.05rem; font-weight: 700; color: var(--text-primary); }
.header-sub   { font-family: var(--font-mono); font-size: 0.6rem; color: var(--text-muted); letter-spacing: 0.15em; text-transform: uppercase; margin-top: 1px; }
.header-right { display: flex; align-items: center; gap: 1.5rem; }
.header-stat  { text-align: right; }
.header-stat-val { font-family: var(--font-mono); font-size: 0.72rem; color: var(--cyan); letter-spacing: 0.06em; }
.header-stat-lbl { font-family: var(--font-mono); font-size: 0.55rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.12em; }
.status-indicator { display: flex; align-items: center; gap: 6px; background: var(--green-dim); border: 1px solid rgba(0,229,160,0.2); border-radius: 20px; padding: 4px 10px; }
.status-dot   { width: 6px; height: 6px; background: var(--green); border-radius: 50%; box-shadow: 0 0 8px var(--green); animation: pulse 1.8s infinite; }
.status-text  { font-family: var(--font-mono); font-size: 0.58rem; color: var(--green); text-transform: uppercase; letter-spacing: 0.12em; }

/* ── SIDEBAR BRAND ── */
.sidebar-brand { background: var(--bg-panel); border-bottom: 1px solid var(--border-subtle); padding: 1.2rem 1rem; margin-bottom: 0.5rem; }
.sidebar-brand-title { font-family: var(--font-display); font-size: 0.78rem; font-weight: 700; color: var(--text-primary); }
.sidebar-brand-sub   { font-family: var(--font-mono); font-size: 0.58rem; color: var(--text-muted); letter-spacing: 0.12em; text-transform: uppercase; margin-top: 2px; }

/* ── HEATMAP ── */
.heatmap-wrapper { width: 100%; overflow-x: auto; padding-bottom: 10px; }
.heatmap-grid { display: grid; grid-template-columns: repeat(24, 1fr); gap: 3px; margin-bottom: 0.4rem; min-width: 600px; }
.heatmap-labels { display: grid; grid-template-columns: repeat(24, 1fr); gap: 3px; margin-top: 4px; min-width: 600px; }
.heatmap-cell { height: 28px; border-radius: 3px; cursor: default; transition: transform 0.1s; }
.heatmap-cell:hover { transform: scaleY(1.3); }

/* ── ANIMATIONS ── */
@keyframes pulse   { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
@keyframes fadeIn  { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
.animate-in { animation: fadeIn 0.4s ease forwards; }

/* ── RESPONSIVE (MOBILES & TABLETTES) ── */
@media (max-width: 1024px) {
    .kpi-grid { grid-template-columns: 1fr; gap: 8px; border: none; background: transparent; }
    .kpi-cell { border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); }
    .app-header { flex-direction: column; align-items: flex-start; gap: 1rem; padding: 1rem; padding-top: 3.5rem; }
    .header-right { width: 100%; justify-content: space-between; flex-wrap: wrap; }
    .header-stat { text-align: left; }
    .main-wrapper { padding: 1rem; }
    .footer-container { flex-direction: column !important; text-align: center; gap: 10px; }
}

/* ── STREAMLIT CLEANUP ── */
#MainMenu, footer { visibility: hidden !important; }
header { background-color: transparent !important; }
.stDeployButton { display: none !important; }
.stPlotlyChart  { padding: 0 !important; }
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

def render_sidebar() -> dict:
    """
    Affiche la sidebar et retourne les paramètres saisis par l'utilisateur.

    Retourne
    --------
    dict avec les clés :
      gare, cat_jour, jour_texte, meteo, temp_moy, pluie_mm, vent_ms
    """
    with st.sidebar:
        _logo = _img_b64("assets/RER_A.png")
        _logo_html = (
            f'<img src="{_logo}" style="width:24px;height:24px;object-fit:contain;border-radius:4px;">' 
            if _logo else '<span style="font-size:0.9rem;"></span>'
        )
        st.markdown(f"""
        <div class="sidebar-brand">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                <div style="width:32px;height:32px;background:var(--cyan-dim);border:1px solid var(--border-accent);
                            border-radius:6px;display:flex;align-items:center;justify-content:center;">
                    {_logo_html}
                </div>
                <div>
                    <div class="sidebar-brand-title">RER A {PROJECT_NAME}</div>
                    <div class="sidebar-brand-sub"> {APP_VERSION}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='padding:0 0.2rem;'>", unsafe_allow_html=True)

        st.markdown("### Gare")
        gare = st.selectbox("", GARES, index=GARE_DEFAULT_INDEX, label_visibility="collapsed")

        st.markdown("### Type de jour")
        jour_texte = st.selectbox("", JOUR_OPTIONS, label_visibility="collapsed")
        cat_jour   = JOUR_CODES[jour_texte]

        st.markdown("---")
        st.markdown("### Météo")
        meteo    = st.selectbox("", METEO_OPTIONS, label_visibility="collapsed")
        temp_moy = st.slider("Température (°C)", -5.0, 40.0, 15.0)
        pluie_mm = st.slider("Précipitations (mm)", 0.0, 30.0, 0.0)
        vent_ms  = st.slider("Rafales de vent (m/s)", 0.0, 30.0, 5.0)

        st.markdown("---")
        
        st.markdown(f"""
        <div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:8px;padding:10px 12px;">
            <div style="font-family:var(--font-mono);font-size:0.58rem;color:var(--text-muted);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:6px;">Conditions actives</div>
            <div style="font-family:var(--font-display);font-size:0.8rem;color:var(--text-primary);">{METEO_ICONS.get(meteo,"")} {meteo}</div>
            <div style="font-family:var(--font-mono);font-size:0.65rem;color:var(--cyan);margin-top:4px;">{temp_moy:.0f}°C · {pluie_mm:.0f}mm · {vent_ms:.0f}m/s</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    return {
        "gare": gare, "cat_jour": cat_jour, "jour_texte": jour_texte,
        "meteo": meteo, "temp_moy": temp_moy, "pluie_mm": pluie_mm, "vent_ms": vent_ms,
    }


# ═══════════════════════════════════════════════════════════════
# HEADER PRINCIPAL
# ═══════════════════════════════════════════════════════════════

def render_header(gare: str, jour_texte: str):
    """Affiche le header fixe de l'application."""
    _logo = _img_b64("assets/RER_A.png")
    _header_logo_html = (
        f'<img src="{_logo}" style="width:26px;height:26px;object-fit:contain;">' 
        if _logo else '<span style="font-size:1.1rem;"></span>'
    )
    st.markdown(f"""
    <div class="app-header animate-in">
        <div class="header-left">
            <div class="header-icon" style="padding:5px;">
                {_header_logo_html}
            </div>
            <div>
                <div class="header-title">Prédiction de l'affluence sur la ligne RER A</div>
                <div class="header-sub">selon les heures, la météo, le jour {PROJECT_NAME} · MLPRegressor</div>
            </div>
        </div>
        <div class="header-right">
            <div class="header-stat">
                <div class="header-stat-val">{gare}</div>
                <div class="header-stat-lbl">Gare sélectionnée</div>
            </div>
            <div class="header-stat">
                <div class="header-stat-val">{jour_texte}</div>
                <div class="header-stat-lbl">Type de journée</div>
            </div>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <div class="status-text">IA Active</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

def render_kpis(kpis: dict):
    """Affiche les 3 cartes KPI principales."""
    st.markdown(f"""
    <div class="kpi-grid animate-in" style="animation-delay:0.1s;">
        <div class="kpi-cell cyan">
            <div class="kpi-label"><span class="kpi-dot"></span>Pic de validations</div>
            <div class="kpi-value">{kpis["pic_val"]:,}</div>
            <div class="kpi-sub">Heure critique · {kpis["pic_heure"]}</div>
        </div>
        <div class="kpi-cell amber">
            <div class="kpi-label"><span class="kpi-dot"></span>Total journalier estimé</div>
            <div class="kpi-value">{kpis["total_jour"]:,}</div>
            <div class="kpi-sub">Moy. horaire · {kpis["moy_horaire"]:,} pass.</div>
        </div>
        <div class="kpi-cell green">
            <div class="kpi-label"><span class="kpi-dot"></span>Indice de concentration</div>
            <div class="kpi-value">{kpis["charge_ratio"]}%</div>
            <div class="kpi-sub">{kpis["heures_pic"]} tranches au-dessus du 75e pct.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# GRAPHIQUE PRINCIPAL — Courbe horaire
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

def render_chart_main(vals: list[int], moy_horaire: int):
    """Affiche la courbe d'affluence sur 24h."""
    st.markdown("""
    <div class="chart-container animate-in" style="animation-delay:0.2s;">
        <div class="chart-header">
            <div>
                <div class="chart-title">Courbe d'affluence horaire estimée</div>
                <div class="chart-sub">Validations prédites sur 24H · Modèle MLPRegressor</div>
            </div>
            <div class="chart-badge badge-live">● Live Prediction</div>
        </div>
    """, unsafe_allow_html=True)

    max_v = max(vals)
    fig   = go.Figure()


    fig.add_trace(go.Scatter(
        x=TRANCHES_LABELS, y=vals,
        fill="tozeroy", fillcolor="rgba(0,220,200,0.05)",
        line=dict(color="rgba(0,0,0,0)", width=0),
        hoverinfo="skip", showlegend=False,
    ))
    # Courbe principale
    fig.add_trace(go.Scatter(
        x=TRANCHES_LABELS, y=vals,
        mode="lines+markers",
        line=dict(color="#00DCC8", width=2, shape="spline", smoothing=0.8),
        marker=dict(
            size=[10 if v == max_v else 4 for v in vals],
            color=["#F5A623" if v == max_v else "#00DCC8" for v in vals],
            line=dict(width=0),
        ),
        hovertemplate="<b>%{x}</b><br>%{y:,} passagers<extra></extra>",
        showlegend=False,
    ))
    
    fig.add_hline(
        y=moy_horaire, line_dash="dot", line_color="rgba(245,166,35,0.35)",
        annotation_text=f"Moy. {moy_horaire:,}",
        annotation_font=dict(color="#F5A623", size=10, family="JetBrains Mono"),
        annotation_position="bottom right",
    )
    fig.update_layout(
        height=320, template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10), hovermode="x unified",
        hoverlabel=dict(bgcolor="#161D2B", bordercolor="#00DCC8", font=dict(family="JetBrains Mono", size=11, color="#E8EDF5")),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.06)", tickfont=dict(family="JetBrains Mono", size=10, color="#3D4E63"), dtick=2),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.06)", tickfont=dict(family="JetBrains Mono", size=10, color="#3D4E63"), zeroline=False),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# HEATMAP HORAIRE
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

def render_heatmap(vals: list[int]):
    """Affiche la heatmap d'intensité sur 24 cases."""
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-container animate-in" style="animation-delay:0.3s;padding-bottom:1.2rem;">
        <div class="chart-header" style="margin-bottom:0.8rem;">
            <div>
                <div class="chart-title">Heatmap d'intensité horaire</div>
                <div class="chart-sub">Distribution de charge sur la journée</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    max_heat = max(vals) if max(vals) > 0 else 1

    cells = ""
    for h, v in zip(TRANCHES_LABELS, vals):
        r = v / max_heat
        if   r < 0.2: color = f"rgba(0,220,200,{0.08 + r*0.5:.2f})"
        elif r < 0.5: color = f"rgba(0,220,200,{0.2  + r*0.6:.2f})"
        elif r < 0.8: color = f"rgba(245,166,35,{0.4 + r*0.4:.2f})"
        else:         color = f"rgba(255,77,106,{0.6  + r*0.4:.2f})"
        cells += f'<div class="heatmap-cell" style="background:{color};" title="{h} · {v:,} pass."></div>'

    labels = "".join(
        f'<div style="font-family:var(--font-mono);font-size:0.48rem;color:var(--text-muted);text-align:center;">{h}</div>'
        for h in TRANCHES_LABELS
    )

    st.markdown(f"""
    <div class="heatmap-wrapper">
        <div class="heatmap-grid">{cells}</div>
        <div class="heatmap-labels">{labels}</div>
    </div>
    <div style="display:flex;align-items:center;gap:16px;margin-top:12px;flex-wrap:wrap;">
        <div style="font-family:var(--font-mono);font-size:0.58rem;color:var(--text-muted);letter-spacing:0.1em;">INTENSITÉ :</div>
        <div style="display:flex;align-items:center;gap:5px;font-family:var(--font-mono);font-size:0.58rem;color:#00DCC8;">
            <div style="width:10px;height:10px;background:rgba(0,220,200,0.3);border-radius:2px;"></div>Faible
        </div>
        <div style="display:flex;align-items:center;gap:5px;font-family:var(--font-mono);font-size:0.58rem;color:#F5A623;">
            <div style="width:10px;height:10px;background:rgba(245,166,35,0.7);border-radius:2px;"></div>Modérée
        </div>
        <div style="display:flex;align-items:center;gap:5px;font-family:var(--font-mono);font-size:0.58rem;color:#FF4D6A;">
            <div style="width:10px;height:10px;background:rgba(255,77,106,0.9);border-radius:2px;"></div>Critique
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# GRAPHIQUE BARRES — Distribution par période
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

def render_chart_periodes(periodes: dict):
    """Affiche le graphique en barres des 4 périodes de la journée."""
    st.markdown("""
    <div class="chart-container">
        <div class="chart-header">
            <div>
                <div class="chart-title">Distribution par période</div>
                <div class="chart-sub">Nuit · Matin · Après-midi · Soir</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    fill_colors  = [c[0] for c in PERIODES_COLORS]
    line_colors  = [c[1] for c in PERIODES_COLORS]

    fig = go.Figure(go.Bar(
        x=list(periodes.keys()),
        y=list(periodes.values()),
        marker=dict(color=fill_colors, line=dict(color=line_colors, width=1.5)),
        hovertemplate="<b>%{x}</b><br>%{y:,} passagers<extra></extra>",
        text=[f"{v:,}" for v in periodes.values()],
        textposition="outside",
        textfont=dict(family="JetBrains Mono", size=10, color="#7A8BA0"),
    ))
    fig.update_layout(
        height=260, template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=5, r=5, t=20, b=5), showlegend=False, bargap=0.35,
        hoverlabel=dict(bgcolor="#161D2B", bordercolor="#00DCC8", font=dict(family="JetBrains Mono", size=11)),
        xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(family="JetBrains Mono", size=10, color="#3D4E63"), linecolor="rgba(0,0,0,0)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.03)", tickfont=dict(family="JetBrains Mono", size=10, color="#3D4E63"), zeroline=False),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# TOP 8 TRANCHES CRITIQUES
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

def render_top8(df_pred: pd.DataFrame, max_val: int):
    """Affiche le classement des 8 tranches les plus chargées."""
    st.markdown("""
    <div class="chart-container">
        <div class="chart-header">
            <div>
                <div class="chart-title">Top 8 — Tranches critiques</div>
                <div class="chart-sub">Classement par affluence décroissante</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    top8 = df_pred.nlargest(8, "Affluence").reset_index(drop=True)
    rows = ""
    for i, row in top8.iterrows():
        ratio = row["Affluence"] / max_val if max_val > 0 else 0
        bar_w = int(ratio * 100)
        color = "#FF4D6A" if ratio > 0.85 else ("#F5A623" if ratio > 0.60 else "#00DCC8")
        rows += f"""
        <div style="display:flex;align-items:center;gap:10px;padding:7px 0;border-bottom:1px solid var(--border-subtle);">
            <div style="font-family:var(--font-mono);font-size:0.58rem;color:var(--text-muted);width:14px;text-align:right;">{i+1}</div>
            <div style="flex:1;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="font-family:var(--font-mono);font-size:0.68rem;color:var(--text-primary);">{row["Tranche_Horaire"]}</span>
                    <span style="font-family:var(--font-mono);font-size:0.68rem;color:{color};font-weight:500;">{row["Affluence"]:,}</span>
                </div>
                <div style="height:3px;background:var(--border-subtle);border-radius:2px;overflow:hidden;">
                    <div style="height:100%;width:{bar_w}%;background:{color};border-radius:2px;"></div>
                </div>
            </div>
        </div>"""

    st.markdown(rows + "</div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

def render_footer(nb_features: int, nb_gares: int):
    """Affiche le pied de page avec les métadonnées du modèle."""
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="footer-container" style="display:flex;justify-content:space-between;align-items:center;padding:0.8rem 0;border-top:1px solid var(--border-subtle);">
        <div style="font-family:var(--font-mono);font-size:0.58rem;color:var(--text-muted);">
            RER A {PROJECT_NAME} 
        </div>
        <div style="font-family:var(--font-mono);font-size:0.58rem;color:var(--text-muted);">
            {nb_features} features · {nb_gares} gares · 24 tranches horaires
        </div>
    </div>
    """, unsafe_allow_html=True)