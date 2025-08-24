# Knowlers Scraper API

API de web scraping para la plataforma Knowlers que permite realizar consultas de personas por DNI o nombre completo.

## Características

- 🔐 Autenticación automática en Knowlers
- 🆔 Búsqueda por DNI
- 👤 Búsqueda por nombre completo
- 🌐 API REST con endpoints JSON
- 🖥️ Interfaz web para pruebas
- ☁️ Listo para desplegar en Railway

## Endpoints de la API

### Autenticación

#### POST `/api/scraper/login`
Inicia sesión en Knowlers.

**Body:**
```json
{
  "username": "tu_usuario",
  "password": "tu_contraseña"
}
```

**Respuesta:**
```json
{
  "message": "Login exitoso",
  "logged_in": true
}
```

#### POST `/api/scraper/logout`
Cierra la sesión y libera recursos.

**Respuesta:**
```json
{
  "message": "Sesión cerrada exitosamente"
}
```

### Consultas

#### POST `/api/scraper/search/dni`
Busca información por DNI.

**Body:**
```json
{
  "dni": "12345678"
}
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "DNI": "12345678",
    "Nombres": "JUAN CARLOS",
    "Apellido Paterno": "PEREZ",
    "Apellido Materno": "GARCIA",
    "Fecha Nacimiento": "01/01/1990",
    "Padre": "CARLOS PEREZ",
    "Madre": "MARIA GARCIA",
    "Direccion": "AV. EJEMPLO 123"
  },
  "timestamp": 1640995200
}
```

#### POST `/api/scraper/search/name`
Busca información por nombre completo.

**Body:**
```json
{
  "nombres": "JUAN CARLOS",
  "apellido_paterno": "PEREZ",
  "apellido_materno": "GARCIA"
}
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "DNI": "12345678",
    "Nombres": "JUAN CARLOS",
    "Apellido Paterno": "PEREZ",
    "Apellido Materno": "GARCIA",
    "Fecha Nacimiento": "01/01/1990",
    "Padre": "CARLOS PEREZ",
    "Madre": "MARIA GARCIA",
    "Direccion": "AV. EJEMPLO 123"
  },
  "timestamp": 1640995200
}
```

### Estado

#### GET `/api/scraper/status`
Verifica el estado del scraper.

**Respuesta:**
```json
{
  "status": "active",
  "logged_in": true,
  "driver_active": true
}
```

## Instalación Local

1. Clona el repositorio
2. Instala las dependencias:
   ```bash
   cd knowlers-scraper
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Instala Chrome y ChromeDriver
4. Ejecuta la aplicación:
   ```bash
   python src/main.py
   ```
5. Abre http://localhost:5000 en tu navegador

## Despliegue en Railway

1. Conecta tu repositorio a Railway
2. Railway detectará automáticamente la configuración
3. La aplicación se desplegará con Chrome y ChromeDriver incluidos

## Variables de Entorno

- `PORT`: Puerto de la aplicación (por defecto: 5000)
- `CHROME_BIN`: Ruta del binario de Chrome (automático en Railway)
- `CHROMEDRIVER_PATH`: Ruta del ChromeDriver (automático en Railway)

## Uso

1. Inicia sesión usando el endpoint `/api/scraper/login`
2. Realiza consultas usando los endpoints de búsqueda
3. Cierra sesión cuando termines usando `/api/scraper/logout`

## Interfaz Web

La aplicación incluye una interfaz web en la ruta raíz (`/`) que permite:
- Iniciar/cerrar sesión
- Realizar búsquedas por DNI
- Realizar búsquedas por nombre
- Ver resultados en tiempo real

## Consideraciones

- Requiere credenciales válidas de Knowlers
- Las consultas consumen créditos en la plataforma Knowlers
- El scraper respeta los términos de uso de Knowlers
- Incluye manejo de errores y timeouts

## Tecnologías

- Flask (API REST)
- Selenium (Web Scraping)
- Chrome/ChromeDriver (Navegador)
- Railway (Despliegue)

