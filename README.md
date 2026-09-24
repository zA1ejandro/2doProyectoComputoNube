# Proyecto Cloud Computing - Unidad 2: Django & MariaDB en Docker

Aplicación web desarrollada con la **última versión de Django (6.1.x)** conectada a un contenedor de **MariaDB (versión `latest`)**, orquestada completamente mediante **Docker** y **Docker Compose**, ejecutándose en el puerto **8080**, e integrando una interfaz de **inicio de sesión corporativa con el logo de Coca-Cola y fondo blanco**.

---

## 🚀 Características del Proyecto

- **Django**: Última versión estable (`>= 6.1.1`).
- **MariaDB**: Imagen oficial `mariadb:latest` con persistencia de datos mediante volúmenes de Docker.
- **Puerto de Ejecución**: Configurado y expuesto en el puerto **8080** (`http://localhost:8080`).
- **Interfaz de Login (Coca-Cola)**:
  - Diseño limpio sobre **fondo blanco** con el logo oficial vectorizado de **Coca-Cola**.
  - Formulario con campos de **Usuario**, **Password** y botón **Login**.
  - Alternador para ver/ocultar contraseña.
  - Pestaña para **Crear Cuenta (Registro)** directamente en la base de datos MariaDB.
  - Botones de autocompletado rápido para pruebas instantáneas.
- **Página "Hola Mundo"**:
  - Protegida por autenticación con barra de estado del usuario conectado y botón para **Cerrar Sesión**.
  - Verificación en tiempo real del estado de la conexión con MariaDB y su versión real (`SELECT VERSION()`).
  - Prueba de persistencia ORM: contador de visitas almacenadas en MariaDB mediante el modelo `Visit`.
- **Automatización**:
  - Script de inicio `entrypoint.sh` que comprueba activamente la disponibilidad y autenticación en MariaDB antes de iniciar Django.
  - Aplicación automática de migraciones (`python manage.py migrate`).
  - Inicialización automática de usuarios de prueba por defecto (`init_users`).
  - Hot-reloading en desarrollo mediante montaje de volúmenes.

---

## 🔑 Credenciales de Prueba Preconfiguradas

Al iniciar los contenedores, los siguientes usuarios se crean automáticamente en MariaDB para facilitar la prueba:

| Usuario | Password | Rol |
| :--- | :--- | :--- |
| `admin` | `admin123` | **Superusuario / Administrador** |
| `coca_user` | `coca123` | **Usuario estándar** |

*(También puedes registrar nuevos usuarios directamente desde la interfaz en la pestaña "Crear Cuenta")*.

---

## 📁 Estructura del Proyecto

```text
2doProyectoComputoNube/
├── config/                      # Configuración principal de Django
│   ├── __init__.py              # Soporte para conectores MySQL/MariaDB
│   ├── asgi.py                  # Configuración ASGI
│   ├── settings.py              # Variables, base de datos y redirecciones de Login
│   ├── urls.py                  # Enrutador principal de URLs
│   └── wsgi.py                  # Configuración WSGI
├── core/                        # Aplicación Django
│   ├── management/commands/     # Comandos personalizados
│   │   ├── __init__.py
│   │   └── init_users.py        # Generación de usuarios de prueba iniciales
│   ├── migrations/              # Migraciones de base de datos
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── static/core/images/      # Recursos estáticos
│   │   └── coca_cola_logo.svg   # Logo oficial Coca-Cola
│   ├── templates/core/          # Plantillas HTML
│   │   ├── index.html           # Dashboard Hola Mundo y diagnóstico DB
│   │   └── login.html           # Interfaz de Login Coca-Cola (fondo blanco)
│   ├── admin.py                 # Configuración del panel admin
│   ├── apps.py
│   ├── models.py                # Modelo Visit para persistencia ORM
│   ├── urls.py                  # Rutas /, /login/ y /logout/
│   └── views.py                 # Lógica de login, logout y dashboard
├── .dockerignore                # Exclusión de archivos en construcción Docker
├── .env                         # Variables de entorno preconfiguradas
├── .env.example                 # Plantilla de variables de entorno
├── .gitignore                   # Archivos ignorados por Git
├── docker-compose.yml           # Orquestación de servicios web y MariaDB
├── Dockerfile                   # Imagen de la aplicación Django (Python 3.12-slim)
├── entrypoint.sh                # Inicialización, espera de DB y creación de usuarios
├── manage.py                    # Utilidad de administración Django
├── README.md                    # Documentación del proyecto
└── requirements.txt             # Dependencias Python
```

---

## 🛠️ Requisitos Previos

- **Docker** y **Docker Compose** instalados en el sistema.

> [!NOTE]
> Si tu usuario no tiene permisos para acceder al socket de Docker (`/var/run/docker.sock`), puedes agregarlo al grupo `docker` con:
> ```bash
> sudo usermod -aG docker $USER
> newgrp docker
> ```
> O bien anteponer `sudo` a los comandos de docker compose.

---

## ⚡ Cómo Ejecutar el Proyecto

### 1. Iniciar los contenedores

En la raíz del proyecto, ejecuta:

```bash
docker compose up --build
```
*(o `sudo docker compose up --build` si tu usuario requiere permisos de superusuario)*.

Docker:
1. Construirá la imagen de Django y descargará la última versión de MariaDB.
2. Esperará a que MariaDB esté lista y acepte conexiones.
3. Aplicará las migraciones de Django a MariaDB.
4. Creará automáticamente los usuarios `admin` y `coca_user`.
5. Levantará el servidor en el puerto **8080**.

### 2. Acceder a la Interfaz de Login

Abre tu navegador en:

👉 **[http://localhost:8080/](http://localhost:8080/)** o **[http://localhost:8080/login/](http://localhost:8080/login/)**

Verás la interfaz de inicio de sesión con:
- **Fondo blanco y diseño corporativo.**
- **Logo oficial de Coca-Cola.**
- Campos para **Usuario**, **Password** y botón **Login**.
- Botones de autocompletado rápido para ingresar inmediatamente con `admin` o `coca_user`.

### 3. Dashboard "¡Hola Mundo!"

Al iniciar sesión serás redirigido a la página de bienvenida con:
- Barra superior con el nombre del usuario autenticado y botón para **Cerrar Sesión**.
- Diagnóstico en vivo de la conexión con **MariaDB** y su versión.
- Contador interactivo de visitas persistidas en la base de datos.
- Botón para recargar y probar la persistencia.

---

## 🔐 Panel de Administración

Puedes acceder al administrador de Django en:

👉 **[http://localhost:8080/admin/](http://localhost:8080/admin/)**

Inicia sesión con el usuario:
- **Usuario:** `admin`
- **Contraseña:** `admin123`

---

## 🛑 Detener los Contenedores

Para apagar los servicios:

```bash
docker compose down
```

Para apagar y eliminar los volúmenes de MariaDB:

```bash
docker compose down -v
```