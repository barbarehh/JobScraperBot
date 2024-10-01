from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import time

# ChromeDriver setup
chrome_options = Options()
chrome_options.add_argument("--headless")  # Use this for standard headless mode
# chrome_options.add_argument("--headless=old")  # Works on my device but not standard


# Correct path to chromewebdriver (es chemia konkretulad)
service = Service(executable_path=r'C:\Users\user\chromedriver-win64\chromedriver-win64\chromedriver.exe')  

# Your Telegram bot token and chat ID
telegram_token='' # Your Telegram Bot token goes here
chat_id='' # Your Telegram chat ID goes here


def send_message(message):
    url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    requests.post(url, data=payload)



def get_jobs():

    # Start the Chrome browser
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('https://jobs.ge/?page=1&q=&cid=6&lid=&jid=')


    # Find all job rows except the header (pirvel tr tagshi marto headeria)
    job_rows = driver.find_elements("css selector", "tr")[1:] # Skip header

    job_list = []
    for row in job_rows:
        # Check if the job was published in the last 2 days (aweria rom gamoqveynebulia bolo ori dgis ganmavlobasi)
        new_job = row.find_elements("css selector", "img[alt='გამოქვეყნებულია ბოლო 2 დღის განმავლობაში']")  

        if new_job:
            title_element = row.find_element("css selector", "td a.vip")  # Get the title link
            job_title = title_element.text.strip() # Get the job title text
            job_link = title_element.get_attribute('href') # Get the job link
            job_list.append((job_title, job_link)) # add title and link to the list

    driver.quit()
    return job_list

    
# Keep track of sent jobs to avoid duplicates
sent_jobs=set()

while True:
    jobs = get_jobs()

    #davareverse, yvelaze dzvelebidan moyveba
    for title, link in reversed(jobs):
        # Check if this job has not been sent yet
        if (title, link) not in sent_jobs:
            # prepare the message to send 
            message = f"Unemployed friend...\nNew vacancy just dropped!\nCheck it out: {title}\nLink: {link}"
            send_message(message)
            sent_jobs.add((title, link))  # # Mark this job as sent
    time.sleep(3600)  # Check every hour
