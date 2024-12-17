#!/usr/bin/env python3
import os
import sys
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def setup_driver():
    chrome_options = Options()
    # Uncomment the line below if you want to run headless
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    return webdriver.Chrome(options=chrome_options)

def fetch_image_links(query, num_images):
    driver = setup_driver()
    
    # Construct Bing image search URL with size filter
    base_url = "https://www.bing.com/images/search"
    params = {
        'q': query,
        'qft': '+filterui:imagesize-custom_2000_2000',  # Filter for large images
        'form': 'IRFLTR',
        'first': '1'
    }
    
    # Convert params to URL query string
    query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
    url = f"{base_url}?{query_string}"
    
    try:
        driver.get(url)
        links = []
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while len(links) < num_images:
            # Scroll to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for images to load
            
            # Click "See more images" button if present
            try:
                more_button = driver.find_element(By.CLASS_NAME, "btn_seemore")
                more_button.click()
                time.sleep(2)
            except:
                pass
            
            # Get image links
            thumbnails = driver.find_elements(By.CSS_SELECTOR, ".iusc")
            for thumb in thumbnails:
                if len(links) >= num_images:
                    break
                try:
                    img_data = thumb.get_attribute("m")
                    if img_data:
                        import json
                        img_url = json.loads(img_data)["murl"]
                        if img_url not in links:
                            links.append(img_url)
                except:
                    continue
            
            # Check if we've reached the bottom
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        return links
    
    finally:
        driver.quit()

def download_image(url, dest_dir):
    filename = os.path.basename(url.split('?')[0])
    # In case the filename is something weird, fall back to something random
    if not filename or '.' not in filename:
        from uuid import uuid4
        filename = str(uuid4()) + ".jpg"
    filepath = os.path.join(dest_dir, filename)
    
    # Don't redownload if it exists
    if os.path.exists(filepath):
        print(f"Skipping {url}, already exists.")
        return
    
    try:
        # Ensure destination directory exists
        os.makedirs(dest_dir, exist_ok=True)
        
        # Add headers to prevent some blocks
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        resp = requests.get(url, timeout=15, headers=headers)  # Increased timeout
        resp.raise_for_status()
        
        # Verify we got an image
        content_type = resp.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            print(f"Skipping {url}, not an image (content-type: {content_type})")
            return
            
        with open(filepath, 'wb') as f:
            f.write(resp.content)
        print(f"Downloaded HD image {url} to {filepath}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 script.py <search_query> <num_images>")
        sys.exit(1)
    
    query = sys.argv[1]
    num_images = int(sys.argv[2])
    
    # Create base images directory if it doesn't exist
    base_dir = os.path.join(os.path.dirname(__file__), 'images')
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    # Create query-specific subdirectory with improved sanitization
    safe_query = ''.join(c for c in query if c.isalnum() or c.isspace() or c in '-_')
    query_dir = os.path.join(base_dir, safe_query.strip().replace(' ', '-').lower())
    os.makedirs(query_dir, exist_ok=True)
    
    print(f"Searching for HD images of '{query}'...")
    
    links = fetch_image_links(query, num_images)
    
    print(f"Found {len(links)} images. Starting download...")
    
    for link in links:
        download_image(link, query_dir)
    
    print(f"Done. Downloaded {len(links)} images to {query_dir}")
if __name__ == "__main__":
    main()
