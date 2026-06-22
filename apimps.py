# -*- coding: utf-8 -*-
"""
MOTOR ANALÍTICO Y PREDICTIVO MPS — Dashboard Streamlit
Pedro Andrés Aranda Muñoz

Ejecución:  streamlit run app_mps.py
Requisitos: pip install streamlit plotly pandas
"""

import json, os, glob, math, statistics
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MPS · Motor Analítico y Predictivo",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# ESTILOS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Fondo oscuro con tono ligeramente azulado */
.stApp { background-color: #0D1117; color: #E6EDF3; }
section[data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #21262D; }
section[data-testid="stSidebar"] * { color: #C9D1D9 !important; }

/* Encabezado principal */
.mps-header {
    background: linear-gradient(135deg, #0D1117 0%, #131A24 50%, #0A1628 100%);
    border: 1px solid #21262D;
    border-radius: 12px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.mps-header::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #1F6FEB, #58A6FF, #1F6FEB);
}
.mps-title { font-size: 26px; font-weight: 700; color: #E6EDF3; margin: 0 0 4px; letter-spacing: -0.5px; }
.mps-subtitle { font-size: 13px; color: #8B949E; margin: 0; font-weight: 400; }
.mps-badge {
    display: inline-block; background: rgba(31,111,235,0.13); border: 1px solid rgba(31,111,235,0.33);
    color: #58A6FF; font-size: 11px; padding: 3px 10px; border-radius: 20px;
    font-family: 'JetBrains Mono', monospace; margin-top: 10px;
}

/* KPI Cards */
.kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }
.kpi { background: #161B22; border: 1px solid #21262D; border-radius: 10px; padding: 16px 20px; position: relative; }
.kpi::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; border-radius: 10px 10px 0 0; }
.kpi.blue::before  { background: #1F6FEB; }
.kpi.green::before { background: #2EA043; }
.kpi.red::before   { background: #DA3633; }
.kpi.amber::before { background: #9E6A03; }
.kpi-val { font-size: 28px; font-weight: 700; margin: 0; font-family: 'JetBrains Mono', monospace; }
.kpi-lbl { font-size: 11px; color: #8B949E; margin: 4px 0 0; text-transform: uppercase; letter-spacing: .06em; }
.kpi.blue .kpi-val  { color: #58A6FF; }
.kpi.green .kpi-val { color: #3FB950; }
.kpi.red .kpi-val   { color: #F85149; }
.kpi.amber .kpi-val { color: #D29922; }

/* Secciones */
.sec-header {
    font-size: 13px; font-weight: 600; color: #8B949E;
    text-transform: uppercase; letter-spacing: .08em;
    border-bottom: 1px solid #21262D; padding-bottom: 8px; margin: 24px 0 16px;
}

/* Chips de grupo */
.chip { display: inline-block; font-size: 11px; padding: 2px 9px; border-radius: 20px; font-weight: 500; }
.chip-a { background: #1A3A2A; color: #3FB950; }
.chip-b { background: #2D1F06; color: #D29922; }
.chip-c { background: #2D0A09; color: #F85149; }

/* Nota metodológica */
.nota {
    background: #161B22; border: 1px solid #21262D; border-left: 3px solid #58A6FF;
    border-radius: 0 8px 8px 0; padding: 14px 18px; font-size: 13px;
    color: #8B949E; line-height: 1.7; margin: 12px 0;
}
.nota strong { color: #E6EDF3; }

/* Alerta */
.alerta {
    background: #2D0A09; border: 1px solid rgba(218,54,51,0.33); border-radius: 8px;
    padding: 12px 16px; margin: 6px 0; font-size: 13px;
}

/* Perfil de país */
.perfil-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.perfil-item { background: #161B22; border: 1px solid #21262D; border-radius: 8px; padding: 14px; }
.perfil-label { font-size: 11px; color: #8B949E; text-transform: uppercase; letter-spacing: .06em; margin: 0 0 4px; }
.perfil-val { font-size: 18px; font-weight: 600; color: #E6EDF3; margin: 0; font-family: 'JetBrains Mono', monospace; }

/* Scrollable table */
.stDataFrame { background: #161B22 !important; }
div[data-testid="stDataFrame"] > div { background: #161B22; border: 1px solid #21262D; border-radius: 8px; }

/* Plotly dark override */
.js-plotly-plot { border-radius: 8px; }

/* Tab styling */
button[data-baseweb="tab"] { color: #8B949E !important; font-size: 13px !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: #E6EDF3 !important; border-bottom-color: #58A6FF !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────────────────────────────────────
NOMBRES = {
    "AFG":"Afganistán","AGO":"Angola","ALB":"Albania","ARE":"Emiratos Árabes",
    "ARG":"Argentina","ARM":"Armenia","AUS":"Australia","AUT":"Austria",
    "AZE":"Azerbaiyán","BDI":"Burundi","BEL":"Bélgica","BEN":"Benín",
    "BFA":"Burkina Faso","BGD":"Bangladés","BGR":"Bulgaria","BHR":"Baréin",
    "BIH":"Bosnia-Herz.","BLR":"Bielorrusia","BLZ":"Belice","BOL":"Bolivia",
    "BRA":"Brasil","BRB":"Barbados","BRN":"Brunéi","BTN":"Bután",
    "BWA":"Botsuana","CAF":"R. Centroafricana","CAN":"Canadá","CHE":"Suiza",
    "CHL":"Chile","CHN":"China","CMR":"Camerún","COD":"R.D. Congo",
    "COG":"Congo","COL":"Colombia","COM":"Comoras","CRI":"Costa Rica",
    "CUB":"Cuba","CYP":"Chipre","CZE":"Rep. Checa","DEU":"Alemania",
    "DJI":"Yibuti","DNK":"Dinamarca","DOM":"R. Dominicana","DZA":"Argelia",
    "ECU":"Ecuador","EGY":"Egipto","ERI":"Eritrea","ESP":"España",
    "EST":"Estonia","ETH":"Etiopía","FIN":"Finlandia","FJI":"Fiyi",
    "FRA":"Francia","GAB":"Gabón","GBR":"Reino Unido","GEO":"Georgia",
    "GHA":"Ghana","GIN":"Guinea","GMB":"Gambia","GNB":"Guinea-Bisáu",
    "GRC":"Grecia","GTM":"Guatemala","GUY":"Guyana","HKG":"Hong Kong",
    "HND":"Honduras","HRV":"Croacia","HTI":"Haití","HUN":"Hungría",
    "IDN":"Indonesia","IND":"India","IRL":"Irlanda","IRN":"Irán",
    "IRQ":"Irak","ISL":"Islandia","ISR":"Israel","ITA":"Italia",
    "JAM":"Jamaica","JOR":"Jordania","JPN":"Japón","KAZ":"Kazajistán",
    "KEN":"Kenia","KGZ":"Kirguistán","KHM":"Camboya","KOR":"Corea del Sur",
    "KWT":"Kuwait","LAO":"Laos","LBN":"Líbano","LBR":"Liberia",
    "LBY":"Libia","LSO":"Lesoto","LTU":"Lituania","LUX":"Luxemburgo",
    "LVA":"Letonia","MAR":"Marruecos","MDA":"Moldavia","MDG":"Madagascar",
    "MDV":"Maldivas","MEX":"México","MKD":"Macedonia N.","MLI":"Mali",
    "MMR":"Myanmar","MNE":"Montenegro","MNG":"Mongolia","MOZ":"Mozambique",
    "MRT":"Mauritania","MUS":"Mauricio","MWI":"Malaui","MYS":"Malasia",
    "NAM":"Namibia","NER":"Níger","NGA":"Nigeria","NIC":"Nicaragua",
    "NLD":"Países Bajos","NOR":"Noruega","NPL":"Nepal","NZL":"Nueva Zelanda",
    "OMN":"Omán","PAK":"Pakistán","PAN":"Panamá","PER":"Perú",
    "PHL":"Filipinas","PNG":"Papúa N. Guinea","POL":"Polonia","PRY":"Paraguay",
    "PSE":"Palestina","QAT":"Qatar","ROU":"Rumanía","RUS":"Rusia",
    "RWA":"Ruanda","SAU":"Arabia Saudí","SDN":"Sudán","SEN":"Senegal",
    "SGP":"Singapur","SLE":"Sierra Leona","SLV":"El Salvador","SOM":"Somalia",
    "SRB":"Serbia","SSD":"Sudán del Sur","SUR":"Surinam","SVK":"Eslovaquia",
    "SVN":"Eslovenia","SWE":"Suecia","SWZ":"Suazilandia","SYR":"Siria",
    "TCD":"Chad","TGO":"Togo","THA":"Tailandia","TJK":"Tayikistán",
    "TLS":"Timor Oriental","TTO":"Trinidad y Tobago","TUN":"Túnez",
    "TUR":"Turquía","TWN":"Taiwán","TZA":"Tanzania","UGA":"Uganda",
    "UKR":"Ucrania","URY":"Uruguay","USA":"Estados Unidos","UZB":"Uzbekistán",
    "VEN":"Venezuela","VNM":"Vietnam","WSM":"Samoa","YEM":"Yemen",
    "ZAF":"Sudáfrica","ZMB":"Zambia","ZWE":"Zimbabue",
}

REGIONES = {
    "Europa Occidental": ["DEU","FRA","GBR","ITA","ESP","BEL","NLD","AUT","CHE","LUX","IRL","DNK","SWE","NOR","FIN","ISL","GRC","CYP"],
    "Europa del Este":   ["POL","CZE","SVK","HUN","ROU","BGR","HRV","SVN","EST","LVA","LTU","BIH","SRB","MNE","MKD","ALB","MDA","UKR","BLR","RUS"],
    "América del Norte": ["USA","CAN","MEX"],
    "América Latina":    ["BRA","ARG","COL","CHL","PER","VEN","ECU","BOL","PRY","URY","CRI","GTM","HND","SLV","NIC","PAN","DOM","CUB","JAM","HTI","BRB","TTO","GUY","SUR"],
    "Asia Oriental":     ["CHN","JPN","KOR","TWN","HKG","MNG"],
    "Asia Sudoriental":  ["IDN","THA","PHL","VNM","MYS","SGP","MMR","KHM","LAO","TLS"],
    "Asia del Sur":      ["IND","PAK","BGD","NPL","LKA","BTN","MDV"],
    "Asia Central":      ["KAZ","UZB","TJK","KGZ","AZE","ARM","GEO"],
    "Oriente Medio":     ["SAU","ARE","QAT","KWT","BHR","OMN","IRN","IRQ","SYR","JOR","LBN","ISR","YEM","PSE"],
    "África del Norte":  ["EGY","DZA","MAR","TUN","LBY","SDN","MRT"],
    "África Subsahariana":["NGA","ETH","COD","TZA","KEN","UGA","AGO","MOZ","GHA","CMR","NER","SEN","ZMB","ZWE","MWI","ZAF","NAM","BWA","GAB","COG","RWA","BDI","SLE","LBR","GMB","GIN","GNB","SOM","DJI","CAF","TCD","SSD","BEN","TGO"],
    "Oceanía":           ["AUS","NZL","FJI","PNG","WSM"],
}

ALERTAS_CONOCIDAS = {
    "ARG": "Quiebre estructural 2024: las reformas Milei rompen la inercia histórica. El modelo proyecta deterioro por extrapolación lineal, pero el shock fiscal real detiene la autofagia.",
    "UKR": "La serie 2022-2023 refleja contracción de G_cons por destrucción institucional de guerra. La proyección de mejora es estadística, no real.",
    "LBY": "Cleptocracia total. Los valores extremos son el resultado correcto: el modelo muestra un estado que consume 50× su economía real.",
    "NOR": "Estado del bienestar con renta petrolera. La PN negativa refleja que el estado gestiona la renta del recurso, no que haya drenaje parasitario sobre economía privada pura.",
    "LUX": "Economía de servicios financieros. El G_trans incluye redistribución supranacional UE que infla artificialmente el denominador.",
    "CHN": "La PN extrema refleja el tamaño absoluto del aparato estatal chino y la C_H elevada por el índice SOE (empresas públicas). La inversión pública masiva penaliza adicionalmente.",
}

PLOTLY_DARK = dict(
    template="plotly_dark",
    paper_bgcolor="#0D1117",
    plot_bgcolor="#0D1117",
    font=dict(family="Inter", color="#8B949E", size=12),
)

# ─────────────────────────────────────────────────────────────────────────────
# CARGA DE DATOS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def cargar_todo():
    def _find(patron):
        rutas = glob.glob(f"./*{patron}*.json") + glob.glob(f"./output_mps/*{patron}*.json")
        if not rutas:
            return None
        return max(rutas, key=os.path.getmtime)

    def _load(path):
        if not path: return {}
        with open(path, encoding='utf-8') as f:
            return json.load(f)

    matriz    = _load(_find("matriz_completa"))
    alertas   = _load(_find("alertas"))
    rankings  = _load(_find("rankings"))
    interdep  = _load(_find("interdependencia"))

    if not matriz:
        st.error("❌ No se encuentra la matriz MPS. Coloca los JSON en la carpeta ./output_mps/")
        st.stop()

    return matriz, alertas if isinstance(alertas, list) else [], rankings, interdep

MATRIZ, ALERTAS, RANKINGS, INTERDEP = cargar_todo()
PAISES = sorted(MATRIZ.keys())
AÑOS   = sorted({a for p in MATRIZ for a in MATRIZ[p]}, key=int)

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def nombre(iso): return NOMBRES.get(iso, iso)
def region(iso):
    for r, ps in REGIONES.items():
        if iso in ps: return r
    return "Otras"

def df_año(año, grupo_filter=None, excluir_extremos=True):
    """DataFrame de todos los países para un año dado."""
    rows = []
    for p in PAISES:
        d = MATRIZ[p].get(str(año), {})
        if not d: continue
        pn = d.get('PN')
        g  = d.get('grupo')
        if grupo_filter and g != grupo_filter: continue
        if excluir_extremos and pn is not None and pn < -1000: continue
        rows.append({
            'ISO':       p,
            'País':      nombre(p),
            'Región':    region(p),
            'Grupo':     g or '?',
            'Proyectado': d.get('proyectado', False),
            'PN':        pn,
            'TPL':       d.get('TPL'),
            'ERI':       d.get('ERI'),
            'C_H':       d.get('C_H'),
            'G_cons%':   d.get('G_cons_pct'),
            'G_trans%':  d.get('G_trans_pct'),
            'Inv%':      d.get('inversion_pct'),
            'C_eficiencia': d.get('C_eficiencia'),
            'IIJ':       d.get('IIJ'),
            'WJP':       d.get('WJP'),
            'PS':        d.get('PS'),
            'PIB_nom':   d.get('PIB_nominal'),
        })
    return pd.DataFrame(rows)

def serie_pais(iso):
    """Serie temporal completa de un país."""
    rows = []
    for año in AÑOS:
        d = MATRIZ[iso].get(año, {})
        if not d: continue
        rows.append({
            'Año': int(año), 'Proyectado': d.get('proyectado', False),
            'PN': d.get('PN'), 'TPL': d.get('TPL'),
            'ERI': d.get('ERI'), 'C_H': d.get('C_H'),
            'G_cons%': d.get('G_cons_pct'), 'G_trans%': d.get('G_trans_pct'),
            'Inv%': d.get('inversion_pct'), 'C_eficiencia': d.get('C_eficiencia'),
            'PS': d.get('PS'),
        })
    return pd.DataFrame(rows)

def fmt(v, dec=1, suffix=""):
    if v is None or (isinstance(v, float) and math.isnan(v)): return "N/D"
    return f"{v:+.{dec}f}{suffix}" if suffix else f"{v:.{dec}f}"

def color_pn(v):
    if v is None: return "#8B949E"
    if v > 50:  return "#3FB950"
    if v > 0:   return "#8B949E"
    if v > -100: return "#D29922"
    return "#F85149"

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚖️ MPS · Control")
    st.markdown("---")

    año_global = st.slider("Año de análisis global", 2008, 2026, 2023)
    st.markdown("---")
    pais_sel   = st.selectbox(
        "País para análisis individual",
        PAISES,
        format_func=nombre,
        index=PAISES.index("ESP") if "ESP" in PAISES else 0
    )
    st.markdown("---")
    region_sel = st.selectbox("Filtrar por región", ["Todas"] + sorted(REGIONES.keys()))
    st.markdown("---")
    mostrar_extremos = st.checkbox("Mostrar países con PN < −1000", value=False)
    st.markdown("---")
    st.markdown("""
    **Leyenda de grupos:**  
    🟢 **A** — Economías comparables  
    🟡 **B** — Drenaje severo  
    🔴 **C** — Colapso institucional
    """)

# ─────────────────────────────────────────────────────────────────────────────
# HEADER PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="mps-header">
  <div class="mps-title">⚖️ Motor Analítico y Predictivo MPS</div>
  <div class="mps-subtitle">Modelo de Prosperidad Sostenible · Pedro Andrés Aranda Muñoz</div>
  <div class="mps-badge">163 países · 2008 → 2026 · {len(AÑOS)} años de serie</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab_global, tab_pais_tab, tab_ranking, tab_grupos, tab_metodo = st.tabs([
    "🌍 Visión Global",
    "🗺️ Análisis País",
    "🏆 Rankings y Alertas",
    "🧬 Grupos y Clústeres",
    "📖 Metodología",
])

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — VISIÓN GLOBAL
# ═════════════════════════════════════════════════════════════════════════════
with tab_global:
    df = df_año(año_global, excluir_extremos=not mostrar_extremos)
    if region_sel != "Todas":
        df = df[df['Región'] == region_sel]

    # KPIs
    ga  = df[df['Grupo']=='A']
    n_alertas = len([a for a in ALERTAS if str(a.get('año','')) == str(año_global)])
    med_pn = ga['PN'].median() if not ga.empty else 0
    pct_pos = (ga['PN'] > 0).mean() * 100 if not ga.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="kpi blue"><p class="kpi-val">{len(df)}</p><p class="kpi-lbl">Países con datos {año_global}</p></div>', unsafe_allow_html=True)
    with c2:
        color = "green" if med_pn > 10 else "amber" if med_pn > 0 else "red"
        st.markdown(f'<div class="kpi {color}"><p class="kpi-val">{med_pn:+.1f}</p><p class="kpi-lbl">PN mediana grupo A</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kpi green"><p class="kpi-val">{pct_pos:.0f}%</p><p class="kpi-lbl">Países con PN positiva</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="kpi red"><p class="kpi-val">{n_alertas}</p><p class="kpi-lbl">Alertas estructurales {año_global}</p></div>', unsafe_allow_html=True)

    st.markdown("")

    # Gráfico scatter principal: TPL vs PN
    df_plot = df.dropna(subset=['PN','TPL','ERI'])
    df_plot = df_plot[df_plot['TPL'] < 2000]  # excluir outliers visuales

    fig_scatter = px.scatter(
        df_plot, x='TPL', y='PN',
        color='PN', size='ERI',
        size_max=20,
        hover_name='País',
        hover_data={'ISO': False, 'Grupo': True, 'G_cons%': ':.1f', 'C_H': ':.1f', 'ERI': ':.3f'},
        color_continuous_scale='RdYlGn',
        range_color=[-200, 100],
        labels={'TPL': 'Carga Parasitaria Total (TPL)', 'PN': 'Prosperidad Neta (PN)'},
        title=f"Mapa Estructural Global {año_global} — TPL vs Prosperidad Neta",
        template="plotly_dark",
    )
    fig_scatter.add_hline(y=0, line_dash="dot", line_color="rgba(88,166,255,0.27)",
                          annotation_text="Límite autofagia", annotation_font_color="#58A6FF")
    fig_scatter.update_traces(marker=dict(opacity=0.8, line=dict(width=0.5, color='#21262D')))
    fig_scatter.update_layout(
        height=520, paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
        coloraxis_showscale=True,
        xaxis=dict(gridcolor="#21262D", zeroline=False),
        yaxis=dict(gridcolor="#21262D", zeroline=False),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Tabla global
    st.markdown('<div class="sec-header">Matriz macro-institucional completa</div>', unsafe_allow_html=True)
    cols_tabla = ['País', 'Región', 'Grupo', 'PN', 'TPL', 'ERI', 'C_H', 'G_cons%', 'G_trans%', 'C_eficiencia']
    df_tabla = df[cols_tabla].copy().sort_values('PN', ascending=False)

    def color_grupo(val):
        if val == 'A': return 'color: #3FB950'
        if val == 'B': return 'color: #D29922'
        return 'color: #F85149'

    st.dataframe(
        df_tabla.style
        .map(color_grupo, subset=['Grupo'])
        .background_gradient(subset=['PN'], cmap='RdYlGn', vmin=-200, vmax=100)
        .background_gradient(subset=['C_H'], cmap='Reds', vmin=0, vmax=200)
        .format({'PN': '{:.1f}', 'TPL': '{:.1f}', 'ERI': '{:.3f}',
                 'C_H': '{:.1f}', 'G_cons%': '{:.1f}', 'G_trans%': '{:.1f}',
                 'C_eficiencia': '{:.3f}'}, na_rep="N/D"),
        use_container_width=True, height=420
    )

    # Tendencia histórica global
    st.markdown('<div class="sec-header">Tendencia de la Prosperidad Neta global (mediana grupo A)</div>', unsafe_allow_html=True)
    trend_data = []
    for a in AÑOS:
        d = df_año(a, excluir_extremos=True)
        ga2 = d[d['Grupo']=='A']['PN'].dropna()
        if len(ga2) < 10: continue
        trend_data.append({
            'Año': int(a), 'Mediana PN': ga2.median(),
            '% Positivos': (ga2 > 0).mean() * 100,
            'Proyectado': int(a) > 2023
        })
    df_trend = pd.DataFrame(trend_data)

    fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
    mask_hist = df_trend['Proyectado'] == False
    mask_proy = df_trend['Proyectado'] == True

    fig_trend.add_trace(go.Scatter(
        x=df_trend[mask_hist]['Año'], y=df_trend[mask_hist]['Mediana PN'],
        mode='lines+markers', name='Mediana PN (real)',
        line=dict(color='#58A6FF', width=2.5), marker=dict(size=6)
    ))
    fig_trend.add_trace(go.Scatter(
        x=df_trend[mask_proy]['Año'], y=df_trend[mask_proy]['Mediana PN'],
        mode='lines+markers', name='Mediana PN (proyección)',
        line=dict(color='#58A6FF', width=2, dash='dash'), marker=dict(size=6, symbol='circle-open')
    ))
    fig_trend.add_trace(go.Bar(
        x=df_trend['Año'], y=df_trend['% Positivos'],
        name='% Países PN positiva', marker_color='rgba(46,160,67,0.2)',
        opacity=0.5
    ), secondary_y=True)
    fig_trend.add_vrect(x0=2023.5, x1=2026.5,
                        fillcolor="rgba(88,166,255,0.03)", layer="below", line_width=0,
                        annotation_text="Proyección", annotation_position="top left",
                        annotation_font_color="rgba(88,166,255,0.53)")
    # Marcar COVID
    fig_trend.add_vline(x=2020, line_dash="dot", line_color="rgba(248,81,73,0.27)",
                        annotation_text="COVID-19", annotation_font_color="#F85149")
    fig_trend.update_layout(
        height=380, paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
        font=dict(color="#8B949E"), legend=dict(orientation="h", y=1.05),
        xaxis=dict(gridcolor="#21262D"), yaxis=dict(gridcolor="#21262D"),
        yaxis2=dict(range=[0, 100], tickformat='.0f', ticksuffix='%'),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — ANÁLISIS PAÍS A PAÍS
# ═════════════════════════════════════════════════════════════════════════════
with tab_pais_tab:
    iso = pais_sel
    nom = nombre(iso)
    df_p = serie_pais(iso)

    if df_p.empty:
        st.warning(f"No hay datos para {nom}")
    else:
        # Header de país
        d23 = MATRIZ[iso].get('2023', {})
        d26 = MATRIZ[iso].get('2026', {})
        gr  = d23.get('grupo', '?')
        chip_cls = {'A': 'chip-a', 'B': 'chip-b', 'C': 'chip-c'}.get(gr, '')

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:18px">
          <div style="font-size:22px;font-weight:700;color:#E6EDF3">{nom}</div>
          <div class="chip {chip_cls}">Grupo {gr}</div>
          <div style="color:#8B949E;font-size:13px">{region(iso)}</div>
        </div>
        """, unsafe_allow_html=True)

        # KPIs del país
        pn23 = d23.get('PN'); pn26 = d26.get('PN')
        delta_pn = (pn26 - pn23) if (pn23 and pn26) else None
        tpl23 = d23.get('TPL'); eri23 = d23.get('ERI'); ch23 = d23.get('C_H')

        c1, c2, c3, c4, c5 = st.columns(5)
        metrics = [
            (c1, "PN 2023", fmt(pn23), "blue"),
            (c2, "PN 2026 (proy.)", fmt(pn26), "green" if (pn26 or 0) > 0 else "red"),
            (c3, "Δ PN 2023→26", fmt(delta_pn), "green" if (delta_pn or 0) > 0 else "red"),
            (c4, "TPL 2023", fmt(tpl23), "amber"),
            (c5, "ERI 2023", fmt(eri23, 3), "blue"),
        ]
        for col, lbl, val, cls in metrics:
            with col:
                st.markdown(f'<div class="kpi {cls}"><p class="kpi-val">{val}</p><p class="kpi-lbl">{lbl}</p></div>', unsafe_allow_html=True)

        st.markdown("")

        # Alerta específica si existe
        if iso in ALERTAS_CONOCIDAS:
            st.markdown(f'<div class="nota">⚠️ <strong>Nota de auditoría cuantitativa:</strong> {ALERTAS_CONOCIDAS[iso]}</div>', unsafe_allow_html=True)

        # Gráfico principal de series
        fig_main = go.Figure()

        df_p['Proyectado'] = df_p['Proyectado'].fillna(False)
        df_hist = df_p[df_p['Proyectado'] == False]
        df_proy = df_p[df_p['Proyectado'] == True]

        # PN histórica
        fig_main.add_trace(go.Scatter(
            x=df_hist['Año'], y=df_hist['PN'],
            mode='lines+markers', name='Prosperidad Neta (real)',
            line=dict(color='#3FB950', width=2.5), marker=dict(size=5)
        ))
        # PN proyectada
        if not df_proy.empty:
            # Conectar con último real
            ult = df_hist.iloc[-1] if not df_hist.empty else None
            x_conn = ([ult['Año']] + list(df_proy['Año'])) if ult is not None else list(df_proy['Año'])
            y_conn = ([ult['PN']] + list(df_proy['PN'])) if ult is not None else list(df_proy['PN'])
            fig_main.add_trace(go.Scatter(
                x=x_conn, y=y_conn, mode='lines+markers',
                name='PN proyectada', line=dict(color='#3FB950', width=2, dash='dash'),
                marker=dict(size=6, symbol='circle-open')
            ))

        # TPL (eje secundario)
        fig_main.add_trace(go.Scatter(
            x=df_hist['Año'], y=df_hist['TPL'],
            mode='lines', name='TPL (real)',
            line=dict(color='#F85149', width=1.5),
            yaxis='y2'
        ))
        if not df_proy.empty:
            fig_main.add_trace(go.Scatter(
                x=list(df_proy['Año']), y=list(df_proy['TPL']),
                mode='lines+markers', name='TPL proyectada',
                line=dict(color='#F85149', width=1.5, dash='dash'),
                marker=dict(symbol='circle-open', size=5), yaxis='y2'
            ))

        fig_main.add_hline(y=0, line_dash="dot", line_color="rgba(88,166,255,0.2)")
        fig_main.add_vrect(x0=2023.5, x1=2026.5, fillcolor="rgba(88,166,255,0.02)", layer="below", line_width=0)

        fig_main.update_layout(
            title=f"Evolución estructural — {nom} (2008-2026)",
            height=420, paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
            font=dict(color="#8B949E"),
            xaxis=dict(gridcolor="#21262D"),
            yaxis=dict(title="Prosperidad Neta (%)", gridcolor="#21262D"),
            yaxis2=dict(title="TPL", overlaying='y', side='right',
                        showgrid=False, color="#F85149"),
            legend=dict(orientation="h", y=1.05),
            hovermode="x unified",
        )
        st.plotly_chart(fig_main, use_container_width=True)

        # Gráfico de componentes del gasto
        col_a, col_b = st.columns(2)

        with col_a:
            fig_comp = go.Figure()
            for var, col, name in [
                ('G_cons%', '#58A6FF', 'G. Consumo'),
                ('G_trans%', '#D29922', 'G. Transferencias'),
                ('Inv%', '#3FB950', 'Inversión'),
            ]:
                fig_comp.add_trace(go.Scatter(
                    x=df_p['Año'], y=df_p[var], mode='lines', name=name,
                    line=dict(color=col, width=2)
                ))
            fig_comp.update_layout(
                title="Composición del gasto público (%PIB)",
                height=320, paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
                font=dict(color="#8B949E"), xaxis=dict(gridcolor="#21262D"),
                yaxis=dict(gridcolor="#21262D"), legend=dict(orientation="h", y=1.1),
            )
            st.plotly_chart(fig_comp, use_container_width=True)

        with col_b:
            fig_inst = go.Figure()
            for var, col, name in [
                ('ERI', '#3FB950', 'ERI (efic. inversión)'),
                ('C_eficiencia', '#58A6FF', 'C_Eficiencia (WGI)'),
            ]:
                fig_inst.add_trace(go.Scatter(
                    x=df_p['Año'], y=df_p[var], mode='lines+markers', name=name,
                    line=dict(color=col, width=2), marker=dict(size=4)
                ))
            fig_inst.update_layout(
                title="Índices institucionales",
                height=320, paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
                font=dict(color="#8B949E"), xaxis=dict(gridcolor="#21262D"),
                yaxis=dict(gridcolor="#21262D"), legend=dict(orientation="h", y=1.1),
            )
            st.plotly_chart(fig_inst, use_container_width=True)

        # Tabla histórica completa
        st.markdown('<div class="sec-header">Serie histórica y proyecciones</div>', unsafe_allow_html=True)
        cols_hist = [c for c in ['Año','PN','TPL','ERI','C_H','G_cons%','G_trans%','Inv%','C_eficiencia','PS','Proyectado'] if c in df_p.columns]
        df_tabla_p = df_p[cols_hist].copy()
        try:
            styled_p = df_tabla_p.style \
                .background_gradient(subset=['PN'], cmap='RdYlGn', vmin=-200, vmax=100) \
                .format({'PN':'{:.2f}','TPL':'{:.2f}','ERI':'{:.3f}','C_H':'{:.2f}',
                         'G_cons%':'{:.2f}','G_trans%':'{:.2f}','Inv%':'{:.2f}',
                         'C_eficiencia':'{:.3f}','PS':'{:.2f}'}, na_rep="N/D")
            st.dataframe(styled_p, use_container_width=True, height=380)
        except Exception:
            st.dataframe(df_tabla_p, use_container_width=True, height=380)

        # Perfil del país
        st.markdown('<div class="sec-header">Perfil institucional 2023</div>', unsafe_allow_html=True)
        iij_v  = d23.get('IIJ', 0) or 0
        wjp_v  = d23.get('WJP', 0) or 0
        cef_v  = d23.get('C_eficiencia', 0) or 0
        inter26 = INTERDEP.get('2026', {}).get(iso, {})
        tipos_dep = ', '.join(inter26.get('tipos', ['N/D']))

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="perfil-item">
              <p class="perfil-label">Integridad institucional (IIJ)</p>
              <p class="perfil-val">{iij_v:.2f} / 10</p>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="perfil-item">
              <p class="perfil-label">Estado de derecho (WJP)</p>
              <p class="perfil-val">{wjp_v:.2f} / 10</p>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="perfil-item">
              <p class="perfil-label">Eficiencia gubernamental</p>
              <p class="perfil-val">{cef_v:.3f}</p>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="nota" style="margin-top:12px">
          <strong>Tipo de dependencia estructural (2026):</strong> {tipos_dep}<br>
          <strong>ERI 2023:</strong> {fmt(eri23, 3)} — {'Inversión altamente eficiente' if (eri23 or 0) > 2 else 'Inversión moderadamente eficiente' if (eri23 or 0) > 0.5 else 'Inversión mayoritariamente ineficiente'}<br>
          <strong>C_H 2023:</strong> {fmt(ch23, 1)} — {'Baja fricción institucional' if (ch23 or 0) < 20 else 'Fricción institucional moderada' if (ch23 or 0) < 60 else 'Alta carga institucional oculta'}
        </div>
        """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 — RANKINGS Y ALERTAS
# ═════════════════════════════════════════════════════════════════════════════
with tab_ranking:
    año_rank = st.selectbox("Año para el ranking", [2023,2024,2025,2026], index=3, key="yr")
    df_r = df_año(año_rank, excluir_extremos=True)
    df_r = df_r.dropna(subset=['PN','TPL'])

    col_top, col_bot = st.columns(2)

    with col_top:
        top20 = df_r.sort_values('PN', ascending=False).head(20)
        fig_top = go.Figure(go.Bar(
            x=top20['PN'], y=top20['País'], orientation='h',
            marker=dict(
                color=top20['PN'],
                colorscale=[[0,'#1A3A2A'],[1,'#3FB950']],
                line=dict(width=0)
            ),
            text=[f"{v:.1f}" for v in top20['PN']],
            textposition='outside', textfont=dict(color='#8B949E', size=11)
        ))
        fig_top.update_layout(
            title=f"Top 20 Prosperidad Neta — {año_rank}",
            height=580, paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
            font=dict(color="#8B949E"),
            xaxis=dict(gridcolor="#21262D"),
            yaxis=dict(autorange="reversed", gridcolor="#21262D"),
            margin=dict(l=120),
        )
        st.plotly_chart(fig_top, use_container_width=True)

    with col_bot:
        bot20 = df_r.sort_values('PN', ascending=True).head(20)
        fig_bot = go.Figure(go.Bar(
            x=bot20['PN'], y=bot20['País'], orientation='h',
            marker=dict(
                color=bot20['PN'],
                colorscale=[[0,'#F85149'],[1,'#2D0A09']],
                reversescale=True, line=dict(width=0)
            ),
            text=[f"{v:.1f}" for v in bot20['PN']],
            textposition='outside', textfont=dict(color='#8B949E', size=11)
        ))
        fig_bot.update_layout(
            title=f"Bottom 20 (autofagia) — {año_rank}",
            height=580, paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
            font=dict(color="#8B949E"),
            xaxis=dict(gridcolor="#21262D"),
            yaxis=dict(autorange="reversed", gridcolor="#21262D"),
            margin=dict(l=120),
        )
        st.plotly_chart(fig_bot, use_container_width=True)

    # Ranking TPL
    st.markdown('<div class="sec-header">Ranking de Carga Parasitaria Total (TPL) — menor es mejor</div>', unsafe_allow_html=True)
    df_tpl = df_r[df_r['TPL'] < 500].sort_values('TPL')
    fig_tpl = px.bar(
        df_tpl.head(30), x='País', y='TPL', color='TPL',
        color_continuous_scale='Reds',
        title=f"Países con menor TPL — {año_rank}",
    )
    fig_tpl.update_layout(height=380, paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
                          font=dict(color="#8B949E"), xaxis=dict(gridcolor="#21262D"),
                          yaxis=dict(gridcolor="#21262D"))
    st.plotly_chart(fig_tpl, use_container_width=True)

    # Alertas
    st.markdown('<div class="sec-header">🚨 Alertas de deterioro estructural proyectado</div>', unsafe_allow_html=True)
    alertas_proy = [a for a in ALERTAS if a.get('proyectado', False)]
    alertas_a    = [a for a in alertas_proy
                    if MATRIZ.get(a['pais'],{}).get(str(a['año']),{}).get('grupo') == 'A'
                    and a['delta'] < -10]
    alertas_a.sort(key=lambda x: x['delta'])

    if alertas_a:
        df_al = pd.DataFrame(alertas_a[:30])
        df_al['País'] = df_al['pais'].map(nombre)
        df_al = df_al[['País','pais','año','pn_ant','pn_act','delta','tipo']]
        df_al.columns = ['País','ISO','Año','PN anterior','PN proyectada','Δ','Tipo']

        fig_al = px.bar(
            df_al, x='Δ', y='País', orientation='h', color='Δ',
            color_continuous_scale='Reds_r',
            title="Países con mayor deterioro proyectado (grupo A)",
        )
        fig_al.update_layout(height=460, paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
                             font=dict(color="#8B949E"), yaxis=dict(autorange="reversed"),
                             margin=dict(l=120))
        st.plotly_chart(fig_al, use_container_width=True)

        try:
            st.dataframe(
                df_al.style
                .background_gradient(subset=['Δ'], cmap='Reds_r', vmin=-130, vmax=0)
                .format({'PN anterior':'{:.1f}','PN proyectada':'{:.1f}','Δ':'{:.1f}'}, na_rep="N/D"),
                use_container_width=True
            )
        except Exception:
            st.dataframe(df_al, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 4 — GRUPOS Y CLÚSTERES
# ═════════════════════════════════════════════════════════════════════════════
with tab_grupos:
    st.markdown('<div class="sec-header">Clasificación por grupo MPS y tipo de dependencia estructural</div>', unsafe_allow_html=True)

    año_g = st.selectbox("Año de referencia", [2023,2024,2025,2026], index=0, key="yg")
    df_g = df_año(año_g, excluir_extremos=True)

    # Distribución de grupos
    col_pie, col_dep = st.columns(2)
    with col_pie:
        grupo_counts = df_g['Grupo'].value_counts().reset_index()
        grupo_counts.columns = ['Grupo', 'N']
        fig_pie = px.pie(
            grupo_counts, values='N', names='Grupo',
            color='Grupo',
            color_discrete_map={'A': '#3FB950', 'B': '#D29922', 'C': '#F85149', '?': '#8B949E'},
            title=f"Distribución por grupo — {año_g}",
            hole=0.55,
        )
        fig_pie.update_layout(height=340, paper_bgcolor="#0D1117",
                              font=dict(color="#8B949E"), legend=dict(orientation="h"))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_dep:
        # Interdependencia tipos
        inter_año = INTERDEP.get(str(año_g), {})
        tipos_count = {}
        for p, d in inter_año.items():
            for t in d.get('tipos', []):
                tipos_count[t] = tipos_count.get(t, 0) + 1
        df_tipos = pd.DataFrame(list(tipos_count.items()), columns=['Tipo', 'N']).sort_values('N', ascending=False)
        fig_dep = px.bar(
            df_tipos, x='N', y='Tipo', orientation='h',
            color='N', color_continuous_scale='Blues',
            title=f"Tipos de dependencia estructural — {año_g}",
        )
        fig_dep.update_layout(height=340, paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
                              font=dict(color="#8B949E"), yaxis=dict(autorange="reversed"),
                              xaxis=dict(gridcolor="#21262D"))
        st.plotly_chart(fig_dep, use_container_width=True)

    # Grupos por región
    st.markdown('<div class="sec-header">PN por región geográfica</div>', unsafe_allow_html=True)
    df_g2 = df_g.dropna(subset=['PN'])
    df_g2 = df_g2[df_g2['PN'] > -500]

    fig_box = px.box(
        df_g2, x='Región', y='PN', color='Grupo',
        color_discrete_map={'A': '#3FB950', 'B': '#D29922', 'C': '#F85149'},
        points='outliers',
        title=f"Distribución PN por región — {año_g}",
    )
    fig_box.update_layout(
        height=480, paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
        font=dict(color="#8B949E"),
        xaxis=dict(tickangle=-35, gridcolor="#21262D"),
        yaxis=dict(gridcolor="#21262D"),
        legend=dict(orientation="h"),
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # Scatter ERI vs C_H coloreado por PN
    st.markdown('<div class="sec-header">Eficiencia de la inversión vs Fricción institucional oculta</div>', unsafe_allow_html=True)
    df_g3 = df_g.dropna(subset=['ERI','C_H','PN'])
    df_g3 = df_g3[(df_g3['C_H'] < 200) & (df_g3['ERI'] < 5)]

    fig_eri_ch = px.scatter(
        df_g3, x='C_H', y='ERI', color='PN',
        hover_name='País',
        color_continuous_scale='RdYlGn', range_color=[-150, 100],
        labels={'C_H': 'Carga Oculta (C_H)', 'ERI': 'Efectividad de Inversión (ERI)'},
        title="C_H vs ERI — Mayor arriba-izquierda = más eficiente con menos fricción",
    )
    fig_eri_ch.add_hline(y=1, line_dash="dot", line_color="rgba(88,166,255,0.2)",
                         annotation_text="ERI = 1 (neutral)", annotation_font_color="#58A6FF")
    fig_eri_ch.update_layout(
        height=460, paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
        font=dict(color="#8B949E"),
        xaxis=dict(gridcolor="#21262D"), yaxis=dict(gridcolor="#21262D"),
    )
    st.plotly_chart(fig_eri_ch, use_container_width=True)

    # Tabla de grupos
    st.markdown('<div class="sec-header">Países por grupo (detalle)</div>', unsafe_allow_html=True)
    grupo_sel = st.radio("Grupo", ["A", "B", "C"], horizontal=True)
    df_grp = df_año(año_g, excluir_extremos=False)
    df_grp = df_grp[df_grp['Grupo'] == grupo_sel].sort_values('PN', ascending=False)
    if not df_grp.empty:
        cols = ['País','Región','PN','TPL','ERI','C_H','G_cons%','G_trans%']
        try:
            st.dataframe(
                df_grp[cols].style
                .background_gradient(subset=['PN'], cmap='RdYlGn', vmin=-500, vmax=100)
                .format({'PN':'{:.1f}','TPL':'{:.1f}','ERI':'{:.3f}','C_H':'{:.1f}',
                         'G_cons%':'{:.1f}','G_trans%':'{:.1f}'}, na_rep="N/D"),
                use_container_width=True
            )
        except Exception:
            st.dataframe(df_grp[cols], use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 5 — METODOLOGÍA
# ═════════════════════════════════════════════════════════════════════════════
with tab_metodo:
    st.markdown('<div class="sec-header">Fundamentos teóricos del Modelo de Prosperidad Sostenible</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="nota">
    <strong>Premisa central:</strong> El PIB per cápita contabiliza el gasto público como actividad económica positiva,
    generando circularidad estadística — el estado aparece simultáneamente como drenador y como generador de riqueza.
    El MPS invierte esta lógica: el gasto del estado es siempre un coste sobre la economía privada productiva,
    medible y comparable entre países.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **🔴 Carga Oculta (C_H)**
        ```
        C_H = (carga_bruta / 10) ^ (1.85 − WJP/10)
        carga_bruta = Σ (10−indicador) × 10
        Indicadores: IIJ, WJP, Fraser REG, SOE, FISCAL
        ```
        Mide la fricción institucional invisible: corrupción, inseguridad jurídica,
        exceso regulatorio, empresas públicas ineficientes y presión fiscal opaca.
        El exponente dinámico amplifica geométricamente el daño cuando el estado
        de derecho es débil — un país corrupto sin justicia sufre más del doble.
        """)

        st.markdown("""
        **🟠 Carga Parasitaria Total (TPL)**
        ```
        TPL = G_cons^(2−WGI) + √G_trans + C_H
              × (1 − ERI_norm × 0.5)
        ```
        Suma el coste directo del aparato estatal (G_cons elevado al cuadrado
        ponderado por eficiencia), el peso amortiguado de las transferencias
        y la fricción institucional oculta. El factor ERI mitiga la carga
        proporcionalmente a cuánta inversión pública resulta realmente productiva.
        """)

        st.markdown("""
        **🟡 Efectividad Real de la Inversión (ERI)**
        ```
        ERI = Inversión_pública% / C_H
        ```
        Ratio entre lo que el estado invierte en infraestructura y su propio
        nivel de corrupción e ineficiencia. Si ERI > 1, la inversión supera la
        carga institucional — el estado usa bien al menos esa partida.
        """)

    with col2:
        st.markdown("""
        **🟢 Prosperidad Neta (PN)**
        ```
        PN = 100 − (TPL × 1.18)
        ```
        Stock de prosperidad privada que queda tras descontar el coste del estado.
        El coeficiente 1.18 captura el deadweight loss — por cada unidad extraída,
        la economía pierde un 18% adicional por distorsión de incentivos.
        Un PN positivo indica economía viable; negativo indica hipoteca generacional.
        """)

        st.markdown("""
        **🔵 Prosperidad Sostenible (PS)**
        ```
        PS = PN + S_E%
        S_E = ((Importaciones − Exportaciones) + ODA + Remesas) / PIB × 100
        ```
        Corrige la PN por el subsidio exterior neto. Países receptores netos
        (S_E positivo) tienen PN artificialmente sostenida por flujos externos.
        Países donantes netos (S_E negativo, como EEUU o Alemania) sostienen
        la prosperidad de otros con su propio esfuerzo productivo.
        """)

        st.markdown("""
        **📊 Clasificación de países**

        | Grupo | PN | Descripción |
        |-------|-----|-------------|
        | 🟢 A  | > −500 | Economías comparables — núcleo del análisis |
        | 🟡 B  | −5.000 a −500 | Drenaje severo — hipoteca generacional visible |
        | 🔴 C  | < −5.000 | Colapso institucional — estado como cleptocracia |
        """)

    st.markdown('<div class="sec-header">Notas metodológicas sobre las proyecciones 2024-2026</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="nota">
    <strong>Método de proyección:</strong> Las variables fiscales (G_cons, G_trans, inversión) se proyectan
    mediante regresión lineal sobre la serie 2008-2023, con intervalos de confianza al 80%.
    Las variables institucionales (IIJ, WJP, Fraser) se proyectan como media móvil de los últimos 3 años,
    dado que cambian lentamente. La inflación permanece como <em>null</em> hasta que se inyecten datos
    del FMI WEO — esto afecta solo a PSA y VNA, no a PN ni TPL.
    </div>
    <div class="nota" style="margin-top:8px">
    <strong>Países con saltos bruscos 2023→2024:</strong> Ucrania (+177 pts), Luxemburgo (+138 pts),
    Guinea (−124 pts). Estos saltos reflejan tendencias pronunciadas en los últimos 2-3 años de la serie
    histórica que la regresión lineal extrapola con fuerza. Se recomienda interpretarlos con cautela y
    contrastar con fuentes externas para 2024.
    </div>
    <div class="nota" style="margin-top:8px">
    <strong>Sobre PN negativas extremas:</strong> Valores como Libia (−1.300.000) o Timor Oriental (−150.000)
    no son errores numéricos — son la foto real de lo que el modelo predice para estados en colapso institucional.
    La fórmula G_cons^(2−WGI) con WGI muy negativo produce exponentes superiores a 2, lo que refleja
    matemáticamente que estados con gobierno destructivo neto amplifican el daño de forma no lineal.
    Es una consecuencia deliberada del diseño: el modelo no tiene techo porque el parasitismo estatal tampoco lo tiene.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-header">Fuentes de datos</div>', unsafe_allow_html=True)

    fuentes = [
        ("Gasto de consumo público (G_cons)", "FMI — General Government Final Consumption Expenditure (% PIB)"),
        ("Gasto de transferencias (G_trans)", "Banco Mundial — Social Protection & Labor, transfers (% PIB)"),
        ("WGI — Efectividad gubernamental", "Banco Mundial — Worldwide Governance Indicators"),
        ("IIJ — Índice de Integridad", "Fraser Institute + Transparency International CPI"),
        ("WJP — Estado de derecho", "World Justice Project Rule of Law Index"),
        ("Fraser REG / SOE / FISCAL", "Fraser Institute — Economic Freedom of the World"),
        ("Subsidio Exterior (S_E)", "FMI BPM6 (economías avanzadas) / Banco Mundial ODA (economías en desarrollo)"),
        ("PIB nominal", "FMI — World Economic Outlook Database"),
    ]

    df_fuentes = pd.DataFrame(fuentes, columns=['Variable', 'Fuente'])
    st.dataframe(df_fuentes, use_container_width=True, hide_index=True)