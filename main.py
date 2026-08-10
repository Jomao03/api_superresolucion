from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime
import time
import os
import onnxruntime as ort
import numpy as np
from PIL import Image
import io
import os

# --- CONFIGURACIÓN DE BASE DE DATOS ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin123@db:5432/superresolucion_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RegistroInferencia(Base):
    __tablename__ = "historial_procesamiento"
    id = Column(Integer, primary_key=True, index=True)
    nombre_archivo = Column(String)
    modelo_utilizado = Column(String)
    tiempo_segundos = Column(Float)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- CONFIGURACIÓN DE LA API Y ONNX ---
app = FastAPI(title="API de Superresolución Satelital con ONNX")

# Carga segura del modelo
ruta_modelo = "modelo_optimizado.onnx"
if os.path.exists(ruta_modelo):
    sesion_onnx = ort.InferenceSession(ruta_modelo)
    print("Modelo ONNX cargado exitosamente.")
else:
    sesion_onnx = None
    print("⚠️ ADVERTENCIA: No se encontró el modelo ONNX. Debes generarlo.")

@app.get("/")
def home():
    return {"mensaje": "Servidor Activo, Base de Datos Conectada y Modelo ONNX Cargado."}

@app.post("/super-resolve/")
async def procesar_imagen(
    modelo: str = "SwinIR", 
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    inicio = time.time()
    contenido_imagen = await file.read()
    
    # 1. Preprocesamiento: Convertir bytes a matriz matemática (Tensor)
    imagen = Image.open(io.BytesIO(contenido_imagen)).convert('RGB')
    imagen = imagen.resize((256, 256)) # Redimensionar a lo que espera el modelo
    input_data = np.array(imagen).astype(np.float32) / 255.0 # Normalizar entre 0 y 1
    input_data = np.transpose(input_data, (2, 0, 1)) # Cambiar formato de HWC a CHW
    input_data = np.expand_dims(input_data, axis=0) # Añadir dimensión de Batch Size (1, 3, 256, 256)
    
    # 2. Inferencia Real con ONNX Runtime
    nombre_entrada = sesion_onnx.get_inputs()[0].name
    resultado = sesion_onnx.run(None, {nombre_entrada: input_data})
    
    # El resultado[0] contiene la matriz de la imagen de salida procesada.
    # Por ahora solo registraremos el éxito de la operación y el tiempo.
    
    tiempo_total = round(time.time() - inicio, 2)
    
    # 3. Guardar en Base de Datos
    nuevo_registro = RegistroInferencia(
        nombre_archivo=file.filename,
        modelo_utilizado=f"{modelo} (Optimizado ONNX)",
        tiempo_segundos=tiempo_total
    )
    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)
    
    return JSONResponse(content={
        "id_registro_bd": nuevo_registro.id,
        "archivo": file.filename,
        "modelo": f"{modelo} (Optimizado ONNX)",
        "estado": "Inferencia matemática exitosa",
        "tiempo_segundos": tiempo_total,
        "forma_salida_tensor": str(resultado[0].shape)
    })