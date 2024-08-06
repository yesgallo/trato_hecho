
# Trato Hecho Web Application

Este es un proyecto web basado en el juego "Deal or No Deal" utilizando Flask, SQLAlchemy y Flask-Login.

## Requisitos

- Python 3.7+
- pip (gestor de paquetes de Python)
- Virtualenv (opcional, pero recomendado)

## Instalación

1. Clona el repositorio:

    ```bash
    git clone https://github.com/yesgallo/TratoHecho.git
    cd tu_repositorio
    ```

2. Crea un entorno virtual:

    ```bash
    python -m venv venv
    ```

3. Activa el entorno virtual:

    - En macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

    - En Windows:
        ```bash
        venv\Scripts\activate
        ```

4. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

5. Configura las variables de entorno creando un archivo `.env` en el directorio raíz del proyecto con el siguiente contenido:

    ```plaintext
    SECRET_KEY=your_secret_key
    SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite3
    ```

6. Inicia la base de datos:

    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

7. Ejecuta la aplicación:

    ```bash
    flask run
    ```

## Uso

- Accede a la aplicación en tu navegador web en `http://localhost:5000`.
- Regístrate e inicia sesión para comenzar a jugar.

## Estructura del Proyecto

trato_hecho/
    app/ 
        __init__.py
        auth.py
        models.py
        views.py
        static/
        templates/
    instance/
    test/
    venv/
    config.py
    game.py
    README.md
    requirements.txt
    run.py



## Licencia

Programación - Desarrollo de Sofware - 2º año - ISFDyT Nº 27
>>>>>>> develop
