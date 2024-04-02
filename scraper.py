from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import requests
import io
from PIL import Image

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://google.com")

def get_google_images(driver, delay, max_images):
    def scroll_down(driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
        
    url = "https://www.google.com/search?q=success+kid&sca_esv=12ccb0fb0fe1b570&rlz=1C1PNFB_enLK995LK999&udm=2&biw=1536&bih=730&sxsrf=ACQVn0_1tUH_xcAdc2GHd3GpEKRzQ1H9Sw%3A1712067869128&ei=HRUMZrCkB5zW4-EPyNyPiAc&ved=0ahUKEwjwpq7p3aOFAxUc6zgGHUjuA3EQ4dUDCBA&uact=5&oq=success+kid&gs_lp=Egxnd3Mtd2l6LXNlcnAiC3N1Y2Nlc3Mga2lkMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABEj6FVD5A1jAE3ABeACQAQCYAWGgAdAHqgECMTG4AQPIAQD4AQGYAgygAqkIqAIKwgIHECMY6gIYJ8ICBBAjGCfCAgoQABiABBiKBRhDwgIIEAAYgAQYsQPCAgsQABiABBiKBRixA8ICDRAAGIAEGIoFGEMYsQPCAgsQABiABBixAxiDAZgDBpIHBDEwLjKgB708&sclient=gws-wiz-serp"
    
    driver.get(url)
    
    image_urls = set()
    skips = 0
    
    while len(image_urls) + skips < max_images:
        scroll_down(driver)
        
        thumbnails = driver.find_elements(By.CLASS_NAME, "mNsIhb")
        
        for img in thumbnails[len(image_urls): max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue
            
            images = driver.find_elements(By.CLASS_NAME, "sFlh5c")
            for image in images:
                if  image.get_attribute('src') in image_urls:
                    max_images +=1
                    skips += 1
                    break
                    
                elif image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")
    
    return image_urls

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name
        
        with open(file_path, "wb") as f:
            image.save(f, "JPEG")
            
        print("Success")
    except Exception as e:
        print('FAILED -', e)

urls = get_google_images(driver, 1, 10)

for i, url in enumerate(urls):
    download_image("images/", url, str(i) + ".jpg")

time.sleep(5)

driver.quit()