# MPS API v3 — Motor Predictivo Completo
# Pedro Andres Aranda Munoz
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json, os, glob, statistics, math

app = FastAPI()

def resp(data):
    r = JSONResponse(content=data)
    r.headers["Access-Control-Allow-Origin"] = "*"
    r.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    r.headers["Access-Control-Allow-Headers"] = "*"
    return r

@app.options("/{rest:path}")
async def options(rest: str):
    r = JSONResponse(content={})
    r.headers["Access-Control-Allow-Origin"] = "*"
    r.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    r.headers["Access-Control-Allow-Headers"] = "*"
    return r

BASE = os.path.dirname(os.path.abspath(__file__))

def find(pat):
    for d in [os.path.join(BASE,"output_mps"), BASE,
              "/opt/render/project/src/output_mps",
              "/opt/render/project/src"]:
        m = glob.glob(os.path.join(d, f"*{pat}*.json"))
        if m: return max(m, key=os.path.getmtime)
    raise FileNotFoundError(pat)

def find_direct(filename):
    for d in [BASE, os.path.join(BASE,"output_mps"),
              "/opt/render/project/src"]:
        p = os.path.join(d, filename)
        if os.path.exists(p): return p
    raise FileNotFoundError(filename)

# Carga principal
try:
    MATRIZ = json.load(open(find("matriz_completa"), encoding="utf-8"))
    PAISES = sorted(MATRIZ.keys())
    ANOS   = sorted({a for p in MATRIZ for a in MATRIZ[p]}, key=int)
    print(f"OK matriz: {len(PAISES)} paises, {ANOS[0]}-{ANOS[-1]}")
except Exception as e:
    print(f"ERROR matriz: {e}")
    MATRIZ, PAISES, ANOS = {}, [], []

# Datos institucionales para componentes CH
try:
    INST = json.load(open(find_direct("almacen_datos_maestro.json"), encoding="utf-8"))
    print(f"OK institucional: {len(INST)} paises")
except Exception as e:
    print(f"WARN institucional: {e}")
    INST = {}

# Interdependencia
try:
    INTER = json.load(open(find_direct("interdependencia.json"), encoding="utf-8"))
    print(f"OK interdependencia: {len(INTER)} paises")
except Exception as e:
    print(f"WARN interdependencia: {e}")
    INTER = {}

# Alertas
try:
    ALERTAS = json.load(open(find("alertas"), encoding="utf-8"))
    print(f"OK alertas: {len(ALERTAS)}")
except Exception as e:
    print(f"WARN alertas: {e}")
    ALERTAS = []

