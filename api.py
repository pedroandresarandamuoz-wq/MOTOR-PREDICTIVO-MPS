# -*- coding: utf-8 -*-
"""
MPS API — Backend FastAPI
Lee los JSON de output_mps/ y sirve endpoints para el dashboard
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json, os, glob, statistics, math

app = FastAPI(title="MPS API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ─── Carga de datos ────────────────────────────────────────────────────────
def find_json(patron):
    rutas = glob.glob(f"./output_mps/*{patron}*.json")
    if not rutas:
        raise FileNotFoundError(f"No se encuentra fichero con patrón: {patron}")
    return max(rutas, key=os.path.getmtime)

def load():
    matriz   = json.load(open(find_json("matriz_completa"),   encoding="utf-8"))
    alertas  = json.load(open(find_json("alertas"),           encoding="utf-8"))
    rankings = json.load(open(find_json("rankings"),          encoding="utf-8"))
    interdep = json.load(open(find_json("interdependencia"),  encoding="utf-8"))
    return matriz, alertas, rankings, interdep

try:
    MATRIZ, ALERTAS, RANKINGS, INTERDEP = load()
    PAISES = sorted(MATRIZ.keys())
    AÑOS   = sorted({a for p in MATRIZ for a in MATRIZ[p]}, key=int)
    print(f"[OK] Datos cargados: {len(PAISES)} países, años {AÑOS[0]}-{AÑOS[-1]}")
except Exception as e:
    print(f"[ERROR] {e}")
    MATRIZ, ALERTAS, RANKINGS, INTERDEP = {}, [], {}, {}
    PAISES, AÑOS = [], []

NOMBRES = {
    "AFG":"Afganistán","AGO":"Angola","ALB":"Albania","ARE":"Emiratos Árabes",
    "ARG":"Argentina","ARM":"Armenia","AUS":"Australia","AUT":"Austria",
    "AZE":"Azerbaiyán","BDI":"Burundi","BEL":"Bélgica","BEN":"Benín",
    "BFA":"Burkina Faso","BGD":"Bangladés","BGR":"Bulgaria","BHR":"Baréin",
    "BIH":"Bosnia-Herz.","BLR":"Bielorrusia","BLZ":"Belice","BOL":"Bolivia",
    "BRA":"Brasil","BRB":"Barbados","BRN":"Brunéi","BTN":"Bután",
    "BWA":"Botsuana","CAF":"R.Centroafricana","CAN":"Canadá","CHE":"Suiza",
    "CHL":"Chile","CHN":"China","CMR":"Camerún","COD":"R.D.Congo",
    "COG":"Congo","COL":"Colombia","COM":"Comoras","CRI":"Costa Rica",
    "CUB":"Cuba","CYP":"Chipre","CZE":"Rep.Checa","DEU":"Alemania",
    "DJI":"Yibuti","DNK":"Dinamarca","DOM":"R.Dominicana","DZA":"Argelia",
    "ECU":"Ecuador","EGY":"Egipto","ESP":"España","EST":"Estonia",
    "ETH":"Etiopía","FIN":"Finlandia","FJI":"Fiyi","FRA":"Francia",
    "GAB":"Gabón","GBR":"Reino Unido","GEO":"Georgia","GHA":"Ghana",
    "GIN":"Guinea","GMB":"Gambia","GNB":"Guinea-Bisáu","GRC":"Grecia",
    "GTM":"Guatemala","GUY":"Guyana","HKG":"Hong Kong","HND":"Honduras",
    "HRV":"Croacia","HTI":"Haití","HUN":"Hungría","IDN":"Indonesia",
    "IND":"India","IRL":"Irlanda","IRN":"Irán","IRQ":"Irak",
    "ISL":"Islandia","ISR":"Israel","ITA":"Italia","JAM":"Jamaica",
    "JOR":"Jordania","JPN":"Japón","KAZ":"Kazajistán","KEN":"Kenia",
    "KGZ":"Kirguistán","KHM":"Camboya","KOR":"Corea del Sur","KWT":"Kuwait",
    "LAO":"Laos","LBN":"Líbano","LBR":"Liberia","LBY":"Libia",
    "LSO":"Lesoto","LTU":"Lituania","LUX":"Luxemburgo","LVA":"Letonia",
    "MAR":"Marruecos","MDA":"Moldavia","MDG":"Madagascar","MDV":"Maldivas",
    "MEX":"México","MKD":"Macedonia N.","MLI":"Mali","MMR":"Myanmar",
    "MNE":"Montenegro","MNG":"Mongolia","MOZ":"Mozambique","MRT":"Mauritania",
    "MUS":"Mauricio","MWI":"Malaui","MYS":"Malasia","NAM":"Namibia",
    "NER":"Níger","NGA":"Nigeria","NIC":"Nicaragua","NLD":"Países Bajos",
    "NOR":"Noruega","NPL":"Nepal","NZL":"Nueva Zelanda","OMN":"Omán",
    "PAK":"Pakistán","PAN":"Panamá","PER":"Perú","PHL":"Filipinas",
    "PNG":"Papúa N.Guinea","POL":"Polonia","PRY":"Paraguay","PSE":"Palestina",
    "QAT":"Qatar","ROU":"Rumanía","RUS":"Rusia","RWA":"Ruanda",
    "SAU":"Arabia Saudí","SDN":"Sudán","SEN":"Senegal","SGP":"Singapur",
    "SLE":"Sierra Leona","SLV":"El Salvador","SOM":"Somalia","SRB":"Serbia",
    "SSD":"Sudán del Sur","SUR":"Surinam","SVK":"Eslovaquia","SVN":"Eslovenia",
    "SWE":"Suecia","SWZ":"Suazilandia","SYR":"Siria","TCD":"Chad",
    "TGO":"Togo","THA":"Tailandia","TJK":"Tayikistán","TLS":"Timor Oriental",
    "TTO":"Trinidad y Tobago","TUN":"Túnez","TUR":"Turquía","TWN":"Taiwán",
    "TZA":"Tanzania","UGA":"Uganda","UKR":"Ucrania","URY":"Uruguay",
    "USA":"EE.UU.","UZB":"Uzbekistán","VEN":"Venezuela","VNM":"Vietnam",
    "WSM":"Samoa","YEM":"Yemen","ZAF":"Sudáfrica","ZMB":"Zambia","ZWE":"Zimbabue",
}

REGIONES = {
    "TWN":"Asia Oriental","CHE":"Europa Occidental","USA":"América del Norte",
    "IRL":"Europa Occidental","PHL":"Asia Sudoriental","GTM":"América Latina",
    "CRI":"América Latina","MUS":"África Subsahariana","CHL":"América Latina",
    "CYP":"Europa Occidental","SGP":"Asia Sudoriental","HKG":"Asia Oriental",
    "NZL":"Oceanía","AUS":"Oceanía","KOR":"Asia Oriental","JPN":"Asia Oriental",
    "CAN":"América del Norte","GBR":"Europa Occidental","DEU":"Europa Occidental",
    "ESP":"Europa Occidental","FRA":"Europa Occidental","ITA":"Europa Occidental",
    "NOR":"Europa Occidental","SWE":"Europa Occidental","DNK":"Europa Occidental",
    "FIN":"Europa Occidental","BEL":"Europa Occidental","NLD":"Europa Occidental",
    "AUT":"Europa Occidental","POL":"Europa del Este","CZE":"Europa del Este",
    "HUN":"Europa del Este","ROU":"Europa del Este","ARG":"América Latina",
    "BRA":"América Latina","MEX":"América Latina","COL":"América Latina",
    "CHN":"Asia Oriental","IND":"Asia del Sur","IDN":"Asia Sudoriental",
    "RUS":"Europa del Este","TUR":"Oriente Medio","SAU":"Oriente Medio",
    "ARE":"Oriente Medio","QAT":"Oriente Medio","NGA":"África Subsahariana",
    "ETH":"África Subsahariana","KEN":"África Subsahariana","ZAF":"África Subsahariana",
    "EGY":"África del Norte","MAR":"África del Norte",
}

def nombre(iso): return NOMBRES.get(iso, iso)
def region(iso): return REGIONES.get(iso, "Otras")

# ─── Endpoints ────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "ok", "paises": len(PAISES), "años": f"{AÑOS[0]}-{AÑOS[-1]}"}

@app.get("/api/paises")
def get_paises():
    return sorted([
        {"iso": p, "nombre": nombre(p), "region": region(p)}
        for p in PAISES
    ], key=lambda x: x["nombre"])

@app.get("/api/global/{año}")
def get_global(año: str):
    if año not in AÑOS:
        raise HTTPException(404, f"Año {año} no disponible")
    vals_a = [MATRIZ[p][año]["PN"] for p in PAISES
              if año in MATRIZ[p] and MATRIZ[p][año].get("PN") is not None
              and MATRIZ[p][año].get("grupo") == "A"
              and -500 <= MATRIZ[p][año]["PN"] <= 100]
    tpl_vals = [MATRIZ[p][año]["TPL"] for p in PAISES
                if año in MATRIZ[p] and MATRIZ[p][año].get("TPL") is not None]
    return {
        "año": int(año),
        "n_paises": len([p for p in PAISES if año in MATRIZ[p]]),
        "pn_mediana": round(statistics.median(vals_a), 2) if vals_a else None,
        "pn_media":   round(statistics.mean(vals_a), 2)   if vals_a else None,
        "pct_positivos": round(sum(1 for v in vals_a if v > 0) / len(vals_a) * 100, 1) if vals_a else None,
        "grupo_a": len(vals_a),
        "grupo_b": len([p for p in PAISES if año in MATRIZ[p] and MATRIZ[p][año].get("grupo") == "B"]),
        "grupo_c": len([p for p in PAISES if año in MATRIZ[p] and MATRIZ[p][año].get("grupo") == "C"]),
        "proyectado": int(año) > 2023,
    }

@app.get("/api/tendencia")
def get_tendencia():
    result = []
    for año in AÑOS:
        vals = [MATRIZ[p][año]["PN"] for p in PAISES
                if año in MATRIZ[p] and MATRIZ[p][año].get("PN") is not None
                and MATRIZ[p][año].get("grupo") == "A"
                and -500 <= MATRIZ[p][año]["PN"] <= 100]
        if vals:
            result.append({
                "año": int(año),
                "mediana": round(statistics.median(vals), 2),
                "media":   round(statistics.mean(vals), 2),
                "pct_pos": round(sum(1 for v in vals if v > 0) / len(vals) * 100, 1),
                "n": len(vals),
                "proyectado": int(año) > 2023,
            })
    return result

@app.get("/api/pais/{iso}")
def get_pais(iso: str):
    iso = iso.upper()
    if iso not in MATRIZ:
        raise HTTPException(404, f"País {iso} no encontrado")
    serie = {}
    for año in AÑOS:
        if año not in MATRIZ[iso]:
            continue
        d = MATRIZ[iso][año]
        serie[año] = {
            "pn":    d.get("PN"),
            "tpl":   d.get("TPL"),
            "eri":   d.get("ERI"),
            "ch":    d.get("C_H"),
            "gc":    d.get("G_cons_pct"),
            "gt":    d.get("G_trans_pct"),
            "inv":   d.get("inversion_pct"),
            "ps":    d.get("PS"),
            "grupo": d.get("grupo"),
            "proy":  d.get("proyectado", False),
        }
    return {
        "iso":    iso,
        "nombre": nombre(iso),
        "region": region(iso),
        "serie":  serie,
    }

@app.get("/api/ranking/{año}")
def get_ranking(año: str):
    if año not in AÑOS:
        raise HTTPException(404, f"Año {año} no disponible")
    filas = []
    for p in PAISES:
        if año not in MATRIZ[p]:
            continue
        d = MATRIZ[p][año]
        pn = d.get("PN")
        if pn is None:
            continue
        filas.append({
            "iso":    p,
            "nombre": nombre(p),
            "region": region(p),
            "pn":     round(pn, 2),
            "tpl":    round(d.get("TPL", 0), 2),
            "eri":    round(d.get("ERI", 0), 3),
            "grupo":  d.get("grupo"),
            "proy":   d.get("proyectado", False),
        })
    filas.sort(key=lambda x: x["pn"], reverse=True)
    return {
        "año": int(año),
        "top":    filas[:20],
        "bottom": filas[-20:][::-1],
        "total":  len(filas),
    }

@app.get("/api/scatter/{año}")
def get_scatter(año: str):
    if año not in AÑOS:
        raise HTTPException(404, f"Año {año} no disponible")
    puntos = []
    for p in PAISES:
        if año not in MATRIZ[p]:
            continue
        d = MATRIZ[p][año]
        pn  = d.get("PN")
        tpl = d.get("TPL")
        if pn is None or tpl is None:
            continue
        if tpl > 1000 or pn < -500:
            continue
        puntos.append({
            "iso":    p,
            "nombre": nombre(p),
            "pn":     round(pn, 2),
            "tpl":    round(tpl, 2),
            "eri":    round(d.get("ERI", 0), 3),
            "grupo":  d.get("grupo"),
        })
    return {"año": int(año), "puntos": puntos}

@app.get("/api/alertas")
def get_alertas():
    proy = [a for a in ALERTAS if a.get("proyectado")]
    grupo_a = [a for a in proy
               if MATRIZ.get(a["pais"], {}).get(str(a["año"]), {}).get("grupo") == "A"]
    return {
        "total":    len(ALERTAS),
        "proyect":  len(proy),
        "grupo_a":  len(grupo_a),
        "alertas":  sorted(grupo_a, key=lambda x: x["delta"])[:30],
    }

@app.get("/api/tabla/{año}")
def get_tabla(año: str):
    if año not in AÑOS:
        raise HTTPException(404, f"Año {año} no disponible")
    filas = []
    for p in PAISES:
        if año not in MATRIZ[p]:
            continue
        d = MATRIZ[p][año]
        filas.append({
            "iso":    p,
            "nombre": nombre(p),
            "region": region(p),
            "pn":     round(d["PN"], 2)    if d.get("PN")  is not None else None,
            "tpl":    round(d["TPL"], 2)   if d.get("TPL") is not None else None,
            "eri":    round(d["ERI"], 3)   if d.get("ERI") is not None else None,
            "ch":     round(d["C_H"], 2)   if d.get("C_H") is not None else None,
            "gc":     round(d["G_cons_pct"], 2) if d.get("G_cons_pct") is not None else None,
            "gt":     round(d["G_trans_pct"], 2) if d.get("G_trans_pct") is not None else None,
            "grupo":  d.get("grupo"),
            "proy":   d.get("proyectado", False),
        })
    filas.sort(key=lambda x: (x["pn"] or -9999), reverse=True)
    return {"año": int(año), "paises": filas}
