import csv
from bs4 import BeautifulSoup
import requests



url = 'https://www.buyrentkenya.com/houses-for-sale'



html_text = requests.get(url).text

print(url)


# soup = BeautifulSoup(html_text, 'html.parser')

# properties = soup.find_all('div', class_='relative w-full overflow-hidden rounded-2xl bg-white')

# for prop in properties:

#     price_tag = prop.find('p', class_='text-xl font-bold leading-7 text-grey-900').find('a', class_='no-underline')

#     price_text= price_tag.text if price_tag else None
    
#     print(price_text)