NOMBRES = {
    "AFG":"Afganistan","AGO":"Angola","ALB":"Albania","ARE":"Emiratos Arabes",
    "ARG":"Argentina","ARM":"Armenia","AUS":"Australia","AUT":"Austria",
    "AZE":"Azerbaiyan","BDI":"Burundi","BEL":"Belgica","BEN":"Benin",
    "BFA":"Burkina Faso","BGD":"Bangladesh","BGR":"Bulgaria","BHR":"Barein",
    "BIH":"Bosnia-Herz.","BLR":"Bielorrusia","BLZ":"Belice","BOL":"Bolivia",
    "BRA":"Brasil","BRB":"Barbados","BRN":"Brunei","BTN":"Butan",
    "BWA":"Botsuana","CAF":"R.Centroafricana","CAN":"Canada","CHE":"Suiza",
    "CHL":"Chile","CHN":"China","CMR":"Camerun","COD":"R.D.Congo",
    "COG":"Congo","COL":"Colombia","COM":"Comoras","CRI":"Costa Rica",
    "CUB":"Cuba","CYP":"Chipre","CZE":"Rep.Checa","DEU":"Alemania",
    "DJI":"Yibuti","DNK":"Dinamarca","DOM":"R.Dominicana","DZA":"Argelia",
    "ECU":"Ecuador","EGY":"Egipto","ESP":"Espana","EST":"Estonia",
    "ETH":"Etiopia","FIN":"Finlandia","FJI":"Fiyi","FRA":"Francia",
    "GAB":"Gabon","GBR":"Reino Unido","GEO":"Georgia","GHA":"Ghana",
    "GIN":"Guinea","GMB":"Gambia","GNB":"Guinea-Bisau","GRC":"Grecia",
    "GTM":"Guatemala","GUY":"Guyana","HKG":"Hong Kong","HND":"Honduras",
    "HRV":"Croacia","HTI":"Haiti","HUN":"Hungria","IDN":"Indonesia",
    "IND":"India","IRL":"Irlanda","IRN":"Iran","IRQ":"Irak",
    "ISL":"Islandia","ISR":"Israel","ITA":"Italia","JAM":"Jamaica",
    "JOR":"Jordania","JPN":"Japon","KAZ":"Kazajistan","KEN":"Kenia",
    "KGZ":"Kirguistan","KHM":"Camboya","KOR":"Corea del Sur","KWT":"Kuwait",
    "LAO":"Laos","LBN":"Libano","LBR":"Liberia","LBY":"Libia",
    "LSO":"Lesoto","LTU":"Lituania","LUX":"Luxemburgo","LVA":"Letonia",
    "MAR":"Marruecos","MDA":"Moldavia","MDG":"Madagascar","MDV":"Maldivas",
    "MEX":"Mexico","MKD":"Macedonia N.","MLI":"Mali","MMR":"Myanmar",
    "MNE":"Montenegro","MNG":"Mongolia","MOZ":"Mozambique","MRT":"Mauritania",
    "MUS":"Mauricio","MWI":"Malawi","MYS":"Malasia","NAM":"Namibia",
    "NER":"Niger","NGA":"Nigeria","NIC":"Nicaragua","NLD":"Paises Bajos",
    "NOR":"Noruega","NPL":"Nepal","NZL":"Nueva Zelanda","OMN":"Oman",
    "PAK":"Pakistan","PAN":"Panama","PER":"Peru","PHL":"Filipinas",
    "PNG":"Papua N.Guinea","POL":"Polonia","PRY":"Paraguay","PSE":"Palestina",
    "QAT":"Qatar","ROU":"Rumania","RUS":"Rusia","RWA":"Ruanda",
    "SAU":"Arabia Saudi","SDN":"Sudan","SEN":"Senegal","SGP":"Singapur",
    "SLE":"Sierra Leona","SLV":"El Salvador","SOM":"Somalia","SRB":"Serbia",
    "SSD":"Sudan del Sur","SUR":"Surinam","SVK":"Eslovaquia","SVN":"Eslovenia",
    "SWE":"Suecia","SWZ":"Suazilandia","SYR":"Siria","TCD":"Chad",
    "TGO":"Togo","THA":"Tailandia","TJK":"Tayikistan","TLS":"Timor Oriental",
    "TTO":"Trinidad y Tobago","TUN":"Tunez","TUR":"Turquia","TWN":"Taiwan",
    "TZA":"Tanzania","UGA":"Uganda","UKR":"Ucrania","URY":"Uruguay",
    "USA":"EE.UU.","UZB":"Uzbekistan","VEN":"Venezuela","VNM":"Vietnam",
    "WSM":"Samoa","YEM":"Yemen","ZAF":"Sudafrica","ZMB":"Zambia","ZWE":"Zimbabue",
}

