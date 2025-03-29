import pickle
from selenium import webdriver
from selenium.webdriver.edge.service import Service

# Set up Edge WebDriver
driver_path = "C:/Users/maste/Downloads/edgedriver_win64/msedgedriver.exe"
service = Service(driver_path)
edge_options = webdriver.EdgeOptions()
edge_options.add_argument("user-data-dir=C:\\Users\\maste\\New_Edge_Profile")

driver = webdriver.Edge(service=service, options=edge_options)
driver.get("https://www.spotify.com")

# Load saved cookies
with open("spotify_cookies.pkl", "rb") as file:
    cookies = pickle.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)

# Access Spotify Charts directly without logging in
driver.get("https://charts.spotify.com/charts/view/regional-in-daily/latest")
print(f"Page title is: {driver.title}")

# Continue your automation logic...
driver.quit()
