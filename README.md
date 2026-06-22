# ⚖️ Modelo de Prosperidad Sostenible (MPS)

**Autor:** Pedro Andrés Aranda Muñoz  
**Versión:** 1.0 · 2026  

> *"El estado es un parásito que drena la economía. El MPS lo mide."*

---

## ¿Qué es el MPS?

El **Modelo de Prosperidad Sostenible** es un índice macroeconómico alternativo al PIB per cápita que mide la **prosperidad privada neta** de 163 países entre 2008 y 2026.

A diferencia del PIB, que contabiliza el gasto público como actividad económica positiva, el MPS trata el gasto estatal como lo que es: un **coste sobre la economía productiva**. El resultado es una métrica que captura el daño real del estado sobre la riqueza privada, incluyendo la corrupción, la ineficiencia institucional y el exceso de transferencias.

### Premisa central

El PIB genera **circularidad estadística**: el estado aparece simultáneamente como drenador y como generador de riqueza. El MPS invierte esta lógica: cada euro gastado por el estado es un euro extraído de la economía privada, con un coste adicional de destrucción de incentivos del 18% (deadweight loss).

---

## Fórmulas del modelo

### Carga Oculta (C_H)
```
C_H = (carga_bruta / 10) ^ (1.85 − WJP/10)

carga_bruta = (10−IIJ)×10 + (10−WJP)×10 + (10−Fraser_REG)×10
            + (10−Fraser_SOE)×10 + (10−Fraser_FISCAL)×10
```
Mide la fricción institucional invisible. El exponente dinámico amplifica geométricamente el daño cuando el estado de derecho es débil.

### Efectividad Real de la Inversión (ERI)
```
ERI = Inversión_pública% / C_H
```
Ratio entre lo que el estado invierte y su propio nivel de corrupción. ERI > 1 indica inversión eficiente.

### Carga Parasitaria Total (TPL)
```
TPL = G_cons^(2−WGI) + √G_trans + C_H
      × (1 − ERI_norm × 0.5)
```
Suma el coste directo del aparato estatal, el peso amortiguado de las transferencias y la fricción institucional oculta. El ERI mitiga la carga proporcionalmente a la eficiencia inversora.

### Prosperidad Neta (PN)
```
PN = 100 − (TPL × 1.18)
```
Stock de prosperidad privada tras descontar el coste del estado. **PN positiva = economía viable. PN negativa = hipoteca generacional.**

### Subsidio Exterior (S_E)
```
S_E% = ((Importaciones − Exportaciones) + ODA + Remesas) / PIB × 100
```
Corrige por flujos externos. S_E positivo = país subsidiado. S_E negativo = país donante neto.

### Prosperidad Sostenible (PS)
```
PS = PN + S_E%
```

### Prosperidad Sostenible Ajustada (PSA)
```
PSA = PN − 1.18 × (Inflación/100)² × 100
```

### Valor Nominal Ajustado (VNA)
```
VNA = PIB_nominal × (PSA / 100)
```

---

## Clasificación de países

| Grupo | Rango PN | Descripción |
|-------|----------|-------------|
| 🟢 **A** | > −500 | Economías comparables — núcleo del análisis cuantitativo |
| 🟡 **B** | −5.000 a −500 | Drenaje severo — hipoteca generacional visible |
| 🔴 **C** | < −5.000 | Colapso institucional — estado como cleptocracia |

---

## Resultados principales

- **R² = 0.61** entre TPL y ln(PIB per cápita) — validación empírica sobre 163 países
- **163 países** analizados con serie completa 2008-2026
- **2024-2026** proyectados mediante regresión lineal sobre tendencias históricas
- Taiwán, Suiza y EEUU lideran el ranking de Prosperidad Neta en 2026
- Francia, Noruega y Países Bajos registran la mayor presión parasitaria relativa entre economías avanzadas

---

## Fuentes de datos

