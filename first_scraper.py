import requests
from bs4 import BeautifulSoup
import json



# Function to extract quotes, authors, and tags from a web page
def scrape_page(soup, quotes):
    # Find all elements containing quotes
    quote_elements = soup.find_all('div', class_='quote')

    # Iterate through each quote element
    for quote_element in quote_elements:
        # Extract text of the quote
        text = quote_element.find('span', class_='text').text
        # Extract author of the quote
        author = quote_element.find('small', class_='author').text

        # Extract tags associated with the quote
        tag_elements = quote_element.find('div', class_='tags').find_all('a', class_='tag')
        tags = [tag_element.text for tag_element in tag_elements]

        # Append extracted data to the list of quotes
        quotes.append({
            'text': text,
            'author': author,
            'tags': tags
        })

# Base URL for the website to scrape
base_url = 'https://quotes.toscrape.com'
# Headers to mimic a web browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

# Send HTTP request to the base URL and parse the HTML content
page = requests.get(base_url, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')

# List to store extracted quotes
quotes = []
# Extract quotes from the initial page
scrape_page(soup, quotes)

# Find the link to the next page
next_li_element = soup.find('li', class_='next')

# Continue extracting quotes from subsequent pages until there are no more pages
while next_li_element is not None:
    # Extract relative URL of the next page
    next_page_relative_url = next_li_element.find('a', href=True)['href']
    # Construct full URL of the next page
    next_page_url = base_url + next_page_relative_url

    # Send HTTP request to the next page and parse its HTML content
    page = requests.get(next_page_url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    # Extract quotes from the next page
    scrape_page(soup, quotes)
    # Find the link to the next page (if exists)
    next_li_element = soup.find('li', class_='next')

# Check if any quotes were extracted
if len(quotes) == 0:
    print("No quotes extracted.")
else:
    # Write extracted quotes to a JSON file
    with open('quotes.json', 'w', encoding='utf-8') as json_file:
        json.dump(quotes, json_file, indent=4)
    print("Quotes successfully written to quotes.json")
