from fastapi import FastAPI, Depends, HTTPException, Query
from routes import maestros, materias, horarios
from dotenv import load_dotenv
import os

API_KEY =  os.getenv("API_KEY")  # Define tu API Key aquí

async def verify_api_key(api_key: str = Query(...)):
    """
    Verifica que la API Key enviada como parámetro en la URL sea válida.
    """
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# Instancia de FastAPI
app = FastAPI()

# Registrar rutas con dependencia para verificar API Key
app.include_router(maestros.router, prefix="/maestros", dependencies=[Depends(verify_api_key)], tags=["Maestros"])
app.include_router(materias.router, prefix="/materias", dependencies=[Depends(verify_api_key)], tags=["Materias"])
app.include_router(horarios.router, prefix="/horarios", dependencies=[Depends(verify_api_key)], tags=["Horarios"])

# Ruta principal
@app.get("/")
async def root():
    return {"message": "API de Gestión Escolar"}
