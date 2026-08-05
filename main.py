from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime
import time
import os

# --- 1. CONFIGURACIÓN DE BASE DE DATOS ---
# Leemos la URL de conexión desde el docker-compose.yml
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin123@db:5432/superresolucion_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definimos cómo se verá nuestra tabla en la base de datos
class RegistroInferencia(Base):
    __tablename__ = "historial_procesamiento"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_archivo = Column(String)
    modelo_utilizado = Column(String)
    tiempo_segundos = Column(Float)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

# Creamos la tabla automáticamente si no existe
Base.metadata.create_all(bind=engine)

# Función para abrir y cerrar la conexión a la BD en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 2. CONFIGURACIÓN DE LA API ---
app = FastAPI(title="API de Superresolución Satelital con Base de Datos")

def cargar_modelo(tipo_modelo: str):
    print(f"Cargando pesos para el modelo {tipo_modelo}...")
    return True 

@app.on_event("startup")
async def startup_event():
    app.state.modelo_swinir = cargar_modelo("SwinIR")
    app.state.modelo_edsr = cargar_modelo("EDSR")

@app.get("/")
def home():
    return {"mensaje": "Servidor Activo y Base de Datos Conectada."}

@app.post("/super-resolve/")
async def procesar_imagen(
    modelo: str = "SwinIR", 
    file: UploadFile = File(...),
    db: Session = Depends(get_db) # Inyectamos la conexión a la base de datos aquí
):
    inicio = time.time()
    contenido_imagen = await file.read()
    
    # Simulación de inferencia
    time.sleep(1.5) 
    tiempo_total = round(time.time() - inicio, 2)
    
    # --- 3. GUARDAR EN LA BASE DE DATOS ---
    nuevo_registro = RegistroInferencia(
        nombre_archivo=file.filename,
        modelo_utilizado=modelo,
        tiempo_segundos=tiempo_total
    )
    db.add(nuevo_registro)
    db.commit() # Confirmamos el guardado
    db.refresh(nuevo_registro) # Refrescamos para obtener el ID asignado
    
    return JSONResponse(content={
        "id_registro_bd": nuevo_registro.id,
        "archivo": file.filename,
        "modelo": modelo,
        "estado": "Procesamiento exitoso y guardado en PostgreSQL",
        "tiempo_segundos": tiempo_total
    })