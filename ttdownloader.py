from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
from sys import argv, exit
from requests import get
from time import sleep

chrome_options = Options()
chrome_options.add_argument("--lang=en-US")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

if len(argv) < 2:
    print('Usage: python script.py <url>')
    exit(1)

url = argv[1]

def download_video(session, video_url, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ttdownloader_{timestamp}.mp4"    
    headers = {
        'User-Agent': session.execute_script("return navigator.userAgent;"),
        'Referer': url,
        'Cookie': "; ".join([f"{c['name']}={c['value']}" for c in session.get_cookies()])
    }
    response = get(video_url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Video downloaded as {filename}")
    else:
        print(f"Error downloading video. Status code: {response.status_code}")

try:
    driver.get(url)
    sleep(3)
    video_url = None
    while True:
        try:
            video_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )
            video_url = video_element.get_attribute("src")
            if video_url:
                print("Video URL:", video_url)
                break
        except Exception as e:
            print("Waiting for video element...")

    if video_url:
        print("Downloading video...")
        download_video(driver, video_url)
    else:
        print("Video URL not found.")
finally:
    driver.quit()
