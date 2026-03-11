from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import io

app = FastAPI()

# Esto es VITAL: Si no está, el navegador bloquea la respuesta por seguridad (CORS)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.post("/procesar-csv")
async def procesar_csv(file: UploadFile = File(...), columna: str = Form(...)):
	try:
		# 1. Leer el archivo
		contents = await file.read()
		filename = (file.filename or "").lower()

		# Intentar leer según tipo de archivo con tolerancia de codificación/separador
		if filename.endswith((".xlsx", ".xls")):
			df = pd.read_excel(io.BytesIO(contents))
		else:
			df = None
			for encoding in ["utf-8", "latin-1", "cp1252"]:
				try:
					texto = contents.decode(encoding)
					df = pd.read_csv(io.StringIO(texto), sep=None, engine="python")
					break
				except Exception:
					continue

			if df is None:
				try:
					df = pd.read_excel(io.BytesIO(contents))
				except Exception as exc:
					raise HTTPException(status_code=400, detail=f"No se pudo leer el archivo: {str(exc)}")

		# 2. Limpiar nombres de columnas (Quita espacios y convierte a minúsculas para facilitar)
		# Así si escribes "income" o "Income" funcionará igual
		df.columns = df.columns.str.strip()
		columna_buscada = columna.strip()

		# Búsqueda flexible de columna (ignora mayúsculas/minúsculas)
		mapa_columnas = {str(col).strip().casefold(): str(col) for col in df.columns}
		columna_real = mapa_columnas.get(columna_buscada.casefold())

		if not columna_real:
			return {
				"error": f"Columna '{columna_buscada}' no encontrada.",
				"sugerencias": list(df.columns)[:5],
			}

		# 3. Convertir a números y limpiar
		datos_sucios = pd.to_numeric(df[columna_real], errors="coerce").dropna()
		datos = datos_sucios.values

		if len(datos) < 2:
			return {"error": "La columna seleccionada no tiene suficientes datos numéricos."}

		# 4. Cálculos NumPy (Lo que pide el profesor)
		return {
			"status": "success",
			"variable": columna_real,
			"n": int(len(datos)),
			"media": round(float(np.mean(datos)), 4),
			"desv": round(float(np.std(datos, ddof=1)), 4),
			"min": float(np.min(datos)),
			"max": float(np.max(datos)),
		}

	except Exception as e:
		return {"error": f"Error interno en el servidor: {str(e)}"}
