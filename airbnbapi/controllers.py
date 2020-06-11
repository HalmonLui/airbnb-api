import json, requests, pprint, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from . import helpers

def get_listings(args):
    # Build the URL
    URL = helpers.build_url(args)
    print('URL', URL, flush=True)

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
    spans = soup.find_all('button')
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
            listing_type = None
            rating = None
            num_reviews = None

            # Some have a discounted price so we only want the actual price per night
            price_per_night = text.rsplit('$', 1)[1]
            price_per_night = price_per_night.replace(' / night', '')
            price_per_night = ' '.join(price_per_night.split())

            # Gets amenities like Wifi/Kitching/Free Parking
            amenities_element = span.parent.parent.parent.previous_sibling
            if amenities_element:
                amenities = amenities_element.get_text()
                amenities = amenities.split(' · ')

            # Gets gusts, bedrooms, baths
            housing_info_element = span.parent.parent.parent.previous_sibling.previous_sibling
            if housing_info_element:
                housing_info = housing_info_element.get_text()
                housing_info = housing_info.split(' · ')

            # Gets is_superhost, listing_type, rating, and num_reviews
            # listing_info = span.parent.parent.parent.previous_sibling.previous_sibling.previous_sibling.previous_sibling.children
            listing_info = None
            if listing_info:
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


def get_neighborhoods(args):
    # Build the URL
    URL = helpers.build_url(args)

    # Prepare the webdriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(500, 951) # Manually set window size so we can find by class name later

    # Control the page to show all neighborhoods
    driver.get(URL)
    time.sleep(1) # Since we are in a browser, the javascript takes time to run so let's give it time
    more_filters_button = driver.find_elements_by_xpath('//*[@id="filter-menu-chip-group"]/div[2]/button')[0] # Dangerous, location of filter button may change
    more_filters_button.click()
    time.sleep(1) # Waiting for page's js to run
    show_all_neighborhoods_button = driver.find_elements_by_class_name('_6lth7f')[5] # Dangerous, classnames automatically change based on window dimensions, they might also rotate every once and a while for airbnb security
    show_all_neighborhoods_button.click()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit() # Close driver so we don't have idle processes

    # Get neighborhoods and IDs from page
    neighborhoods = []
    inputs = soup.find_all('input')
    for i in inputs:
        ids = i.get('id')
        if ids and 'neighborhood_ids' in ids:
            neighborhood_id = ids.replace('neighborhood_ids-', '')
            neighborhood = i.get('name')
            neighborhoods.append({'neighborhood': neighborhood, 'neighborhood_id': neighborhood_id})

    return neighborhoods, 200
