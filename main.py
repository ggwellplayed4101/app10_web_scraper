import requests
import selectorlib
import time
import ssl, smtplib
import os
from dotenv import load_dotenv
import sqlite3

# Url from where web scrapping will be done
URL = "https://programmer100.pythonanywhere.com/tours/"

# To make it seem the http request is from a browser and not a script.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

connection = sqlite3.connect("data.db")

def scrape(url):
    """Scrape the page spurce from the URL"""
    response = requests.get(url, headers=HEADERS)

    # Get source code in text
    source = response.text
    return source


def extract(source):
    """Extract from the given source according to extraction rule in
    extract.html"""
    
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)['tours']
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    # Load the .env file
    load_dotenv()

    # Access the variables
    username = os.getenv("EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    receiver = os.getenv("EMAIL")
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email was sent!")


def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row

    # Inserts the row if already not inserted before
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", 
                   (band, city, date))
    connection.commit()

def read(extracted):
    """Returns rows which are sane as the extracted data"""
    # Created a row of dara
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row

    # Slects rowa matching the extracted data
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                   (band, city, date))
    rows = cursor.fetchall()
    return rows

if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        # Store data if it is not already stored
        # Send email if it is new tour
        if extracted != "No upcoming tours":
            row = read(extracted)
            with open("data.txt", "r") as file:
                if not row:
                    send_email(message="Hey new event was found!")
                    store(extracted)
        time.sleep(2)