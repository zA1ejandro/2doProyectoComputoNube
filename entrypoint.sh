#!/bin/bash
set -e

echo "=========================================================="
echo "           Iniciando Contenedor Django                    "
echo "=========================================================="
echo "Esperando que el servicio MariaDB esté disponible en $DB_HOST:$DB_PORT..."

python << 'EOF'
import os
import sys
import time

try:
    import MySQLdb
except ImportError:
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb

host = os.environ.get('DB_HOST', 'db')
port = int(os.environ.get('DB_PORT', 3306))
user = os.environ.get('DB_USER', 'django_user')
password = os.environ.get('DB_PASSWORD', 'django_password')
database = os.environ.get('DB_NAME', 'mariadb_django')

max_retries = 35
retry_interval = 2

for i in range(1, max_retries + 1):
    try:
        conn = MySQLdb.connect(
            host=host,
            port=port,
            user=user,
            passwd=password,
            db=database,
            connect_timeout=3
        )
        conn.close()
        print(f" Conexión establecida con MariaDB en {host}:{port}/{database}")
        sys.exit(0)
    except Exception as err:
        print(f"[{i}/{max_retries}] MariaDB inicializando ({err}). Reintentando en {retry_interval}s...")
        time.sleep(retry_interval)

print(" Error: No fue posible conectar con MariaDB después de múltiples intentos.")
sys.exit(1)
EOF

echo "Aplicando migraciones a la base de datos MariaDB..."
python manage.py migrate --noinput

echo "Inicializando usuarios de prueba (admin / coca_user)..."
python manage.py init_users

echo "=========================================================="
echo "  Servidor Django listo. Escuchando en el puerto 8080!    "
echo "=========================================================="

exec "$@"
