import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to scrape the website and check for new jobs with specified keywords
def scrape_website(url):
    keywords = ["audit", "compliance", "associate", "intern"]

    # Send a request to the website
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all job listings
        job_listings = soup.find_all('div', class_='posting')

        # Check if any job listing matches the criteria
        for job in job_listings:
            job_title = job.find('h5').text.strip().lower()
            job_link = "https://jobs.lever.co/coalfire" + job.find('a')['href']
            if any(keyword in job_title for keyword in keywords):
                send_alert(job_title, job_link)
    else:
        print("Failed to fetch webpage")

# Function to send email alert
def send_alert(job_title, job_link):
    # Email configuration
    sender_email = "wpwalker1@gmail.com"
    receiver_email = "wpwalker1@gmail.com"
    password = "oojd brku gxdl tovg"

    # Create message container
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "New Job Alert: " + job_title

    # Email body
    body = f"New job available:\n\nTitle: {job_title}\nLink: {job_link}"
    message.attach(MIMEText(body, 'plain'))

    # Send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# URL of the website to scrape
url = "https://jobs.lever.co/coalfire"

# Call the function to scrape the website and check for new jobs with specified keywords
scrape_website(url)
