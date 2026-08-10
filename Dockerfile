FROM python:3.10-slim

WORKDIR /app

# 1. Instalamos solo la dependencia matemática paralela necesaria
RUN apt-get update && \
    apt-get install -y libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# 2. Copiamos e instalamos dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copiamos el resto de tu código
COPY . .

# 4. Comando de arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]