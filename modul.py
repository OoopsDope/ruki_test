import requests
from bs4 import BeautifulSoup
import re


def extract_phone_numbers_from_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        phone_numbers = []
        phone_anchors = soup.find_all('a', href=re.compile(r'tel:'))
        phone_numbers += [re.sub(
            r'\D', '', anchor.get('href')) for anchor in phone_anchors]
        phone_divs = soup.find_all('div', class_='phone-number__number')
        phone_numbers += [re.sub(
            r'\D', '', div.get_text()) for div in phone_divs]
        return phone_numbers
    except Exception as e:
        print(f"Error extracting phone numbers from {url}: {e}")
        return []


def get_phone_numbers_from_organization(organization):
    url = organization['website'] + organization['contacts_page']
    numbers = extract_phone_numbers_from_page(url)
    return numbers


if __name__ == "__main__":
    organizations = [
        {'website': 'https://hands.ru', 'contacts_page': '/company/about'},
        {'website': 'https://repetitors.info', 'contacts_page': '/contacts'},
    ]
    all_numbers = []
    for org in organizations:
        numbers = get_phone_numbers_from_organization(org)
        all_numbers.extend(numbers)
    print("Phone numbers found:")
    for number in all_numbers:
        print(number)
