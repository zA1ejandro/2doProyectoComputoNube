# ==========================================
# Dockerfile para Django con soporte MariaDB
# ==========================================
FROM python:3.12-slim

# Evitar que Python genere archivos .pyc y activar salida sin búfer en consola
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema requeridas para mysqlclient y herramientas de red
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    mariadb-client \
    netcat-openbsd \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . /app/

# Asegurar permisos de ejecución en el script de entrada
RUN chmod +x /app/entrypoint.sh

# Exponer el puerto 8080 requerido para la aplicación
EXPOSE 8080

# Definir punto de entrada y comando por defecto
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
