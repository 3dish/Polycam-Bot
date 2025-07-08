import os
import time
import argparse
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
    button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#__next > div.WorkspaceView_container__hQc8u > div.WorkspaceView_layout__E_XAT > nav > div > button")))
    print("Button found! Now clicking...")
    button.click()
    print("Button clicked! Waiting for popup...")
    
    # Wait a moment for the popup to appear
    time.sleep(2)
    
    try:
        # Click "Create a Gaussian splat" button (index 2)
        buttons = driver.find_elements(By.CSS_SELECTOR, "dialog button")
        if len(buttons) >= 3:
            gaussian_button = buttons[2]  # Index 2 is "Create a Gaussian splat"
            print("Gaussian button found! Clicking...")
            gaussian_button.click()
            print("Gaussian button clicked!")
        else:
            print(f"Not enough buttons found. Expected at least 3, got {len(buttons)}")
    except Exception as e:
        print(f"Error clicking Gaussian button: {e}")
        print("Let me try to find any buttons in the popup...")
        # Try to find any buttons in the popup
        buttons = driver.find_elements(By.CSS_SELECTOR, "dialog button")
        print(f"Found {len(buttons)} buttons in dialog")
        for i, btn in enumerate(buttons):
            try:
                print(f"Button {i}: {btn.text}")
            except:
                print(f"Button {i}: [Could not get text]")


    # Send the image paths to the file input element
    file_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Upload files"]')))
    file_input.send_keys(files_to_upload)

   
     # Wait a moment for the file upload interface to load
    time.sleep(2)
    
    try:
        # Click "Upload & Process" button using the full selector you provided
        upload_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div:nth-child(50) > div > dialog > div > div.styles_content__GGCD8 > div.styles_container__9wrMQ.styles_y__eiMV9.styles_content__Kkmae > div > div > div.SelectOptions_footer__4gI9c > button.styles_action__Z2Fso.styles_l__vHx1i.styles_rect__lTWI7.styles_l-pad__GSKF9.SelectOptions_btn__aM4on")))
        print("Upload & Process button found! Clicking...")
        upload_button.click()
        print("Upload & Process button clicked!")
        
        # Wait for upload to complete (wait for the dialog to disappear)
        print("Waiting for upload to complete...")
        WebDriverWait(driver, 300).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "body > div:nth-child(50) > div > dialog")))
        print("Upload completed!")
        
    except Exception as e:
        print(f"Error clicking Upload & Process button: {e}")
        print("Let me try to find the button by text...")
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for i, btn in enumerate(buttons):
            try:
                if "Upload" in btn.text or "Process" in btn.text:
                    print(f"Found upload button: {btn.text}")
                    btn.click()
                    print("Upload button clicked by text!")
                    break
            except:
                pass
def rename_models_to_folder_name(driver, folder_name):
    # Find the input field corresponding to the next 3D model name.
    # Using the explicit wait ensures that we get the next available name input.

    model_name_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="itemName"]')))

    model_name_element.clear()  # Clear current name
    model_name_element.send_keys(folder_name)  # Input the folder na
    time.sleep(0.5)
def main(root_folder):
    #root_folder = "G:/Shared drives/Business Operations/CodeAutomations/PolycamBot/RestaurantTest/Photos"
    subfolders = [os.path.join(root_folder, d) for d in os.listdir(root_folder) if
                  os.path.isdir(os.path.join(root_folder, d))]

    driver = webdriver.Chrome()
    # Navigate and perform necessary actions on the website
    driver.get("https://poly.cam")
    #Wait for Enter to continue
    input("Press Enter to continue...") 

    try:
        for folder in subfolders:
            process_folder(driver, folder)
            #rename_models_to_folder_name(driver, os.path.basename(folder))

    except Exception as e:
        print(f"An error occurred(Nelson Debug): {e}")
    finally:
        time.sleep(300)
        driver.quit()

if __name__ == '__main__':
    #Run the main() function
    parser = argparse.ArgumentParser(description="Upload files to PolyCam")
    parser.add_argument("photos_folder", help="Path to the Photos folder where the files should be imported")
    args = parser.parse_args()
    main(args.photos_folder)