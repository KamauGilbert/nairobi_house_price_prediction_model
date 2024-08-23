import csv
from bs4 import BeautifulSoup
import requests

# Function to extract price from a house details page
def extract_price(details_url):
    try:
        html_text = requests.get(details_url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        price_tag = soup.find('span', class_='block text-right text-xl font-semibold leading-7 md:text-xxl md:font-extrabold')
        return price_tag.text.strip() if price_tag else 'None'
    except Exception as e:
        print(f"Error fetching details from {details_url}: {e}")
        return 'None'

# Function to fetch properties from a given URL and save to CSV
def fetch_properties(url, writer):
    try:
        # Fetch the HTML content of the page
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')

        # Determine property type and purchase type based on URL
        if 'houses-for-sale' in url:
            property_type = 'House'
            purchase_type = 'Sale'
        elif 'flats-apartments-for-sale' in url:
            property_type = 'Apartment'
            purchase_type = 'Sale'
        elif 'houses-for-rent' in url:
            property_type = 'House'
            purchase_type = 'Rent'
        elif 'flats-apartments-for-rent' in url:
            property_type = 'Apartment'
            purchase_type = 'Rent'
        elif 'bedsitters-for-rent' in url:
            property_type = 'Bedsitter'
            purchase_type = 'Rent'
        else:
            property_type = 'Unknown'
            purchase_type = 'Unknown'

        # Find all property listings
        properties = soup.find_all('div', class_='relative w-full overflow-hidden rounded-2xl bg-white')

        for prop in properties:
            location = prop.find('p', class_='ml-1 truncate text-sm font-normal capitalize text-grey-650')
            size = prop.find('span', class_='whitespace-nowrap', attrs={'data-cy': 'card-area'})
            bedrooms = prop.find('span', class_='whitespace-nowrap', attrs={'data-cy': 'card-beds'})
            bathrooms = prop.find('span', class_='whitespace-nowrap font-normal', attrs={'data-cy': 'card-bathrooms'})
            price_tag = prop.find('a', class_='no-underline')
            
            if location:
                # Get the text content of location
                location_text = location.text.strip()
                # Initialize other_location_details
                other_location_details = location_text
                # Check if there's a comma in the location text
                if ',' in location_text:
                    # Split by the first comma
                    location_parts = location_text.split(',', 1)
                    location_text = location_parts[0].strip()
                    other_location_details = location_parts[1].strip() if len(location_parts) > 1 else ''
                
            else:
                location_text = 'None'
                other_location_details = 'None'

            size_text = size.text.strip() if size else 'None'
            bedrooms_text = bedrooms.text.strip() if bedrooms else 'None'
            bathrooms_text = bathrooms.text.strip() if bathrooms else 'None'
            details_url = 'https://www.buyrentkenya.com' + price_tag['href'] if price_tag else 'None'
            
            # Extract detailed price information
            detailed_price = extract_price(details_url)
            
            # Write the data to CSV
            writer.writerow([location_text, other_location_details, size_text, bedrooms_text, bathrooms_text, detailed_price, property_type, purchase_type])
    except Exception as e:
        print(f"Error fetching properties from {url}: {e}")

# Base URLs for different sections
base_urls = [
    'https://www.buyrentkenya.com/houses-for-sale',
    'https://www.buyrentkenya.com/flats-apartments-for-sale',
    'https://www.buyrentkenya.com/houses-for-rent',
    'https://www.buyrentkenya.com/flats-apartments-for-rent',
    'https://www.buyrentkenya.com/bedsitters-for-rent'
]

# Open CSV file for writing
with open('property_listings2.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Location', 'Other Location Details', 'Size', 'Bedrooms', 'Bathrooms', 'Price', 'Property Type', 'Purchase Type'])
    
    # Loop through each base URL
    for base_url in base_urls:
        page = 1
        while True:
            url = base_url if page == 1 else f'{base_url}?page={page}'
            print(f"Fetching data from {url}...")
            try:
                # Fetch and process properties from the current page
                fetch_properties(url, writer)
                
                # Increment page number for next iteration
                page += 1
                
                # Check for next page existence (stop condition)
                html_text = requests.get(url).text
                soup = BeautifulSoup(html_text, 'html.parser')
                next_button_div = soup.find('div', class_='mt-4 flex w-full flex-row items-center justify-center space-x-1 md:space-x-3')
                if next_button_div:
                     next_button = soup.find('svg', class_='fill-current transform -rotate-90 inline-block text-secondary w-3')
                else:
                     next_button = None
                     
                if not next_button:
                    break
            except Exception as e:
                print(f"Error fetching properties from {url}: {e}")
                break

print('File saved successfully')