REGIONES = {
    "TWN":"Asia Oriental","CHE":"Europa Occidental","USA":"America del Norte",
    "IRL":"Europa Occidental","SGP":"Asia Sudoriental","HKG":"Asia Oriental",
    "NZL":"Oceania","AUS":"Oceania","KOR":"Asia Oriental","JPN":"Asia Oriental",
    "CAN":"America del Norte","GBR":"Europa Occidental","DEU":"Europa Occidental",
    "ESP":"Europa Occidental","FRA":"Europa Occidental","ITA":"Europa Occidental",
    "NOR":"Europa Occidental","SWE":"Europa Occidental","DNK":"Europa Occidental",
    "FIN":"Europa Occidental","BEL":"Europa Occidental","NLD":"Europa Occidental",
    "AUT":"Europa Occidental","POL":"Europa del Este","CZE":"Europa del Este",
    "HUN":"Europa del Este","ROU":"Europa del Este","ARG":"America Latina",
    "BRA":"America Latina","MEX":"America Latina","COL":"America Latina",
    "PER":"America Latina","CHL":"America Latina","VEN":"America Latina",
    "CHN":"Asia Oriental","IND":"Asia del Sur","IDN":"Asia Sudoriental",
    "RUS":"Europa del Este","TUR":"Oriente Medio","SAU":"Oriente Medio",
    "ARE":"Oriente Medio","QAT":"Oriente Medio","IRN":"Oriente Medio",
    "IRQ":"Oriente Medio","ISR":"Oriente Medio","NGA":"Africa Subsahariana",
    "ETH":"Africa Subsahariana","KEN":"Africa Subsahariana","ZAF":"Africa Subsahariana",
    "EGY":"Africa del Norte","MAR":"Africa del Norte","DZA":"Africa del Norte",
    "TUN":"Africa del Norte","LBY":"Africa del Norte",
}

def nom(iso): return NOMBRES.get(iso, iso)
def reg(iso):  return REGIONES.get(iso, "Otras")
def rnd(v, d=2):
    if v is None: return None
    try: return round(float(v), d)
    except: return None

# ── ENDPOINTS ────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return resp({"status":"ok","paises":len(PAISES),
                 "anos":f"{ANOS[0]}-{ANOS[-1]}" if ANOS else "?"})

@app.get("/api/paises")
def get_paises():
    return resp(sorted([
        {"iso":p,"nombre":nom(p),"region":reg(p)}
        for p in PAISES
    ], key=lambda x: x["nombre"]))

@app.get("/api/tendencia")
def get_tendencia():
    out = []
    for a in ANOS:
        vals = [MATRIZ[p][a]["PN"] for p in PAISES
                if a in MATRIZ[p] and MATRIZ[p][a].get("PN") is not None
                and MATRIZ[p][a].get("grupo") == "A"
                and -500 <= MATRIZ[p][a]["PN"] <= 100]
        if vals:
            out.append({
                "ano": int(a),
                "mediana": rnd(statistics.median(vals)),
                "pct_pos": rnd(sum(1 for v in vals if v>0)/len(vals)*100, 1),
                "n": len(vals),
                "proyectado": int(a) > 2023,
            })
    return resp(out)

@app.get("/api/global/{anio}")
def get_global(anio: str):
    vals = [MATRIZ[p][anio]["PN"] for p in PAISES
            if anio in MATRIZ[p] and MATRIZ[p][anio].get("PN") is not None
            and MATRIZ[p][anio].get("grupo") == "A"
            and -500 <= MATRIZ[p][anio]["PN"] <= 100]
    return resp({
        "ano": int(anio),
        "n_paises": len([p for p in PAISES if anio in MATRIZ[p]]),
        "pn_mediana": rnd(statistics.median(vals)) if vals else None,
        "pct_positivos": rnd(sum(1 for v in vals if v>0)/len(vals)*100, 1) if vals else None,
        "proyectado": int(anio) > 2023,
    })

@app.get("/api/scatter/{anio}")
def get_scatter(anio: str):
    pts = []
    for p in PAISES:
        if anio not in MATRIZ[p]: continue
        d = MATRIZ[p][anio]
        pn = d.get("PN"); tpl = d.get("TPL")
        if pn is None or tpl is None or tpl > 1000 or pn < -500: continue
        pts.append({
            "iso": p, "nombre": nom(p), "region": reg(p),
            "pn": rnd(pn), "tpl": rnd(tpl),
            "eri": rnd(d.get("ERI"), 3),
            "ch": rnd(d.get("C_H")),
            "grupo": d.get("grupo") or "A",
        })
    return resp({"ano": int(anio), "puntos": pts})

