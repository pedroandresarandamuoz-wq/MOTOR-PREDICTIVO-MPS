from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json, os, glob, statistics

app = FastAPI()

# CORS manual en cada respuesta
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

def load():
    return (
        json.load(open(find("matriz_completa"), encoding="utf-8")),
        json.load(open(find("alertas"),         encoding="utf-8")),
        json.load(open(find("rankings"),        encoding="utf-8")),
    )

try:
    MATRIZ, ALERTAS, RANKINGS = load()
    PAISES = sorted(MATRIZ.keys())
    AÑOS   = sorted({a for p in MATRIZ for a in MATRIZ[p]}, key=int)
    print(f"OK: {len(PAISES)} países, {AÑOS[0]}-{AÑOS[-1]}")
except Exception as e:
    print(f"ERROR: {e}")
    MATRIZ, ALERTAS, RANKINGS, PAISES, AÑOS = {}, [], {}, [], []

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
    "IRL":"Europa Occidental","SGP":"Asia Sudoriental","HKG":"Asia Oriental",
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

def nom(iso): return NOMBRES.get(iso, iso)
def reg(iso): return REGIONES.get(iso, "Otras")

@app.get("/")
def root():
    return resp({"status":"ok","paises":len(PAISES),"años":f"{AÑOS[0]}-{AÑOS[-1]}" if AÑOS else "?"})

@app.get("/api/paises")
def get_paises():
    return resp(sorted([{"iso":p,"nombre":nom(p),"region":reg(p)} for p in PAISES], key=lambda x:x["nombre"]))

@app.get("/api/tendencia")
def get_tendencia():
    out=[]
    for a in AÑOS:
        vals=[MATRIZ[p][a]["PN"] for p in PAISES if a in MATRIZ[p] and MATRIZ[p][a].get("PN") is not None
              and MATRIZ[p][a].get("grupo")=="A" and -500<=MATRIZ[p][a]["PN"]<=100]
        if vals:
            out.append({"año":int(a),"mediana":round(statistics.median(vals),2),
                "media":round(statistics.mean(vals),2),
                "pct_pos":round(sum(1 for v in vals if v>0)/len(vals)*100,1),
                "n":len(vals),"proyectado":int(a)>2023})
    return resp(out)

@app.get("/api/global/{año}")
def get_global(año:str):
    vals=[MATRIZ[p][año]["PN"] for p in PAISES if año in MATRIZ[p]
          and MATRIZ[p][año].get("PN") is not None and MATRIZ[p][año].get("grupo")=="A"
          and -500<=MATRIZ[p][año]["PN"]<=100]
    return resp({"año":int(año),"n_paises":len([p for p in PAISES if año in MATRIZ[p]]),
        "pn_mediana":round(statistics.median(vals),2) if vals else None,
        "pct_positivos":round(sum(1 for v in vals if v>0)/len(vals)*100,1) if vals else None,
        "proyectado":int(año)>2023})

@app.get("/api/scatter/{año}")
def get_scatter(año:str):
    pts=[]
    for p in PAISES:
        if año not in MATRIZ[p]: continue
        d=MATRIZ[p][año]
        pn=d.get("PN"); tpl=d.get("TPL")
        if pn is None or tpl is None or tpl>1000 or pn<-500: continue
        pts.append({"iso":p,"nombre":nom(p),"pn":round(pn,2),"tpl":round(tpl,2),
            "eri":round(d.get("ERI",0),3),"grupo":d.get("grupo")})
    return resp({"año":int(año),"puntos":pts})

@app.get("/api/pais/{iso}")
def get_pais(iso:str):
    iso=iso.upper()
    if iso not in MATRIZ: return resp({"error":"no encontrado"})
    serie={}
    for a in AÑOS:
        if a not in MATRIZ[iso]: continue
        d=MATRIZ[iso][a]
        serie[a]={"pn":d.get("PN"),"tpl":d.get("TPL"),"eri":d.get("ERI"),
            "ch":d.get("C_H"),"gc":d.get("G_cons_pct"),"gt":d.get("G_trans_pct"),
            "inv":d.get("inversion_pct"),"ps":d.get("PS"),
            "grupo":d.get("grupo"),"proy":d.get("proyectado",False)}
    return resp({"iso":iso,"nombre":nom(iso),"region":reg(iso),"serie":serie})

@app.get("/api/ranking/{año}")
def get_ranking(año:str):
    filas=[]
    for p in PAISES:
        if año not in MATRIZ[p]: continue
        d=MATRIZ[p][año]; pn=d.get("PN")
        if pn is None: continue
        filas.append({"iso":p,"nombre":nom(p),"pn":round(pn,2),
            "tpl":round(d.get("TPL",0),2),"grupo":d.get("grupo"),"proy":d.get("proyectado",False)})
    filas.sort(key=lambda x:x["pn"],reverse=True)
    return resp({"año":int(año),"top":filas[:20],"bottom":filas[-20:][::-1],"total":len(filas)})

@app.get("/api/tabla/{año}")
def get_tabla(año:str):
    filas=[]
    for p in PAISES:
        if año not in MATRIZ[p]: continue
        d=MATRIZ[p][año]
        filas.append({"iso":p,"nombre":nom(p),"region":reg(p),
            "pn":round(d["PN"],2) if d.get("PN") is not None else None,
            "tpl":round(d["TPL"],2) if d.get("TPL") is not None else None,
            "eri":round(d["ERI"],3) if d.get("ERI") is not None else None,
            "ch":round(d["C_H"],2) if d.get("C_H") is not None else None,
            "gc":round(d["G_cons_pct"],2) if d.get("G_cons_pct") is not None else None,
            "gt":round(d["G_trans_pct"],2) if d.get("G_trans_pct") is not None else None,
            "grupo":d.get("grupo"),"proy":d.get("proyectado",False)})
    filas.sort(key=lambda x:(x["pn"] or -9999),reverse=True)
    return resp({"año":int(año),"paises":filas})
