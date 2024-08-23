import csv
from bs4 import BeautifulSoup
import requests

def extract_info_from_span(span_element):
    if span_element:
        text = span_element.text.strip()
        if "beds" in text:
            return text.split()[0]
        elif "baths" in text:
            return text.split()[0]
        elif "Toilets" in text:
            return text.split()[0]
    return 'None'

def fetch_properties(url, writer):
    try:
        # Fetch the HTML content of the page
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all property listings
        properties = soup.find_all('div', class_='single-room-text')

        for prop in properties:
            # Extract location
            location = prop.find('h4')
            
            # Extract price
            price_tag = prop.find('h3', class_='listings-price')
            if price_tag:
                price_currency = price_tag.find('span', itemprop='priceCurrency')
                price_value = price_tag.find('span', itemprop='price')
                price = f"{price_currency.text.strip() if price_currency else 'None'} {price_value.text.strip() if price_value else 'None'}" if price_currency and price_value else 'None'
            else:
                price = 'None'
            
            # Extract property type
            property_type_tag = prop.find('h2', class_='listings-property-title')
            if property_type_tag:
                property_title = property_type_tag.text.lower()
                if 'house' in property_title:
                    property_type = 'House'
                elif 'apartment' in property_title:
                    property_type = 'Apartment'
                else:
                    property_type = 'Other'

                purchase_type = 'Sale' if 'sale' in property_title else 'Rent'
            else:
                property_type = 'Unknown'
                purchase_type = 'Unknown'
            
            # Extract beds, baths, and toilets from the div with class 'fur-areea'
            fur_area = prop.find('div', class_='fur-areea')
            beds = None
            baths = None
            toilets = None
            if fur_area:
                spans = fur_area.find_all('span')
                for span in spans:
                    text = span.text.strip()
                    if "beds" in text:
                        beds = text.split()[0]
                    elif "baths" in text:
                        baths = text.split()[0]
                    elif "Toilets" in text:
                        toilets = text.split()[0]

            location_text = location.text.strip() if location else 'None'
            beds_text = beds if beds else 'None'
            baths_text = baths if baths else 'None'
            toilets_text = toilets if toilets else 'None'
            
            # Write the data to CSV
            writer.writerow([location_text, beds_text, baths_text, toilets_text, price, property_type, purchase_type])
    except Exception as e:
        print(f"Error fetching properties from {url}: {e}")

# Base URL for the section
base_url = 'https://www.propertypro.co.ke/property-for-rent/in/nairobi?search=&type=&bedroom=&min_price=&max_price='

# Open CSV file for writing
with open('propco_listings-rent.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Location', 'Beds', 'Baths', 'Toilets', 'Price', 'Property Type', 'Purchase Type'])
    
    page = 1
    while True:
        url = base_url if page == 1 else f'{base_url}&page={page}' # Confirm the url for the next page whether it uses '&' or '?' as the connector
        print(f"Fetching data from {url}...")
        try:
            # Fetch and process properties from the current page
            fetch_properties(url, writer)
            
            # Check for next page existence (stop condition)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            next_button = soup.find('a', {'alt': 'view next property page'})
            
            if not next_button:
                break
            else:
                page += 1
        except Exception as e:
            print(f"Error fetching properties from {url}: {e}")
            break

print('File saved successfully')