@app.get("/api/pais/{iso}")
def get_pais(iso: str):
    iso = iso.upper()
    if iso not in MATRIZ:
        return resp({"error": "no encontrado"})

    serie = {}
    for a in ANOS:
        if a not in MATRIZ[iso]: continue
        d = MATRIZ[iso][a]
        # Componentes CH desde almacen institucional
        ch_comp = {}
        if iso in INST and a in INST[iso]:
            ins = INST[iso][a]
            iij  = ins.get("IIJ", 0) or 0
            wjp  = ins.get("WJP_ROL", 0) or 0
            freg = ins.get("FRASER_REG", 0) or 0
            fsoe = ins.get("FRASER_SOE", 0) or 0
            ffis = ins.get("FRASER_FISCAL", 0) or 0
            ch_comp = {
                "integridad":  rnd((10-iij)*10),
                "juridico":    rnd((10-wjp)*10),
                "regulacion":  rnd((10-freg)*10),
                "soe":         rnd((10-fsoe)*10),
                "fiscal":      rnd((10-ffis)*10),
            }

        # Interdependencia
        inter = {}
        if iso in INTER and a in INTER[iso]:
            it = INTER[iso][a]
            fin = it.get("financiero", {}) or {}
            sec = it.get("sectorial", {}) or {}
            com = it.get("comercio", {}) or {}
            pib = d.get("PIB_nominal") or 1
            inter = {
                "oda_pct":        rnd((fin.get("oda_recibida_usd") or 0)/pib*100, 3),
                "remesas_pct":    rnd((fin.get("remesas_recibidas_usd") or 0)/pib*100, 3),
                "tech_exp_pct":   rnd(sec.get("tech_exports_pct"), 2),
                "energy_imp_pct": rnd(sec.get("energy_imports_pct"), 2),
                "bal_comercial":  rnd((com.get("balance") or 0)/pib*100, 2),
                "exportaciones":  rnd((com.get("exportaciones") or 0)/1e9, 1),
                "importaciones":  rnd((com.get("importaciones") or 0)/1e9, 1),
            }

        serie[a] = {
            "pn":    rnd(d.get("PN")),
            "tpl":   rnd(d.get("TPL")),
            "eri":   rnd(d.get("ERI"), 3),
            "ch":    rnd(d.get("C_H")),
            "gc":    rnd(d.get("G_cons_pct")),
            "gt":    rnd(d.get("G_trans_pct")),
            "inv":   rnd(d.get("inversion_pct")),
            "ps":    rnd(d.get("PS")),
            "se":    rnd(d.get("PS", 0) - d.get("PN", 0), 2) if d.get("PS") is not None and d.get("PN") is not None else None,
            "grupo": d.get("grupo") or "A",
            "proy":  d.get("proyectado", False),
            "ch_comp": ch_comp,
            "inter":   inter,
        }

    return resp({
        "iso":    iso,
        "nombre": nom(iso),
        "region": reg(iso),
        "serie":  serie,
    })

@app.get("/api/ranking/{anio}")
def get_ranking(anio: str):
    filas = []
    for p in PAISES:
        if anio not in MATRIZ[p]: continue
        d = MATRIZ[p][anio]
        pn = d.get("PN")
        if pn is None: continue
        filas.append({
            "iso":    p,
            "nombre": nom(p),
            "region": reg(p),
            "pn":     rnd(pn),
            "tpl":    rnd(d.get("TPL")),
            "ch":     rnd(d.get("C_H")),
            "eri":    rnd(d.get("ERI"), 3),
            "grupo":  d.get("grupo") or "A",
            "proy":   d.get("proyectado", False),
        })
    filas.sort(key=lambda x: (x["pn"] or -9999), reverse=True)
    return resp({
        "ano":    int(anio),
        "top":    filas[:20],
        "bottom": filas[-20:][::-1],
        "todos":  filas,
        "total":  len(filas),
    })

