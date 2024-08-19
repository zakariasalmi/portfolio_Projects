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

# Function to log in to Twitter via Google
def twitter_login_via_google(email, password):
    driver.get('https://twitter.com/i/flow/login')
    
    try:
        # Click on the "Sign in with Google" button
        google_login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="nsm7Bb-HzV7m-LgbsSe-bN97Pc-sM5MNb oXtfBe-l4eHX"]'))
        )
        google_login_button.click()
        print("Clicked on 'Sign in with Google'")
    except Exception as e:
        print(f"Error clicking 'Sign in with Google': {e}")
        driver.quit()
        return
    
    # Switch to the Google login window
    main_window = driver.current_window_handle
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            break

    try:
        # Enter email
        email_elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'identifierId'))
        )
        email_elem.send_keys(email)
        next_button = driver.find_element(By.XPATH, '//div[@id="identifierNext"]')
        next_button.click()
        print("Entered email and clicked Next")
    except Exception as e:
        print(f"Error entering email: {e}")
        driver.quit()
        return
    
    try:
        # Enter password
        password_elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, 'Passwd'))
        )
        password_elem.send_keys(password)
        next_button = driver.find_element(By.XPATH, '//div[@id="passwordNext"]')
        next_button.click()
        print("Entered password and clicked Next")
    except Exception as e:
        print(f"Error entering password: {e}")
        driver.quit()
        return

    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(1))
    driver.switch_to.window(main_window)
    time.sleep(10)  # Increase wait time to ensure login completes

# Function to extract detailed timestamp
def extract_detailed_timestamp(reply):
    try:
        timestamp_element = reply.find_element(By.XPATH, './/time')
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

# Function to scrape replies
def scrape_replies():
    replies = []
    while True:
        reply_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//article[@role="article"]'))
        )
        print(f"Found {len(reply_elements)} replies")
        for reply in reply_elements:
            try:
                author = reply.find_element(By.XPATH, './/span[contains(@class, "css-901oao")]').text
            except Exception as e:
                print(f"Author extraction error: {e}")
                author = "Unknown"
            try:
                text = reply.find_element(By.XPATH, './/div[contains(@class, "css-901oao r-18jsvk2 r-1k78y06 r-1sixt3s r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")]').text
            except Exception as e:
                print(f"Text extraction error: {e}")
                text = "No Text"
            timestamp = extract_detailed_timestamp(reply)
            try:
                user_profile_link = reply.find_element(By.XPATH, './/a[contains(@href, "/status/")]').get_attribute('href')
            except Exception as e:
                print(f"User profile link extraction error: {e}")
                user_profile_link = "Unknown"
            try:
                likes_text = reply.find_element(By.XPATH, './/div[@data-testid="like"]').text
                likes = int(likes_text.replace('K', '000').replace('M', '000000')) if likes_text else 0
            except Exception as e:
                print(f"Likes extraction error: {e}")
                likes = 0
            replies.append({
                'author': author,
                'user_profile_link': user_profile_link,
                'text': text,
                'timestamp': timestamp,
                'likes': likes
            })

        # Try to find and click "Show more replies" button
        try:
            more_replies = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@role="button"]//span[contains(text(), "Show more replies")]'))
            )
            more_replies.click()
            time.sleep(10)  # Wait after clicking 'Show more replies'
        except Exception as e:
            print(f"No more replies to load or error clicking: {e}")
            break

    return replies

# Function to parse detailed timestamp
def parse_timestamp(timestamp):
    try:
        dt = datetime.strptime(timestamp, "%I:%M %p · %b %d, %Y")
        return dt.strftime("%d %B %Y"), dt.strftime("%H:%M")
    except ValueError as e:
        print(f"Timestamp parsing error: {e}")
        return "Unknown Date", "Unknown Time"

# Your Google login credentials
email = '@gmail.com'
password = 'i'

# Twitter post URL
post_url = 'https://x.com/hespress/status/1700274006845264157?lang=ar-x-fm'

# Log in to Twitter via Google
twitter_login_via_google(email, password)

# Navigate to the post
driver.get(post_url)

# Wait for the page to load
time.sleep(15)

# Scrape the replies
replies = scrape_replies()

# Parse timestamps and update replies
for reply in replies:
    date, time = parse_timestamp(reply['timestamp'])
    reply['date'] = date
    reply['time'] = time

# Convert to DataFrame
df = pd.DataFrame(replies)

# Print the DataFrame
print(df)

# Save to CSV (Optional)
df.to_csv('twitter_replies.csv', index=False)

# Close the WebDriver
driver.quit()
