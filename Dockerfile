# 1. Usamos una imagen oficial de Python ligera como base
FROM python:3.10-slim

# 2. Le decimos a Docker en qué carpeta interna va a trabajar
WORKDIR /app

# 3. Copiamos el archivo de requerimientos al contenedor
COPY requirements.txt .

# 4. Instalamos las librerías sin guardar caché para que la imagen sea más ligera
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos todo el código de nuestra API (main.py) dentro del contenedor
COPY . .

# 6. Exponemos el puerto 8000 para poder acceder desde nuestro navegador
EXPOSE 8000

# 7. El comando exacto para iniciar el servidor cuando el contenedor arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]