@app.get("/api/ranking_tpl/{anio}")
def get_ranking_tpl(anio: str):
    filas = []
    for p in PAISES:
        if anio not in MATRIZ[p]: continue
        d = MATRIZ[p][anio]
        tpl = d.get("TPL")
        pn  = d.get("PN")
        if tpl is None or tpl > 500: continue
        filas.append({
            "iso":    p,
            "nombre": nom(p),
            "tpl":    rnd(tpl),
            "pn":     rnd(pn),
            "grupo":  d.get("grupo") or "A",
            "proy":   d.get("proyectado", False),
        })
    filas.sort(key=lambda x: x["tpl"])
    return resp({"ano": int(anio), "paises": filas[:30]})

@app.get("/api/tabla/{anio}")
def get_tabla(anio: str):
    filas = []
    for p in PAISES:
        if anio not in MATRIZ[p]: continue
        d = MATRIZ[p][anio]
        filas.append({
            "iso":    p,
            "nombre": nom(p),
            "region": reg(p),
            "pn":     rnd(d.get("PN")),
            "tpl":    rnd(d.get("TPL")),
            "eri":    rnd(d.get("ERI"), 3),
            "ch":     rnd(d.get("C_H")),
            "gc":     rnd(d.get("G_cons_pct")),
            "gt":     rnd(d.get("G_trans_pct")),
            "grupo":  d.get("grupo") or "A",
            "proy":   d.get("proyectado", False),
        })
    filas.sort(key=lambda x: (x["pn"] or -9999), reverse=True)
    return resp({"ano": int(anio), "paises": filas})

@app.get("/api/grupos/{anio}")
def get_grupos(anio: str):
    grupos = {"A": [], "B": [], "C": []}
    for p in PAISES:
        if anio not in MATRIZ[p]: continue
        d = MATRIZ[p][anio]
        g = d.get("grupo") or "A"
        if g not in grupos: continue
        grupos[g].append({
            "iso":    p,
            "nombre": nom(p),
            "region": reg(p),
            "pn":     rnd(d.get("PN")),
            "tpl":    rnd(d.get("TPL")),
            "eri":    rnd(d.get("ERI"), 3),
            "ch":     rnd(d.get("C_H")),
        })
    for g in grupos:
        grupos[g].sort(key=lambda x: (x["pn"] or -9999), reverse=True)
    return resp({
        "anio":   int(anio),
        "grupos": grupos,
        "counts": {g: len(grupos[g]) for g in grupos},
    })

@app.get("/api/alertas")
def get_alertas():
    if not ALERTAS:
        return resp({"total": 0, "alertas": []})
    proy = [a for a in ALERTAS if a.get("proyectado")]
    grupo_a = []
    for a in proy:
        pais = a.get("pais", "")
        ano  = str(a.get("ano", a.get("año", "")))
        if MATRIZ.get(pais, {}).get(ano, {}).get("grupo") == "A" and (a.get("delta") or 0) < -10:
            grupo_a.append({
                "pais":    pais,
                "nombre":  nom(pais),
                "ano":     ano,
                "pn_ant":  rnd(a.get("pn_ant")),
                "pn_act":  rnd(a.get("pn_act")),
                "delta":   rnd(a.get("delta")),
                "tipo":    a.get("tipo", "DETERIORO"),
            })
    grupo_a.sort(key=lambda x: x.get("delta") or 0)
    return resp({
        "total":      len(ALERTAS),
        "proyectadas": len(proy),
        "grupo_a":    len(grupo_a),
        "alertas":    grupo_a[:30],
    })

@app.get("/api/comparar/{iso1}/{iso2}/{anio}")
def get_comparar(iso1: str, iso2: str, anio: str):
    result = {}
    for iso in [iso1.upper(), iso2.upper()]:
        if iso not in MATRIZ:
            result[iso] = {"error": "no encontrado"}
            continue
        serie = {}
        for a in ANOS:
            if a not in MATRIZ[iso]: continue
            d = MATRIZ[iso][a]
            serie[a] = {
                "pn":  rnd(d.get("PN")),
                "tpl": rnd(d.get("TPL")),
                "ch":  rnd(d.get("C_H")),
                "eri": rnd(d.get("ERI"), 3),
                "proy": d.get("proyectado", False),
            }
        result[iso] = {"nombre": nom(iso), "region": reg(iso), "serie": serie}
    return resp(result)
