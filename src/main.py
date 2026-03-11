from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI(title="API de Créditos 2025")

# Configuración de CORS para permitir la conexión con el HTML local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/procesar-datos")
async def procesar_datos(file: UploadFile = File(...)):
    try:
        # 1. Leer el archivo Excel
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # 2. PROCESO DE LIMPIEZA PROFESIONAL
        duplicados_antes = int(df.duplicated().sum())
        
        # Normalizar nombres de columnas (minúsculas y sin espacios)
        df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
        
        # Eliminar duplicados y filas sin ID crítico
        df = df.drop_duplicates()
        if 'id_credit' in df.columns:
            df = df.dropna(subset=['id_credit'])
        
        # 3. Preparar los resultados para la interfaz
        # Usamos .get() para evitar errores si la columna no existe en el Excel
        return {
            "variables_analizadas": len(df.columns),
            "completitud": f"{int(df.notnull().mean().mean() * 100)}%",
            "duplicados": duplicados_antes,
            "columnas_lista": ", ".join(df.columns.tolist()),
            "promedios": {
                "score": float(df['score_1'].mean()) if 'score_1' in df.columns else 0,
                "ingresos": float(df['income'].mean()) if 'income' in df.columns else 0,
                "solicitado": float(df['cupo_solicitado'].mean()) if 'cupo_solicitado' in df.columns else 0
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

# Endpoint adicional para la Semana 4 (opcional)
@app.get("/health")
def check_health():
    return {"status": "online", "version": "2025.1"}