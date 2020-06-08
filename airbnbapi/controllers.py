import json, requests, pprint
from . import helpers
from bs4 import BeautifulSoup

def get_listings(args):
    # Build the URL
    URL = helpers.build_get_listings_url(args)

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    listings = []

    links = soup.find_all('a')
    # GET LISTING NAME AND URL
    counter = 0
    for link in links:
        # We just want to add real listings, not all link names
        if link.get('data-check-info-section'):
            listing_name = link.get('aria-label')
            url = 'https://www.airbnb.com' + link.get('href')
            listings.append({'listing_name': listing_name, 'url': url})
            counter += 1

    # GET TOTAL PRICE
    spans = soup.find_all('span')
    counter = 0
    for span in spans:
        text = span.get_text()
        if text and 'total' in text:
            total = text.replace('$', '')
            total = total.replace(' total', '')
            listings[counter]['total_price'] = total
            counter += 1

    # GET PRICE PER NIGHT, AMENITIES, HOUSING_INFO, SUPERHOST, LISTING_TYPE, RATING, NUM_REVIEWS
    counter = 0
    for span in spans:
        text = span.get_text()
        if text and '/ night' in text and 'total' not in text:
            price_per_night = None
            amenities = []
            housing_info = []
            is_superhost = 'False'
            listing_type = ''
            rating = None
            num_reviews = '0'

            # Some have a discounted price so we only want the actual price per night
            price_per_night = text.rsplit('$', 1)[1]
            price_per_night = price_per_night.replace(' / night', '')
            price_per_night = ' '.join(price_per_night.split())

            # Gets amenities like Wifi/Kitching/Free Parking
            amenities = span.parent.parent.parent.previous_sibling.get_text()
            amenities = amenities.split(' · ')

            # Gets gusts, bedrooms, baths
            housing_info = span.parent.parent.parent.previous_sibling.previous_sibling.get_text()
            housing_info = housing_info.split(' · ')

            # Gets is_superhost, listing_type, rating, and num_reviews
            listing_info = span.parent.parent.parent.previous_sibling.previous_sibling.previous_sibling.previous_sibling.children
            for child in listing_info:
                child_text = child.get_text()
                if 'Entire ' in child_text or 'Private ' in child_text:
                    listing_type = child_text
                elif 'SUPERHOST' in child_text:
                    is_superhost = 'True'
                elif '(' and ')' in child_text:
                    for c in child:
                        split_rating = c.get_text().split()
                        rating = split_rating[0]
                        num_reviews = split_rating[1].replace('(', '')
                        num_reviews = num_reviews.replace(')', '')

            listings[counter]['price_per_night'] = price_per_night
            listings[counter]['amenities'] = amenities
            listings[counter]['housing_info'] = housing_info
            listings[counter]['is_superhost'] = is_superhost
            listings[counter]['listing_type'] = listing_type
            listings[counter]['rating'] = rating
            listings[counter]['num_reviews'] = num_reviews
            counter += 1

    return listings, 200
