# Usa una imagen oficial de Python compatible
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia todos los archivos a la imagen
COPY . .

# Instala las dependencias del sistema necesarias para matplotlib
RUN apt-get update && apt-get install -y \
    gcc g++ \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que usa Flask
EXPOSE 5000

# Ejecuta la aplicación Flask
CMD ["python", "visual_app.py"]
