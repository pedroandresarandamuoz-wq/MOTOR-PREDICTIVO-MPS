from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json, os, glob, statistics

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
    for d in [os.path.join(BASE,"output_mps"), BASE, "/opt/render/project/src/output_mps"]:
        m = glob.glob(os.path.join(d, f"*{pat}*.json"))
        if m: return max(m, key=os.path.getmtime)
    raise FileNotFoundError(pat)

try:
    MATRIZ = json.load(open(find("matriz_completa"), encoding="utf-8"))
    PAISES = sorted(MATRIZ.keys())
    ANOS   = sorted({a for p in MATRIZ for a in MATRIZ[p]}, key=int)
    print(f"OK: {len(PAISES)} paises, {ANOS[0]}-{ANOS[-1]}")
except Exception as e:
    print(f"ERROR: {e}")
    MATRIZ, PAISES, ANOS = {}, [], []

NOMBRES = {
    "AFG":"Afganistan","AGO":"Angola","ALB":"Albania","ARE":"Emiratos Arabes",
    "ARG":"Argentina","ARM":"Armenia","AUS":"Australia","AUT":"Austria",
    "AZE":"Azerbaiyan","BDI":"Burundi","BEL":"Belgica","BEN":"Benin",
    "BFA":"Burkina Faso","BGD":"Bangla","BGR":"Bulgaria","BHR":"Barein",
    "BIH":"Bosnia","BLR":"Bielorrusia","BOL":"Bolivia","BRA":"Brasil",
    "BRB":"Barbados","BRN":"Brunei","BTN":"Butan","BWA":"Botsuana",
    "CAF":"R.Centroafricana","CAN":"Canada","CHE":"Suiza","CHL":"Chile",
    "CHN":"China","CMR":"Camerun","COD":"R.D.Congo","COG":"Congo",
    "COL":"Colombia","COM":"Comoras","CRI":"Costa Rica","CUB":"Cuba",
    "CYP":"Chipre","CZE":"Rep.Checa","DEU":"Alemania","DJI":"Yibuti",
    "DNK":"Dinamarca","DOM":"R.Dominicana","DZA":"Argelia","ECU":"Ecuador",
    "EGY":"Egipto","ESP":"Espana","EST":"Estonia","ETH":"Etiopia",
    "FIN":"Finlandia","FJI":"Fiyi","FRA":"Francia","GAB":"Gabon",
    "GBR":"Reino Unido","GEO":"Georgia","GHA":"Ghana","GIN":"Guinea",
    "GMB":"Gambia","GNB":"Guinea-Bisau","GRC":"Grecia","GTM":"Guatemala",
    "GUY":"Guyana","HKG":"Hong Kong","HND":"Honduras","HRV":"Croacia",
    "HTI":"Haiti","HUN":"Hungria","IDN":"Indonesia","IND":"India",
    "IRL":"Irlanda","IRN":"Iran","IRQ":"Irak","ISL":"Islandia",
    "ISR":"Israel","ITA":"Italia","JAM":"Jamaica","JOR":"Jordania",
    "JPN":"Japon","KAZ":"Kazajistan","KEN":"Kenia","KGZ":"Kirguistan",
    "KHM":"Camboya","KOR":"Corea del Sur","KWT":"Kuwait","LAO":"Laos",
    "LBN":"Libano","LBR":"Liberia","LBY":"Libia","LSO":"Lesoto",
    "LTU":"Lituania","LUX":"Luxemburgo","LVA":"Letonia","MAR":"Marruecos",
    "MDA":"Moldavia","MDG":"Madagascar","MDV":"Maldivas","MEX":"Mexico",
    "MKD":"Macedonia N.","MLI":"Mali","MMR":"Myanmar","MNE":"Montenegro",
    "MNG":"Mongolia","MOZ":"Mozambique","MRT":"Mauritania","MUS":"Mauricio",
    "MWI":"Malawi","MYS":"Malasia","NAM":"Namibia","NER":"Niger",
    "NGA":"Nigeria","NIC":"Nicaragua","NLD":"Paises Bajos","NOR":"Noruega",
    "NPL":"Nepal","NZL":"Nueva Zelanda","OMN":"Oman","PAK":"Pakistan",
    "PAN":"Panama","PER":"Peru","PHL":"Filipinas","PNG":"Papua N.Guinea",
    "POL":"Polonia","PRY":"Paraguay","PSE":"Palestina","QAT":"Qatar",
    "ROU":"Rumania","RUS":"Rusia","RWA":"Ruanda","SAU":"Arabia Saudi",
    "SDN":"Sudan","SEN":"Senegal","SGP":"Singapur","SLE":"Sierra Leona",
    "SLV":"El Salvador","SOM":"Somalia","SRB":"Serbia","SSD":"Sudan del Sur",
    "SUR":"Surinam","SVK":"Eslovaquia","SVN":"Eslovenia","SWE":"Suecia",
    "SWZ":"Suazilandia","SYR":"Siria","TCD":"Chad","TGO":"Togo",
    "THA":"Tailandia","TJK":"Tayikistan","TLS":"Timor Oriental",
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
    "CHN":"Asia Oriental","IND":"Asia del Sur","IDN":"Asia Sudoriental",
    "RUS":"Europa del Este","TUR":"Oriente Medio","SAU":"Oriente Medio",
    "ARE":"Oriente Medio","QAT":"Oriente Medio","NGA":"Africa Subsahariana",
    "ETH":"Africa Subsahariana","KEN":"Africa Subsahariana","ZAF":"Africa Subsahariana",
    "EGY":"Africa del Norte","MAR":"Africa del Norte",
}

