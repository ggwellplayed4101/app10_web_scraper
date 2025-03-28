import requests
import selectorlib

# Url from where web scrapping will be done
URL = "https://programmer100.pythonanywhere.com/tours/"

# To make it seem the http request is from a browser and not a script.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


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

if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)