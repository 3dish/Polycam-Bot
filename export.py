import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def export():
    driver = webdriver.Chrome()
    driver.get("https://poly.cam")
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-12ll7o1")))
    time.sleep(3)
    export_buttons = driver.find_elements(By.CSS_SELECTOR, '.css-1x0bjs7')

    for button in export_buttons:
        # Click on the Model 3 dots
        driver.execute_script("arguments[0].scrollIntoView();", button)
        button.click()
        # Click Export
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-8y1flk:nth-child(3)"))).click()
        # Select GLTF format
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".css-1rr4qq7:nth-child(1) > .css-1u07a6n:nth-child(3)"))).click()
        # Click Start Download
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1wrlxiy"))).click()
        # Close
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1ghaoiw svg"))).click()

        # Click outside the popup to exit
        driver.execute_script("document.elementFromPoint(1, 1).click();")
        print("Export")

    time.sleep(200)
    driver.quit()


if __name__ == '__main__':
    # Run the export() function when the models finish processing to export the in GLTF
    export()