def nom(iso): return NOMBRES.get(iso, iso)
def reg(iso): return REGIONES.get(iso, "Otras")

@app.get("/")
def root():
    return resp({"status":"ok","paises":len(PAISES),"anos":f"{ANOS[0]}-{ANOS[-1]}" if ANOS else "?"})

@app.get("/api/paises")
def get_paises():
    return resp(sorted([{"iso":p,"nombre":nom(p),"region":reg(p)} for p in PAISES], key=lambda x:x["nombre"]))

@app.get("/api/tendencia")
def get_tendencia():
    out=[]
    for a in ANOS:
        vals=[MATRIZ[p][a]["PN"] for p in PAISES if a in MATRIZ[p]
              and MATRIZ[p][a].get("PN") is not None
              and MATRIZ[p][a].get("grupo")=="A"
              and -500<=MATRIZ[p][a]["PN"]<=100]
        if vals:
            out.append({"ano":int(a),"mediana":round(statistics.median(vals),2),
                "pct_pos":round(sum(1 for v in vals if v>0)/len(vals)*100,1),
                "n":len(vals),"proyectado":int(a)>2023})
    return resp(out)

@app.get("/api/global/{anio}")
def get_global(anio: str):
    vals=[MATRIZ[p][anio]["PN"] for p in PAISES if anio in MATRIZ[p]
          and MATRIZ[p][anio].get("PN") is not None
          and MATRIZ[p][anio].get("grupo")=="A"
          and -500<=MATRIZ[p][anio]["PN"]<=100]
    return resp({
        "ano": int(anio),
        "n_paises": len([p for p in PAISES if anio in MATRIZ[p]]),
        "pn_mediana": round(statistics.median(vals),2) if vals else None,
        "pct_positivos": round(sum(1 for v in vals if v>0)/len(vals)*100,1) if vals else None,
        "proyectado": int(anio)>2023,
    })

@app.get("/api/scatter/{anio}")
def get_scatter(anio: str):
    pts=[]
    for p in PAISES:
        if anio not in MATRIZ[p]: continue
        d=MATRIZ[p][anio]
        pn=d.get("PN"); tpl=d.get("TPL")
        if pn is None or tpl is None or tpl>1000 or pn<-500: continue
        pts.append({"iso":p,"nombre":nom(p),"pn":round(pn,2),"tpl":round(tpl,2),
            "eri":round(d.get("ERI",0),3),"grupo":d.get("grupo")})
    return resp({"ano":int(anio),"puntos":pts})

@app.get("/api/pais/{iso}")
def get_pais(iso: str):
    iso=iso.upper()
    if iso not in MATRIZ: return resp({"error":"no encontrado"})
    serie={}
    for a in ANOS:
        if a not in MATRIZ[iso]: continue
        d=MATRIZ[iso][a]
        serie[a]={"pn":d.get("PN"),"tpl":d.get("TPL"),"eri":d.get("ERI"),
            "ch":d.get("C_H"),"gc":d.get("G_cons_pct"),"gt":d.get("G_trans_pct"),
            "inv":d.get("inversion_pct"),"ps":d.get("PS"),
            "grupo":d.get("grupo"),"proy":d.get("proyectado",False)}
    return resp({"iso":iso,"nombre":nom(iso),"region":reg(iso),"serie":serie})

