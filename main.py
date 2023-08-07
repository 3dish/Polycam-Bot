import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


def list_image_files_from_folder(folder_path):
    """List all image files from a given folder and its subfolders."""
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp']
    image_files = []

    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file in filenames:
            if os.path.splitext(file)[1].lower() in image_extensions:
                image_files.append(os.path.join(dirpath, file))

    return image_files


def process_folder(driver, folder_path):
    # Get list of all image files from the folder
    image_files = list_image_files_from_folder(folder_path)
    if not image_files:
        return

    # Create a single string with all image paths separated by newlines
    files_to_upload = '\n'.join(image_files)
    # portal-target > div > div.css-5d0rkm
    WebDriverWait(driver, 300).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".css-5d0rkm")))
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-12ll7o1"))).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-pu23zc:nth-child(1) .css-ouqbe"))).click()

    # Send the image paths to the file input element
    file_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'image-upload')))
    file_input.send_keys(files_to_upload)

    # Additional steps like setting model options and naming the model can be added here
    # Select Option Reduced
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1io8q4v:nth-child(1) > .css-nwhneq"))).click()
    # Select Object Mask
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1luq9jd:nth-child(2) .css-1t8bg7a"))).click()
    # Select Upload
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-ht7pri"))).click()

    WebDriverWait(driver, 300).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".css-5d0rkm")))
def rename_models_to_folder_name(driver, folder_name):
    # Find the input field corresponding to the next 3D model name.
    # Using the explicit wait ensures that we get the next available name input.
    model_name_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="itemName"]')))

    model_name_element.clear()  # Clear current name
    model_name_element.send_keys(folder_name)  # Input the folder na
def main():
    root_folder = "G:/Shared drives/Business Operations/CodeAutomations/PolycamBot/RestaurantTest/Photos"
    subfolders = [os.path.join(root_folder, d) for d in os.listdir(root_folder) if
                  os.path.isdir(os.path.join(root_folder, d))]

    driver = webdriver.Chrome()
    # Navigate and perform necessary actions on the website
    driver.get("https://poly.cam")
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-12ll7o1")))
    time.sleep(3)

    try:
        for folder in subfolders:
            process_folder(driver, folder)
            rename_models_to_folder_name(driver, os.path.basename(folder))

    except Exception as e:
        print(f"An error occurred(Nelson Debug): {e}")
    finally:
        time.sleep(300)
        driver.quit()

def export():
    driver = webdriver.Chrome()
    driver.get("https://poly.cam")
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-12ll7o1")))
    time.sleep(3)
    export_buttons = driver.find_elements(By.CSS_SELECTOR, '.css-1x0bjs7')

    for button in export_buttons:
        button.click()
        # Depending on the website's behavior, you might need to wait between clicks.
        time.sleep(2)
        driver.execute_script("document.elementFromPoint(1, 1).click();")
        time.sleep(1)
    print("Export")

if __name__ == '__main__':
    #main()
    export()
