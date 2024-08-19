from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
from datetime import datetime
 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")

# Set up the WebDriver
service = Service('C:/Users/zakar/Downloads/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

# login sur facebook
def facebook_login(email, password):
    driver.get('https://www.facebook.com/')
    email_elem = driver.find_element(By.ID, 'email')
    password_elem = driver.find_element(By.ID, 'pass')
    email_elem.send_keys(email)
    password_elem.send_keys(password)
    password_elem.send_keys(Keys.RETURN)
    time.sleep(10)  # Increase wait time to ensure login completes

# Function pour lire tous les commentaires
def load_all_comments():
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait to ensure comments load
        try:
            more_comments = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                    '//div[@role="button"]//span[contains(text(), "View more comments")]'))
            )
            more_comments.click()
            time.sleep(5)  # Wait to click 'View more comments'
        except Exception as e:
            print(f"No more comments to load or error clicking: {e}")
            break

# Function pour extraire timestamp
def extract_detailed_timestamp(comment):
    try:
        timestamp_element = comment.find_element(By.XPATH,
        './/span[contains(@class, "xdj266r") and contains(@class, "x11i5rnm") and contains(@class, "xat24cr")]')
        ActionChains(driver).move_to_element(timestamp_element).perform()
        time.sleep(1)  # Wait for the tooltip to appear
        tooltip = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@role="tooltip"]'))
        )
        detailed_timestamp = tooltip.text
        return detailed_timestamp if detailed_timestamp else "Unknown"
    except Exception as e:
        print(f"Timestamp extraction error: {e}")
        return "Unknown"

# Function pour scrape comments
def scrape_comments():
    comments = []
    comment_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@aria-label and contains(@aria-label, "Comment by")]'))
    )
    print(f"Found {len(comment_elements)} comments")
    for comment in comment_elements:
        try:
            author = comment.find_element(By.XPATH, './/span[@dir="auto"]').text
        except Exception as e:
            print(f"Author extraction error: {e}")
            author = "Unknown"
        try:
            text = comment.find_element(By.XPATH, './/div[@dir="auto" and @style="text-align: start;"]').text
        except Exception as e:
            print(f"Text extraction error: {e}")
            text = "No Text"
        timestamp = extract_detailed_timestamp(comment)
        try:
            user_profile_link = comment.find_element(By.XPATH, './/a[contains(@href, "comment_id")]').get_attribute('href')
        except Exception as e:
            print(f"User profile link extraction error: {e}")
            user_profile_link = "Unknown"
        try:
            likes_text = comment.find_element(By.XPATH, './/span[contains(@class, "xi81zsa") and contains(@class, "x1nxh6w3") and contains(@class, "x1fcty0u")]').text
            likes = int(likes_text) if likes_text else 0
        except Exception as e:
            print(f"Likes extraction error: {e}")
            likes = 0
        comments.append({
            'author': author,
            'user_profile_link': user_profile_link,
            'text': text,
            'timestamp': timestamp,
            'likes': likes
        })
    return comments

# Function pour parsé detailed timestamp
def parse_timestamp(timestamp):
    try:
        dt = datetime.strptime(timestamp, "%A %d %B %Y at %H:%M")
        return dt.strftime("%d %B %Y"), dt.strftime("%H:%M")
    except ValueError as e:
        print(f"Timestamp parsing error: {e}")
        return "Unknown Date", "Unknown Time"

# Your Facebook login credentials
email= 'zakaria.salmi123@gmail.com'
password = ''

# Facebook post URL
# 'https://www.facebook.com/photo/?fbid=711975467637154&set=a.642603861240982'
#post_url ='https://web.facebook.com/Hespress/videos/736445464957201'
#post_url = 'https://web.facebook.com/photo/?fbid=715932950574739&set=a.642603861240982'
post_url ='https://web.facebook.com/radio2m.ma/videos/266103039579128'

# Log in to Facebook
facebook_login(email, password)

# Navigate to the post
driver.get(post_url)

# Wait for the page to load
time.sleep(15)

# Load all comments
load_all_comments()

# Scrape the comments
comments = scrape_comments()

# Parse timestamps and update comments
for comment in comments:
    date, time = parse_timestamp(comment['timestamp'])
    comment['date'] = date
    comment['time'] = time

# Convert to DataFrame
df = pd.DataFrame(comments)

# Print the DataFrame
print(df)

# Save to CSV (Optional)
df.to_csv('fb_comments4.csv', index=False)

# Close the WebDriver
driver.quit()
