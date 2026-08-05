from fastapi.testclient import TestClient
from main import app

# Creamos un cliente de pruebas que simula ser un navegador/usuario
client = TestClient(app)

def test_ruta_principal():
    """Prueba que el servidor responda correctamente en la raíz"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "Servidor Activo y Base de Datos Conectada."}

def test_procesar_imagen():
    """Prueba que el endpoint de superresolución reciba y procese un archivo"""
    # Creamos un archivo falso en memoria para no tener que subir uno real
    archivo_falso = b"contenido de imagen simulada"
    archivos = {"file": ("imagen_prueba.png", archivo_falso, "image/png")}
    
    # Hacemos la petición POST simulando el envío
    response = client.post("/super-resolve/?modelo=EDSR", files=archivos)
    
    # Validamos que la respuesta sea correcta
    assert response.status_code == 200
    datos = response.json()
    
    # Comprobamos que el JSON tenga la estructura que programamos
    assert "id_registro_bd" in datos
    assert datos["modelo"] == "EDSR"
    assert datos["archivo"] == "imagen_prueba.png"