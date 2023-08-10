import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def delete():
    driver = webdriver.Chrome()
    driver.get("https://poly.cam")
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-12ll7o1")))
    time.sleep(3)
    export_buttons = driver.find_elements(By.CSS_SELECTOR, '.css-1x0bjs7')

    for button in export_buttons:
        # Click on the Model 3 dots
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        time.sleep(1)
        button.click()
        # Click delete
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-8y1flk:nth-child(5) .css-1vjvbvp"))).click()
        # Select delete in the popup
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".css-ytva8q:nth-child(2)"))).click()
        time.sleep(0.5)

        print("Delete")

    time.sleep(200)
    driver.quit()


if __name__ == '__main__':
    # Run the export() function when the models finish processing to export the in GLTF
    delete()