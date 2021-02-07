import requests
from bs4 import BeautifulSoup
import base64
import cv2
import numpy as np
import pytesseract
import csv

base_url = 'https://www.property24.com'


def determine_url(url):
    if not url.startswith('https://www.property24.com'):
        url = base_url + url

    return url


def parse_page(page_url):
    url = determine_url(page_url)
    print('Parsing: ' + url)
    page_content = requests.get(url)

    return BeautifulSoup(page_content.content, 'html.parser')


def parse_suberb_page(suburb_url):
    suburb_page = parse_page(suburb_url)

    link_contents = suburb_page.find('div', class_='p24_alphabet')

    for link in link_contents.find_all('a', href=True):
        if link['href'].startswith('/property-values'):
            street_page_link = link['href']
            parse_street_page(street_page_link)


def parse_street_page(page_url):
    page = parse_page(page_url)

    pager = page.find('div', class_='p24_pager')
    rows = page.find('table').find_all('tr', class_='p24_markerRow')

    print('Number of addresses found:', len(rows))

    for row in rows:
        cells = row.find_all("td")
        address_column = cells[1]
        view_column = cells[4]

        address = address_column.find('a').get_text()
        address = address.replace(',', '')
        address_url = view_column.find('a')

        parse_address_page(address, address_url['href'])

    if pager is not None:
        next_page_url = pager.find('a', class_='pull-right')
        if next_page_url['href'].startswith('https'):
            print('Going to next page')
            parse_street_page(next_page_url['href'])


def parse_address_page(address, address_url):
    page = parse_page(address_url)
    print('Finding data for', address)

    images = page.find_all('img', class_='p24_raiseImage')

    try:
        sold = extract_image_text(images[0])
    except:
        sold = 'Sold date not found'

    try:
        price = extract_image_text(images[1])
    except:
        price = 'Sold price not found'

    write_data(determine_url(address_url), address, sold, price)


def extract_image_text(image):
    image_data = image['src'].split(',')
    base64_string = image_data[1]

    text = ''
    shape_value = 2

    while text == '' and shape_value > 0:
        nparr = np.frombuffer(base64.b64decode(base64_string), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        kernel = np.ones((shape_value, shape_value), np.uint8)
        img = cv2.erode(thresh, kernel, iterations=1)

        text = pytesseract.image_to_string(img).strip()
        text = text.replace(',', '')

        shape_value -= 1

    if text == '':
        text = 'No value found'

    return text


def write_data(url, address, sold, price):
    print('Writing data...')
    with open('properties.csv', 'a+') as properties:
        property_writer = csv.writer(properties, delimiter=',', quoting=csv.QUOTE_NONE)
        property_writer.writerow([address, sold, price, url])


if __name__ == '__main__':
    suburb_url = 'https://www.property24.com/property-values/de-bron/bellville/western-cape/9440'
    parse_suberb_page(suburb_url)
