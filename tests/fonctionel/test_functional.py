import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

def test_parcours_complet():
    try:
        driver.get("http://127.0.0.1:5000")
        driver.find_element(By.NAME, "email").send_keys("john@simplylift.co")
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        print("Connexion OK")


        driver.get("http://127.0.0.1:5000/book/%20Classic1/Simply%20Lift")
        time.sleep(2)

        places = driver.find_element(By.NAME, "places")
        places.clear()
        places.send_keys("5")
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(3)

        assert "Great-booking complete!" in driver.page_source
        print("Réservation de 5 places → OK")

        driver.get("http://127.0.0.1:5000/book/%20Classic1/Simply%20Lift")
        time.sleep(2)

        places = driver.find_element(By.NAME, "places")
        places.clear()
        places.send_keys("15")
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(3)

        assert "You cannot book more than 12 places per competition" in driver.page_source
        print("Blocage à 15 places → OK")

        driver.get("http://127.0.0.1:5000/pointsDisplay")
        time.sleep(2)

        assert "Points table" in driver.page_source or "Table points" in driver.page_source
        assert "Simply Lift" in driver.page_source
        print("Tableau des points → OK")

        print("fin des tests fonctionnels")
    finally:
        time.sleep(5)
        driver.quit()


