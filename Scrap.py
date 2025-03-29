from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import pickle
import time
from datetime import datetime, timedelta
import os
import shutil

# Set the full path to your Edge WebDriver executable
edge_driver_path = r"C:\Users\maste\Downloads\edgedriver_win64\msedgedriver.exe"

# Define the download folder
base_path = r"C:\Users\maste\Desktop\Times Music\Daily_tops"
downloads_folder = os.path.join(base_path, "downloads")

# Create the downloads folder if it doesn't exist
if not os.path.exists(downloads_folder):
    os.makedirs(downloads_folder)

# Configure Edge to download files to the specified folder
edge_options = Options()
edge_options.add_argument("--start-maximized")
edge_options.add_experimental_option("prefs", {
    "download.default_directory": downloads_folder,  # Force downloads to this folder
    "download.prompt_for_download": False,  # Disable the download prompt
    "safebrowsing.enabled": True  # Enable safe browsing
})

# Edge WebDriver Service
service = Service(executable_path=edge_driver_path)

def get_date_range(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = timedelta(days=1)
    return [(start + i * delta).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]

start_date = "2025-03-24"
end_date = "2025-03-28"
date_range = get_date_range(start_date, end_date)

with open("spotify_cookies.pkl", "rb") as cookie_file:
    cookies = pickle.load(cookie_file)

for date in date_range:
    driver = webdriver.Edge(service=service, options=edge_options)

    try:
        driver.get(f'https://charts.spotify.com/charts/view/regional-in-daily/{date}')

        for cookie in cookies:
            if 'domain' in cookie:
                cookie['domain'] = '.spotify.com'
            driver.add_cookie(cookie)

        driver.refresh()
        time.sleep(5)

        # Check if the download button exists
        download_button_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/span/span/button"
        try:
            download_button = driver.find_element(By.XPATH, download_button_xpath)
            download_button.click()
            print(f"Download button clicked successfully for date: {date}!")
        except Exception:
            print(f"Download button not found for date: {date}. Skipping...")

        time.sleep(5)  # Allow time for the file to download

        # Check if the file has been downloaded
        downloaded_file_name = f"regional-in-daily-{date}.csv"
        destination_path = os.path.join(downloads_folder, downloaded_file_name)

        if os.path.exists(destination_path):
            print(f"File {downloaded_file_name} downloaded successfully.")
        else:
            print(f"Downloaded file {downloaded_file_name} not found in the downloads folder.")

    except Exception as e:
        print(f"Error processing date {date}: {e}")

    finally:
        driver.quit()

print("CSV download and organization process completed for the given date range!")