| Variable | Fuente |
|----------|--------|
| G_cons% (gasto de consumo) | FMI — Government Final Consumption Expenditure |
| G_trans% (transferencias) | Banco Mundial — Social Protection & Labor |
| WGI (efectividad gubernamental) | Banco Mundial — Worldwide Governance Indicators |
| IIJ (integridad institucional) | Fraser Institute + Transparency International CPI |
| WJP (estado de derecho) | World Justice Project Rule of Law Index |
| Fraser REG / SOE / FISCAL | Fraser Institute — Economic Freedom of the World |
| S_E (subsidio exterior) | FMI BPM6 / Banco Mundial Net ODA Received |
| PIB nominal | FMI — World Economic Outlook Database |

---

## Estructura del repositorio

```
MODELO-PROSPERIDAD-SOSTENIBLE/
│
├── app_mps.py                    # Dashboard Streamlit (punto de entrada)
├── mps_pipeline.py               # Pipeline de cálculo y proyección
├── requirements.txt
├── README.md
│
├── scripts/                      # Calculadores individuales
│   ├── calculador_C_H.py
│   ├── calcularTPL.py
│   ├── calculador_PN.py
│   ├── calcularps.py
│   ├── CalcularPSA.py
│   ├── calcularVNA.py
│   └── calcularS_E.py
│
└── output_mps/                   # Datos generados por el pipeline
    ├── MPS_matriz_completa_*.json       # 163 países × 2008-2026
    ├── MPS_alertas_*.json               # Alertas de deterioro estructural
    ├── MPS_rankings_*.json              # Rankings por PN, TPL, ERI
    ├── MPS_interdependencia_*.json      # Tipos de dependencia estructural
    └── MPS_resumen_ejecutivo_*.json     # Resumen para paper académico
```

---

## Instalación y uso

### Requisitos
- Python 3.10+
- pip

### Instalación

```bash
git clone https://github.com/pedroandresarandamuoz-wq/MODELO-PROSPERIDAD-SOSTENIBLE.git
cd MODELO-PROSPERIDAD-SOSTENIBLE
pip install -r requirements.txt
```

### Lanzar el dashboard

```bash
streamlit run app_mps.py
```

El dashboard se abre automáticamente en `http://localhost:8501`

### Regenerar los datos (opcional)

Si quieres recalcular la matriz desde cero con tus propios datos:

```bash
python mps_pipeline.py
```

Los JSON de entrada deben estar en la raíz del proyecto:
- `Base_Datos_MPS_Definitiva.json`
- `almacen_datos_maestro.json`
- `ch_calculado.json`
- `S_E.json`
- `interdependencia.json`

---

## Notas metodológicas

**Proyecciones 2024-2026:** Las variables fiscales se proyectan mediante regresión lineal sobre la serie 2008-2023. Las variables institucionales (IIJ, WJP, Fraser) se proyectan como media móvil de los últimos 3 años. Los intervalos de confianza son al 80%.

**PN negativas extremas:** Valores como Libia (−1.300.000) no son errores numéricos. Son la consecuencia deliberada del diseño: `G_cons^(2−WGI)` con WGI muy negativo produce exponentes superiores a 2, reflejando matemáticamente que un estado con gobernanza destructiva amplifica el daño de forma no lineal. El modelo no tiene techo porque el parasitismo estatal tampoco lo tiene.

**Países con saltos bruscos 2023→2024:** Ucrania, Luxemburgo y Guinea presentan variaciones grandes por tendencias pronunciadas en los últimos años de la serie histórica. Se recomienda interpretarlos con cautela.

---

## Licencia

Este trabajo es de autoría de **Pedro Andrés Aranda Muñoz** y se publica bajo licencia **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

Puedes usar, compartir y adaptar este trabajo siempre que cites al autor original.

---

## Cita académica

```
Aranda Muñoz, P.A. (2026). Modelo de Prosperidad Sostenible (MPS):
Una métrica alternativa al PIB para medir el coste real del estado
sobre la economía privada. Análisis de 163 países, 2008-2026.
https://github.com/pedroandresarandamuoz-wq/MODELO-PROSPERIDAD-SOSTENIBLE
```
