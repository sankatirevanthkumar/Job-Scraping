#!/usr/bin/env python3
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options for headless execution on a server
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without UI
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-3d-apis")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Use webdriver_manager to automatically download and set up ChromeDriver
service = Service(ChromeDriverManager().install())

# LinkedIn Job Search URL
url = (
    "https://www.linkedin.com/jobs/search?keywords=Software%20Developer&"
    "location=Bengaluru&geoId=105214831&distance=50&f_JT=I&f_PP=105214831&f_TPR=&"
    "position=1&pageNum=0"
)

# Initialize WebDriver using the updated service
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(10)
driver.get(url)

# Allow extra time for dynamic content to load
time.sleep(5)

# Scroll and load more jobs by clicking the "See more jobs" button multiple times
for _ in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    try:
        see_more_button = driver.find_element(By.XPATH, "//button[@aria-label='See more jobs']")
        driver.execute_script("arguments[0].click();", see_more_button)
        time.sleep(3)
    except Exception:
        # Button may not appear every time—ignore if not found.
        pass

# Wait until the job cards are loaded
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.base-search-card"))
)

# Initialize lists for job details.
company_names = []
job_titles   = []
job_links    = []

# Iterate over each job card and extract details.
job_cards = driver.find_elements(By.CSS_SELECTOR, "div.base-search-card")
for card in job_cards:
    # Extract job title
    try:
        title_elem = card.find_element(By.CSS_SELECTOR, ".base-search-card__title")
        title = title_elem.get_attribute("innerText").strip()
    except Exception:
        title = "N/A"
    
    # Extract company name
    try:
        company_elem = card.find_element(By.CSS_SELECTOR, ".base-search-card__subtitle")
        company = company_elem.get_attribute("innerText").strip()
    except Exception:
        company = "N/A"
    
    # Extract job link
    try:
        link_elem = card.find_element(By.CSS_SELECTOR, "a.base-card__full-link")
        link = link_elem.get_attribute("href")
    except Exception:
        link = "N/A"
    
    job_titles.append(title)
    company_names.append(company)
    job_links.append(link)

# Align the lists to the length of the shortest one
min_length = min(len(company_names), len(job_titles), len(job_links))
company_names = company_names[:min_length]
job_titles   = job_titles[:min_length]
job_links    = job_links[:min_length]

# Save the scraped data to a CSV file
job_data = pd.DataFrame({
    "Company": company_names,
    "Title": job_titles,
    "Links": job_links
})
job_data.to_csv("internshipjobs_updated.csv", index=False)

print(f"Scraping completed! {min_length} job postings saved to internshipjobs_updated.csv.")
driver.quit()
