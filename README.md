# 📊 Sistema de Gestión de Microcréditos 2025 - API de Procesamiento

![Python](https://img.shields.io/badge/Python-3.11.9-blue)
![Framework](https://img.shields.io/badge/Framework-Flask-green)
![Data](https://img.shields.io/badge/Library-Pandas-orange)

## 📝 Introducción
Este proyecto forma parte del curso **PYTHON PARA DESARROLLO DE APIS E INTELIGENCIA ARTIFICIAL**. Se enfoca en el procesamiento, validación y limpieza de datos de microcréditos para personas naturales, utilizando un pipeline modular y servicios web.

## 📉 Análisis Descriptivo del Dataset
El dataset contiene información crítica de solicitantes, incluyendo:
* **Demográficos:** Edad, Ciudad, Actividad laboral.
* **Financieros:** Ingresos, Experiencia bancaria, Cupos solicitados vs. aprobados.
* **Riesgo:** 4 niveles de Score crediticio y comportamiento histórico.

### Hallazgos Principales:
- **Ratio de Aprobación:** Se observa una correlación directa entre el `score_4` y la aprobación del cupo.
- **Calidad de Datos:** Se identificaron valores nulos en el historial de delincuencia que fueron tratados mediante limpieza automatizada.

## 🚀 Estructura del Proyecto
- `app.py`: Servidor Flask con los endpoints de la API.
- `logic/cleaning.py`: Funciones puras de procesamiento de datos.
- `schemas/models.py`: Validación de datos con Pydantic.
- `data/`: Dataset original y procesado.

## 🛠️ Instalación y Uso
1. Clonar el repo.
2. Crear entorno virtual: `python -m venv venv`.
3. Instalar dependencias: `pip install -r requirements.txt`.
4. Correr la API: `python app.py`.