@app.get("/api/ranking/{anio}")
def get_ranking(anio: str):
    filas=[]
    for p in PAISES:
        if anio not in MATRIZ[p]: continue
        d=MATRIZ[p][anio]; pn=d.get("PN")
        if pn is None: continue
        filas.append({"iso":p,"nombre":nom(p),"pn":round(pn,2),
            "tpl":round(d.get("TPL",0),2),"grupo":d.get("grupo"),
            "proy":d.get("proyectado",False)})
    filas.sort(key=lambda x:x["pn"],reverse=True)
    return resp({"ano":int(anio),"top":filas[:20],"bottom":filas[-20:][::-1],
                 "todos":filas,"total":len(filas)})

@app.get("/api/tabla/{anio}")
def get_tabla(anio: str):
    filas=[]
    for p in PAISES:
        if anio not in MATRIZ[p]: continue
        d=MATRIZ[p][anio]
        filas.append({"iso":p,"nombre":nom(p),"region":reg(p),
            "pn":   round(d["PN"],2)          if d.get("PN")  is not None else None,
            "tpl":  round(d["TPL"],2)         if d.get("TPL") is not None else None,
            "eri":  round(d["ERI"],3)         if d.get("ERI") is not None else None,
            "ch":   round(d["C_H"],2)         if d.get("C_H") is not None else None,
            "gc":   round(d["G_cons_pct"],2)  if d.get("G_cons_pct")  is not None else None,
            "gt":   round(d["G_trans_pct"],2) if d.get("G_trans_pct") is not None else None,
            "grupo":d.get("grupo"),"proy":d.get("proyectado",False)})
    filas.sort(key=lambda x:(x["pn"] or -9999),reverse=True)
    return resp({"ano":int(anio),"paises":filas})

@app.get("/api/alertas")
def get_alertas():
    try:
        alertas = json.load(open(find("alertas"), encoding="utf-8"))
    except:
        return resp({"total":0,"alertas":[]})
    proy = [a for a in alertas if a.get("proyectado")]
    grupo_a = [a for a in proy
               if MATRIZ.get(a.get("pais",""),{}).get(str(a.get("ano",a.get("año",""))),{}).get("grupo")=="A"]
    return resp({"total":len(alertas),"proyectadas":len(proy),"grupo_a":len(grupo_a),
                 "alertas":sorted(grupo_a, key=lambda x:x.get("delta",0))[:30]})

@app.get("/api/grupos/{anio}")
def get_grupos(anio: str):
    grupos = {"A":[],"B":[],"C":[]}
    for p in PAISES:
        if anio not in MATRIZ[p]: continue
        d = MATRIZ[p][anio]
        g = d.get("grupo","A")
        if g in grupos:
            grupos[g].append({
                "iso":p,"nombre":nom(p),"region":reg(p),
                "pn":round(d.get("PN",0),2) if d.get("PN") is not None else None,
                "tpl":round(d.get("TPL",0),2) if d.get("TPL") is not None else None,
                "eri":round(d.get("ERI",0),3) if d.get("ERI") is not None else None,
                "ch":round(d.get("C_H",0),2) if d.get("C_H") is not None else None,
            })
    for g in grupos:
        grupos[g].sort(key=lambda x:(x["pn"] or -9999),reverse=True)
    return resp({"anio":int(anio),"grupos":grupos,
                 "counts":{"A":len(grupos["A"]),"B":len(grupos["B"]),"C":len(grupos["C"])}})

@app.get("/api/ranking_tpl/{anio}")
def get_ranking_tpl(anio: str):
    filas=[]
    for p in PAISES:
        if anio not in MATRIZ[p]: continue
        d=MATRIZ[p][anio]
        tpl=d.get("TPL")
        pn=d.get("PN")
        if tpl is None or tpl>500: continue
        filas.append({"iso":p,"nombre":nom(p),"tpl":round(tpl,2),
            "pn":round(pn,2) if pn is not None else None,
            "grupo":d.get("grupo"),"proy":d.get("proyectado",False)})
    filas.sort(key=lambda x:x["tpl"])
    return resp({"ano":int(anio),"paises":filas[:30]})
