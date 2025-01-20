# Proyecto LLM Service - API REST con Hugging Face y FastAPI

Este proyecto proporciona una API REST que permite generar texto usando un modelo de lenguaje preentrenado (GPT-2) y almacenar el historial de las solicitudes generadas. Está implementado en Python utilizando FastAPI y Hugging Face Transformers, con persistencia en base de datos usando SQLAlchemy.

## Tecnologías utilizadas

-   **FastAPI**: Framework web moderno para construir APIs en Python.
-   **Transformers (Hugging Face)**: Modelo GPT-2 para la generación de texto.
-   **SQLAlchemy**: ORM para interactuar con la base de datos.
-   **SQLite**: Base de datos utilizada para la persistencia de las solicitudes.
-   **Passlib**: Biblioteca para el manejo de contraseñas de forma segura (bcrypt).
-   **JWT**: JSON Web Tokens para la autenticación de usuarios.

## Características

-   **Generación de texto**: Permite enviar un prompt y obtener un texto generado utilizando el modelo GPT-2.
-   **Historial de solicitudes**: Guarda el historial de las solicitudes de generación de texto por cada usuario.
-   **Autenticación**: Protección de endpoints con autenticación JWT para generar texto y acceder al historial.
-   **Logging**: Todos los servicios y repositorios importantes están registrados con `logging` para facilitar la depuración y la trazabilidad.

## Endpoints

### `/register` (POST)

-   **Descripción**: Registra un nuevo usuario en el sistema.
-   **Cuerpo de la solicitud**:

    ```json
    {
    	"username": "string",
    	"email": "string",
    	"password": "string"
    }
    ```

-   **Respuesta**:
    ```json
    {
    	"message": "User created successfully",
    	"user": {
    		"id": 1,
    		"username": "string",
    		"email": "string"
    	}
    }
    ```

### `/login` (POST)

-   **Descripción**: Inicia sesión y devuelve un token de acceso JWT.
-   **Cuerpo de la solicitud**:

    ```json
    {
    	"username": "string",
    	"password": "string"
    }
    ```

-   **Respuesta**:
    ```json
    {
    	"access_token": "string",
    	"token_type": "bearer"
    }
    ```

### `/generate` (POST)

-   **Descripción**: Genera texto usando el modelo GPT-2.
-   **Cuerpo de la solicitud**:

    ```json
    {
    	"prompt": "string",
    	"max_length": 100,
    	"temperature": 0.7,
    	"top_p": 0.9
    }
    ```

-   **Respuesta**:
    ```json
    {
    	"prompt": "string",
    	"generated_text": "string"
    }
    ```

### `/history` (GET)

-   **Descripción**: Obtiene el historial de solicitudes realizadas por el usuario autenticado.
-   **Respuesta**:
    ```json
    {
    	"historical_requests": [
    		{
    			"max_length": 50,
    			"id": 1,
    			"top_p": 0.9,
    			"prompt": "hola, hablas español?",
    			"temperature": 1.0,
    			"userId": 1,
    			"generated_text": "hola, hablas español? (F) No.\n\nSACRAMENTO, CA - FEBRUARY 05: San Francisco International Airport (FIA) personnel board an aircraft at the San Francisco International Airport"
    		}
    	]
    }
    ```

## Requisitos

-   Python 3.8 o superior
-   Dependencias de Python definidas en `requirements.txt`

## Instalación

1. Clona este repositorio:

    ```bash
    git clone https://github.com/AAAbduu/Roams-Backend-Developer-AI.git
    cd llm_service
    ```

2. Crea y activa un entorno virtual:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Para Linux/Mac
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Ejecución

Para ejecutar la aplicación en desarrollo:

1. **Correr el servidor**:

    ```bash
    uvicorn app.main:app --reload
    ```

2. La API estará disponible en `http://127.0.0.1:8000`.

3. **Acceder a la documentación interactiva**:
    - Swagger: `http://127.0.0.1:8000/docs`
## Autenticación

La API requiere autenticación JWT para los endpoints que permiten generar texto y acceder al historial. Puedes obtener el token de acceso mediante el endpoint `/login` después de registrarte.

## Logs

Todos los eventos importantes, como la creación de usuarios, la generación de texto y los errores, se registran usando el módulo `logging`. Los logs se pueden ver en la consola o se pueden configurar para ser almacenados en un archivo.

## Pruebas (Testing)

Aunque no se solicitó explícitamente en el enunciado del proyecto, es esencial implementar pruebas unitarias y de integración para asegurar la calidad y estabilidad del sistema. A continuación, se describen los tipos de pruebas que serían importantes en este proyecto y algunos ejemplos de cómo podrían implementarse.

### Tipos de Pruebas

1. **Pruebas Unitarias**: Estas pruebas se enfocan en unidades pequeñas e individuales del código, como funciones o métodos. Son cruciales para verificar que las funcionalidades de las clases y servicios estén funcionando correctamente de forma aislada. Por ejemplo:
   - Verificar que la función `generate_text` retorne el texto generado correctamente.
   - Validar que la función `create_user` maneje correctamente los errores de duplicados.

2. **Pruebas de Integración**: Estas pruebas verifican que los diferentes componentes del sistema (como servicios y repositorios) funcionen bien juntos. Aseguran que los endpoints de la API interactúan correctamente con la base de datos y los servicios:
   - Verificar que el endpoint `/register` registre correctamente un usuario en la base de datos.
   - Verificar que el endpoint `/generate` genere texto utilizando el modelo GPT-2.

3. **Pruebas de Endpoint (Pruebas de API)**: Estas pruebas aseguran que los endpoints RESTful proporcionen las respuestas correctas, incluyendo el manejo adecuado de errores y la validación de datos. Aseguran que la API cumpla con los requisitos del proyecto:
   - Verificar que los endpoints como `/login` y `/history` devuelvan respuestas correctas para solicitudes válidas y gestionen adecuadamente los errores para solicitudes inválidas.
