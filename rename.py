import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fetch_model_names_from_polycam(driver):
    # This assumes the model names are in input fields. Adjust as per your actual page structure.
    model_name_elements = driver.find_elements(By.CSS_SELECTOR, "input[name='itemName']")
    return [element.get_attribute('value') for element in model_name_elements]


def move_files_to_directory(source_folder, destination_folder, file_names):
    """
    Moves files from source_folder to destination_folder based on the given file names.
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for file_name in file_names:
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)

        if os.path.exists(source_path):
            print(f"Moving: {source_path} to {destination_path}")
            shutil.move(source_path, destination_path)
        else:
            print(f"{source_path} does not exist!")


def rename_exported_files(exported_folder_path, model_names):
    # Fetch all exported file paths
    full_paths = [os.path.join(exported_folder_path, f) for f in os.listdir(exported_folder_path)]

    # Sort files by modification time (most recent first)
    exported_files = sorted(full_paths, key=os.path.getmtime, reverse=True)

    # Only considering files and ignoring directories
    exported_files = [f for f in exported_files if os.path.isfile(f)]

    print("Exported Files:", exported_files)
    print("Model Names:", model_names)
    model_names.reverse()
    # Rename each file
    for old_path, new_name in zip(exported_files[:len(model_names)], model_names):
        new_path = os.path.join(exported_folder_path,
                                new_name + os.path.splitext(old_path)[1])  # keep the original file extension
        print(f"Renaming: {old_path} to {new_path}")
        os.rename(old_path, new_path)

def rename_and_move():
    # Your Selenium driver setup
    driver = webdriver.Chrome()
    driver.get("https://poly.cam")
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-12ll7o1")))
    time.sleep(3)

    # Fetch names from PolyCam and rename exported files
    model_names = fetch_model_names_from_polycam(driver)
    downloads_path = os.path.expanduser('~/Downloads')
    print("Downloads Path:", downloads_path)
    rename_exported_files(downloads_path, model_names)

    # Define your destination folder path
    destination_folder = "G:/Shared drives/Business Operations/CodeAutomations/PolycamBot/RestaurantTest/Raw"  # Replace with the path where you want to move the files
    renamed_files = [name + ".glb" for name in model_names]
    move_files_to_directory(downloads_path, destination_folder, renamed_files)

    time.sleep(300)
    driver.quit()

if __name__ == '__main__':
    # Run the export() function when the models finish processing to export the in GLTF
    rename_and_move()