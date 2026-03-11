from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io

app = FastAPI()

@app.post("/procesar-datos")
async def procesar_datos(file: UploadFile = File(...)):
    # Leer el archivo subido
    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents))
    
    # 1. Limpieza básica (lo que ya tienes)
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    duplicados_iniciales = df.duplicated().sum()
    df = df.drop_duplicates()
    
    # 2. Generar estadísticas para el HTML
    stats = {
        "variables_analizadas": len(df.columns),
        "completitud": f"{int(df.notnull().mean().mean() * 100)}%",
        "duplicados": int(duplicados_iniciales),
        "promedios": {
            "score": float(df['score_1'].mean()) if 'score_1' in df.columns else 0,
            "ingresos": float(df['income'].mean()) if 'income' in df.columns else 0,
            "solicitado": float(df['cupo_solicitado'].mean()) if 'cupo_solicitado' in df.columns else 0
        },
        "columnas_lista": ", ".join(df.columns.tolist())
    }
    
    return stats