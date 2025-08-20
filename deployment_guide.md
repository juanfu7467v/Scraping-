# Guía de Despliegue en Railway

## Pasos para desplegar el Knowlers Scraper API en Railway

### 1. Preparación del Repositorio

1. Sube el código a un repositorio de GitHub
2. Asegúrate de que todos los archivos estén incluidos:
   - `src/` (código fuente)
   - `requirements.txt` (dependencias)
   - `railway.json` (configuración de Railway)
   - `nixpacks.toml` (configuración de Nixpacks)
   - `Procfile` (comando de inicio)
   - `README.md` (documentación)

### 2. Configuración en Railway

1. Ve a [railway.app](https://railway.app)
2. Inicia sesión con tu cuenta de GitHub
3. Haz clic en "New Project"
4. Selecciona "Deploy from GitHub repo"
5. Elige tu repositorio con el código del scraper

### 3. Variables de Entorno (Opcional)

Railway configurará automáticamente:
- `PORT`: Puerto de la aplicación
- `CHROME_BIN`: Ruta del binario de Chrome
- `CHROMEDRIVER_PATH`: Ruta del ChromeDriver

### 4. Despliegue Automático

Railway detectará automáticamente:
- El archivo `nixpacks.toml` para instalar Chrome y ChromeDriver
- El archivo `requirements.txt` para instalar dependencias de Python
- El comando de inicio desde `railway.json` o `Procfile`

### 5. Verificación del Despliegue

1. Una vez desplegado, Railway te proporcionará una URL pública
2. Visita la URL para acceder a la interfaz web
3. Prueba el endpoint de estado: `https://tu-app.railway.app/api/scraper/status`

### 6. Uso de la API

#### Endpoints disponibles:

- `POST /api/scraper/login` - Iniciar sesión
- `POST /api/scraper/logout` - Cerrar sesión
- `POST /api/scraper/search/dni` - Buscar por DNI
- `POST /api/scraper/search/name` - Buscar por nombre
- `GET /api/scraper/status` - Estado del scraper

#### Ejemplo de uso:

```bash
# Iniciar sesión
curl -X POST https://tu-app.railway.app/api/scraper/login \
  -H "Content-Type: application/json" \
  -d '{"username": "tu_usuario", "password": "tu_contraseña"}'

# Buscar por DNI
curl -X POST https://tu-app.railway.app/api/scraper/search/dni \
  -H "Content-Type: application/json" \
  -d '{"dni": "12345678"}'
```

### 7. Monitoreo

- Railway proporciona logs en tiempo real
- Puedes ver el estado de la aplicación en el dashboard
- El endpoint `/api/scraper/status` permite verificar el estado del scraper

### Notas Importantes

- La aplicación incluye Chrome y ChromeDriver automáticamente
- El scraper funciona en modo headless (sin interfaz gráfica)
- Requiere credenciales válidas de Knowlers para funcionar
- Las consultas consumen créditos en la plataforma Knowlers

