from fastapi.testclient import TestClient
from main import app
import io
from PIL import Image

client = TestClient(app)

def test_ruta_principal():
    """Prueba que el servidor responda correctamente en la raíz"""
    response = client.get("/")
    # Solo validamos que el servidor esté vivo y no haya errores internos
    assert response.status_code == 200

def test_procesar_imagen():
    """Prueba que el endpoint de superresolución reciba y procese un archivo real"""
    
    # 1. Creamos la imagen en RAM
    imagen_falsa = Image.new('RGB', (10, 10), color='black')
    buffer = io.BytesIO()
    imagen_falsa.save(buffer, format="PNG")
    
    # 2. EL TRUCO: Usamos buffer.getvalue() para enviarle los bytes puros a la API
    archivos = {"file": ("imagen_prueba.png", buffer.getvalue(), "image/png")}
    
    # 3. Hacemos la petición POST al modelo
    response = client.post("/super-resolve/?modelo=EDSR", files=archivos)
    
    # 4. Validamos que la respuesta sea un éxito
    assert response.status_code == 200
    datos = response.json()
    
    # 5. Comprobamos la estructura del JSON
# 5. Comprobamos la estructura del JSON
    assert "id_registro_bd" in datos
    assert datos["modelo"] == "EDSR (Optimizado ONNX)"  # <- Aquí está el ajuste
    assert datos["archivo"] == "imagen_prueba.png"