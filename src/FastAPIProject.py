# ============================================
# MI API DE ANÁLISIS — EVALUACIÓN CREDITICIA 2025
# Proyecto Personal: Paul Betancour
# ============================================
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional
import numpy as np

# === FASE 2: MODELOS PYDANTIC (Modelos Propios) ===

class SolicitudCreditoInput(BaseModel):
    """Modelo de entrada para análisis de perfil de cliente."""
    cliente_nombre: str = Field(..., min_length=3, description="Nombre del solicitante")
    ingresos_mensuales: List[float] = Field(..., min_items=3, description="Historial de últimos 3 ingresos")
    puntajes_buro: List[int] = Field(..., min_items=4, description="Scores de crédito de diferentes centrales")
    ciudad: str = Field(..., min_length=2)
    comentarios_adicionales: Optional[str] = None

class AnalisisCreditoOutput(BaseModel):
    """Modelo de salida con métricas financieras calculadas."""
    cliente: str
    promedio_ingresos: float
    riesgo_variabilidad: float
    score_promedio: float
    max_capacidad_estimada: float
    estatus_preaprobacion: str

# === FASE 3: LÓGICA DE PROCESAMIENTO (Función Pura) ===

def procesar_analisis_financiero(nombre, ingresos, scores) -> dict:
    ing_arr = np.array(ingresos)
    scr_arr = np.array(scores)
    
    # 5 Cálculos usando NumPy
    avg_ingresos = np.mean(ing_arr)
    std_ingresos = np.std(ing_arr, ddof=1) # Desviación muestral
    avg_score = np.mean(scr_arr)
    capacidad = np.max(ing_arr) * 0.4 # Estimación del 40% del ingreso max
    
    # Lógica de negocio
    estatus = "APROBADO" if avg_score > 600 and avg_ingresos > 2000 else "RECHAZADO"
    
    return {
        "cliente": nombre,
        "promedio_ingresos": round(float(avg_ingresos), 4),
        "riesgo_variabilidad": round(float(std_ingresos), 4),
        "score_promedio": round(float(avg_score), 4),
        "max_capacidad_estimada": round(float(capacidad), 4),
        "estatus_preaprobacion": estatus
    }

# === FASE 4: APP FASTAPI + ENDPOINTS CRUD ===

app = FastAPI(
    title="Sistema de Evaluación Crediticia Paul Betancour",
    description="API para el procesamiento de solicitudes de crédito 2025",
    version="1.5.0"
)

# Base de datos simulada
historial_analisis = {}
id_counter = 1

@app.post("/analizar-perfil", response_model=AnalisisCreditoOutput)
def crear_analisis(datos: SolicitudCreditoInput):
    global id_counter
    # Procesar
    resultado = procesar_analisis_financiero(
        datos.cliente_nombre, 
        datos.ingresos_mensuales, 
        datos.puntajes_buro
    )
    # Persistir
    historial_analisis[id_counter] = resultado
    id_counter += 1
    return resultado

@app.get("/historial-creditos")
def listar_historial():
    return historial_analisis

@app.get("/historial-creditos/{analisis_id}")
def obtener_detalle(analisis_id: int):
    if analisis_id not in historial_analisis:
        raise HTTPException(status_code=404, detail="El registro de crédito no existe")
    return historial_analisis[analisis_id]

@app.delete("/historial-creditos/{analisis_id}")
def eliminar_registro(analisis_id: int):
    if analisis_id not in historial_analisis:
        raise HTTPException(status_code=404, detail="ID no encontrado para eliminar")
    del historial_analisis[analisis_id]
    return {"mensaje": f"Registro {analisis_id} eliminado exitosamente"}
    from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import io

app = FastAPI()

# Configuración CORS para el HTML
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db_historial = {}
id_auto = 1

# FASE 3: Lógica Pura (Independiente)
def calcular_estadisticas_columna(df, columna_nombre):
    if columna_nombre not in df.columns:
        raise ValueError(f"La columna '{columna_nombre}' no existe en el archivo.")
    
    # Limpieza de datos (quitar nulos y asegurar que sea numérico)
    datos = pd.to_numeric(df[columna_nombre], errors='coerce').dropna().values
    
    if len(datos) < 3:
        raise ValueError("No hay suficientes datos numéricos en esta columna.")

    return {
        "variable_analizada": columna_nombre,
        "n": len(datos),
        "media": round(float(np.mean(datos)), 4),
        "desviacion": round(float(np.std(datos, ddof=1)), 4),
        "minimo": float(np.min(datos)),
        "maximo": float(np.max(datos)),
        "suma_total": float(np.sum(datos))
    }

@app.post("/procesar-csv")
async def procesar_csv(
    file: UploadFile = File(...), 
    columna: str = Form(...)
):
    global id_auto
    try:
        # Leer el contenido del archivo subido
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Procesar con la lógica estadística
        resultado = calcular_estadisticas_columna(df, columna)
        
        # Guardar en el historial (Requisito CRUD)
        db_historial[id_auto] = resultado
        id_auto += 1
        
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/historial")
def ver_historial():
    return db_historial

@app.delete("/historial/{item_id}")
def eliminar(item_id: int):
    if item_id in db_historial:
        del db_historial[item_id]
        return {"msg": "Eliminado"}
    raise HTTPException(status_code=404, detail="No encontrado")