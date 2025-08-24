from flask import Blueprint, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json

scraper_bp = Blueprint('scraper', __name__)

class KnowlersScraper:
    def __init__(self):
        self.driver = None
        self.is_logged_in = False
        
    def setup_driver(self):
        """Configura el driver de Chrome para el scraping"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--disable-javascript')
        
        # Configuración para Railway
        import os
        chrome_bin = os.environ.get('CHROME_BIN')
        chromedriver_path = os.environ.get('CHROMEDRIVER_PATH')
        
        if chrome_bin:
            chrome_options.binary_location = chrome_bin
        
        try:
            if chromedriver_path:
                self.driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
            else:
                self.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Error configurando Chrome: {e}")
            # Fallback para desarrollo local
            self.driver = webdriver.Chrome(options=chrome_options)
            
        return self.driver
    
    def login(self, username, password):
        """Inicia sesión en Knowlers"""
        try:
            if not self.driver:
                self.setup_driver()
                
            self.driver.get("https://dashboard.knowlers.app/personas/consulta")
            
            # Esperar a que aparezca el formulario de login
            wait = WebDriverWait(self.driver, 10)
            
            # Llenar el formulario de login
            username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Ingrese su nombre de usuario']")))
            password_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Ingrese su contraseña']")
            
            username_field.clear()
            username_field.send_keys(username)
            
            password_field.clear()
            password_field.send_keys(password)
            
            # Hacer clic en el botón de ingresar
            login_button = self.driver.find_element(By.XPATH, "//button[text()='Ingresar']")
            login_button.click()
            
            # Esperar a que se complete el login
            time.sleep(5)
            
            # Verificar si el login fue exitoso
            if "dashboard" in self.driver.current_url:
                self.is_logged_in = True
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Error durante el login: {str(e)}")
            return False
    
    def navigate_to_personas(self):
        """Navega a la sección de personas"""
        try:
            if not self.is_logged_in:
                return False
                
            # Navegar a la página de personas
            self.driver.get("https://dashboard.knowlers.app/personas/consulta")
            time.sleep(3)
            return True
            
        except Exception as e:
            print(f"Error navegando a personas: {str(e)}")
            return False
    
    def search_by_dni(self, dni):
        """Realiza una búsqueda por DNI"""
        try:
            if not self.navigate_to_personas():
                return {"error": "No se pudo navegar a la sección de personas"}
            
            wait = WebDriverWait(self.driver, 10)
            
            # Buscar el campo de DNI
            dni_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Ingrese DNI']")))
            dni_field.clear()
            dni_field.send_keys(dni)
            
            # Hacer clic en el botón de buscar
            search_button = self.driver.find_element(By.XPATH, "//button[text()='Buscar']")
            search_button.click()
            
            # Esperar a que aparezcan los resultados
            time.sleep(5)
            
            # Extraer los resultados
            results = self.extract_results()
            return results
            
        except Exception as e:
            return {"error": f"Error en la búsqueda por DNI: {str(e)}"}
    
    def search_by_name(self, nombres, apellido_paterno, apellido_materno):
        """Realiza una búsqueda por nombre completo"""
        try:
            if not self.navigate_to_personas():
                return {"error": "No se pudo navegar a la sección de personas"}
            
            wait = WebDriverWait(self.driver, 10)
            
            # Buscar los campos de nombre
            nombres_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Nombres']")))
            apellido_p_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Apellido Paterno']")
            apellido_m_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Apellido Materno']")
            
            # Llenar los campos
            nombres_field.clear()
            nombres_field.send_keys(nombres)
            
            apellido_p_field.clear()
            apellido_p_field.send_keys(apellido_paterno)
            
            apellido_m_field.clear()
            apellido_m_field.send_keys(apellido_materno)
            
            # Hacer clic en el botón de buscar
            search_button = self.driver.find_element(By.XPATH, "//button[text()='Buscar']")
            search_button.click()
            
            # Esperar a que aparezcan los resultados
            time.sleep(5)
            
            # Extraer los resultados
            results = self.extract_results()
            return results
            
        except Exception as e:
            return {"error": f"Error en la búsqueda por nombre: {str(e)}"}
    
    def extract_results(self):
        """Extrae los resultados de la búsqueda"""
        try:
            # Buscar la tabla de resultados
            results_data = {}
            
            # Intentar extraer datos de la tabla de resultados
            table_rows = self.driver.find_elements(By.CSS_SELECTOR, "table tr")
            
            for row in table_rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 2:
                    key = cells[0].text.strip()
                    value = cells[1].text.strip()
                    if key and value:
                        results_data[key] = value
            
            # Si no hay tabla, intentar extraer de otros elementos
            if not results_data:
                result_elements = self.driver.find_elements(By.CSS_SELECTOR, ".result-item, .data-field")
                for element in result_elements:
                    text = element.text.strip()
                    if ":" in text:
                        key, value = text.split(":", 1)
                        results_data[key.strip()] = value.strip()
            
            return {
                "success": True,
                "data": results_data,
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {"error": f"Error extrayendo resultados: {str(e)}"}
    
    def close(self):
        """Cierra el driver"""
        if self.driver:
            self.driver.quit()

# Instancia global del scraper
scraper_instance = KnowlersScraper()

@scraper_bp.route('/login', methods=['POST'])
def login():
    """Endpoint para iniciar sesión"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "Username y password son requeridos"}), 400
        
        success = scraper_instance.login(username, password)
        
        if success:
            return jsonify({"message": "Login exitoso", "logged_in": True})
        else:
            return jsonify({"error": "Credenciales inválidas"}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@scraper_bp.route('/search/dni', methods=['POST'])
def search_dni():
    """Endpoint para búsqueda por DNI"""
    try:
        data = request.get_json()
        dni = data.get('dni')
        
        if not dni:
            return jsonify({"error": "DNI es requerido"}), 400
        
        if not scraper_instance.is_logged_in:
            return jsonify({"error": "Debe iniciar sesión primero"}), 401
        
        results = scraper_instance.search_by_dni(dni)
        return jsonify(results)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@scraper_bp.route('/search/name', methods=['POST'])
def search_name():
    """Endpoint para búsqueda por nombre"""
    try:
        data = request.get_json()
        nombres = data.get('nombres')
        apellido_paterno = data.get('apellido_paterno')
        apellido_materno = data.get('apellido_materno')
        
        if not all([nombres, apellido_paterno, apellido_materno]):
            return jsonify({"error": "Nombres, apellido paterno y materno son requeridos"}), 400
        
        if not scraper_instance.is_logged_in:
            return jsonify({"error": "Debe iniciar sesión primero"}), 401
        
        results = scraper_instance.search_by_name(nombres, apellido_paterno, apellido_materno)
        return jsonify(results)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@scraper_bp.route('/status', methods=['GET'])
def status():
    """Endpoint para verificar el estado del scraper"""
    return jsonify({
        "status": "active",
        "logged_in": scraper_instance.is_logged_in,
        "driver_active": scraper_instance.driver is not None
    })

@scraper_bp.route('/logout', methods=['POST'])
def logout():
    """Endpoint para cerrar sesión y limpiar recursos"""
    try:
        scraper_instance.close()
        scraper_instance.is_logged_in = False
        return jsonify({"message": "Sesión cerrada exitosamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

