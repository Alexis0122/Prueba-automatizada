from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from jinja2 import Environment, FileSystemLoader
import time
import webbrowser

# Inicialización del navegador
driver = webdriver.Chrome()

# Crear directorio para guardar capturas de pantalla
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

# Función para realizar el inicio de sesión en Netflix
def login_to_netflix():
    try:
        driver.get("https://www.netflix.com/login")
        driver.implicitly_wait(10)
        driver.save_screenshot("screenshots/login_step1.png")
        
        # Completar el formulario de inicio de sesión
        username_field = driver.find_element(By.NAME, "userLoginId")
        username_field.send_keys("Login1234@gmail.com")
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("Password1234")
        password_field.submit()
        
        driver.save_screenshot("screenshots/login_step2.png")
        return "Inicio de sesión exitoso."
    except Exception as e:
        return f"Error durante el inicio de sesión: {e}"

# Función para mostrar los perfiles disponibles en Netflix
def display_profiles():
    try:
        driver.implicitly_wait(10)
        profile_icon = driver.find_element(By.CLASS_NAME, "profile-icon")
        driver.save_screenshot("screenshots/display_profiles.png")
        profile_icon.click()
        return "Perfiles mostrados correctamente."
    except Exception as e:
        return f"Error al mostrar perfiles: {e}"

# Función para navegar a la categoría de series en Netflix
def browse_series_category():
    try:
        link_series = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/browse/genre/83']")))
        link_series.click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "slider-item")))
        driver.save_screenshot("screenshots/browse_series_category.png")
        return "Navegación a la categoría de series exitosa."
    except Exception as e:
        return f"No se pudo navegar a la categoría 'Series': {e}"

# Función para seleccionar una serie específica en Netflix
def select_series():
    try:
        driver.implicitly_wait(20)
        series_thumbnail = driver.find_element(By.CLASS_NAME, "slider-item")
        series_thumbnail.click()
        driver.save_screenshot("screenshots/select_series.png")
        return "Selección de serie exitosa."
    except Exception as e:
        return f"Error al seleccionar la serie: {e}"

# Función para reproducir una serie en Netflix
def play_series():
    try:
        play_button = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CLASS_NAME, "primary-button")))
        play_button.click()
        time.sleep(10)
        driver.save_screenshot("screenshots/play_series.png")
        return "Reproducción de serie exitosa."
    except Exception as e:
        return f"Error durante la reproducción de la serie: {e}"

# Ejecutar las funciones y almacenar los resultados
results = {}
results[1] = login_to_netflix()
results[2] = display_profiles()
results[3] = browse_series_category()
results[4] = select_series()
results[5] = play_series()

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("Report.html")
html_content = template.render(results=results)

with open("Report.html", "w") as file:
    file.write(html_content)
    
webbrowser.open("Report.html")

driver.quit()
