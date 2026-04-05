# 📝 Inscriptions API

Este proyecto es una API RESTful desarrollada con Django y Django Rest Framework para la gestión de inscripciones de personas o grupos a eventos, cursos u otras actividades.

## 🚀 Características

- Gestión de personas y grupos
- Registro de inscripciones
- Carga de vouchers como comprobante de inscripción
- API con autenticación por token (JWT)
- Filtros y paginación en las consultas
- Panel de administración Django para gestión manual

## 🛠️ Tecnologías utilizadas

- Python 3.10+
- Django 4.x
- Django Rest Framework
- PostgreSQL
- djangorestframework-simplejwt
- django-filter

## 📦 Instalación

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/tu-usuario/inscriptions-backend.git
   cd inscriptions-backend
   ```

2. **Crea un entorno virtual y actívalo:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configura el archivo `.env`:**

   Crea un archivo `.env` en la raíz con las siguientes variables:

   ```
   SECRET_KEY=tu_clave_secreta
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=postgres://usuario:contraseña@localhost:5432/inscriptions_db
   ```

5. **Aplica las migraciones y crea un superusuario:**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Inicia el servidor de desarrollo:**

   ```bash
   python manage.py runserver
   ```

## Comandos Personalizados

```bash
python manage.py seed_data.py
```

## 📋 Endpoints principales

| Método | Ruta                | Descripción                     |
| ------ | ------------------- | ------------------------------- |
| GET    | /api/persons/       | Lista de personas registradas   |
| POST   | /api/inscriptions/  | Registrar una nueva inscripción |
| POST   | /api/token/         | Obtener token JWT               |
| POST   | /api/token/refresh/ | Refrescar token JWT             |

> Puedes encontrar toda la documentación de la API accediendo a `/swagger/` si se habilitó drf-yasg o `/api/` si se usa el navegador de DRF.

## 🧪 Pruebas

Para ejecutar pruebas automatizadas:

```bash
python manage.py test
```

## 🗃️ Estructura del proyecto

```
inscriptions/
├── apps/
│ ├── activity/
│ ├── inscription/
│ ├── kenani/ # Conectores o modelos externos (inspectdb)
│ ├── person/
│ ├── seed/ # Scripts o datos iniciales
│ ├── user/ # Gestión de usuarios
│ └── init.py
├── core/ # Configuración principal del proyecto (settings, urls, wsgi, etc.)
├── venv/ # Entorno virtual
├── .env # Variables de entorno
├── .gitignore
├── delete.py # Script personalizado (uso temporal o mantenimiento)
├── init_data.json # Datos de ejemplo para carga inicial
├── manage.py
├── README.md
└── requirements.txt
```

## ✅ TODOs

- [ ] Implementar sistema de notificaciones por correo
- [ ] Agregar validaciones para fechas límite de inscripción
- [ ] Mejorar documentación OpenAPI (Swagger)

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## CI Demo Deploy (root script)

This repository includes `deploy/deploy_jni_demo_backend.sh` as the server-side deploy script used by GitHub Actions.

### Server setup (one time)

1. Copy script to root path:

```bash
sudo install -o root -g root -m 750 deploy/deploy_jni_demo_backend.sh /usr/local/bin/deploy_jni_demo_backend.sh
```

2. Allow `tsi` to run only this script without password:

```bash
echo 'tsi ALL=(root) NOPASSWD: /usr/local/bin/deploy_jni_demo_backend.sh' | sudo tee /etc/sudoers.d/jni-demo-deploy
sudo visudo -cf /etc/sudoers.d/jni-demo-deploy
```

3. Manual test as `tsi`:

```bash
sudo -n /usr/local/bin/deploy_jni_demo_backend.sh codexdeploy
```

The workflow `.github/workflows/build_deploy.yml` calls this command remotely over SSH.

### Important after script updates

If `deploy/deploy_jni_demo_backend.sh` changes in git, reinstall it to root path:

```bash
cd /home/tsi/dl/jni-inscriptions-demo/django_inscriptions
sudo install -o root -g root -m 750 deploy/deploy_jni_demo_backend.sh /usr/local/bin/deploy_jni_demo_backend.sh
```

The GitHub Action executes `/usr/local/bin/deploy_jni_demo_backend.sh`, not the repository copy directly.
