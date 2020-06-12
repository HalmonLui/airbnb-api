import json, requests, pprint, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from . import helpers

def get_listings(args):
    # Build the URL
    URL = helpers.build_url(args)

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

    # GET SUPERHOST, LISTING_TYPE, RATING, NUM_REVIEWS
    # This only works sometimes, airbnb must load their frontend slightly differently every fetch
    divs = soup.find_all('div')
    counter = 0
    for div in divs:
        if counter < len(listings) and div.get_text() == listings[counter]['listing_name']:
            is_superhost = 'False'
            listing_type = ''
            rating = None
            num_reviews = '0'

            listing_info = div.previous_sibling
            if listing_info:
                for child in listing_info:
                    if 'Entire ' in child.get_text() or 'Private ' in child.get_text():
                        listing_type = child.get_text()
                    elif 'SUPERHOST' in child.get_text():
                        is_superhost = 'True'
                    elif '(' and ')' in child.get_text():
                        for c in child:
                            split_rating = c.get_text().split()
                            rating = split_rating[0]
                            num_reviews = split_rating[1].replace('(', '')
                            num_reviews = num_reviews.replace(')', '')

            listings[counter]['is_superhost'] = is_superhost
            listings[counter]['listing_type'] = listing_type
            listings[counter]['rating'] = rating
            listings[counter]['num_reviews'] = num_reviews

            counter += 1

    # GET PRICE PER NIGHT, AMENITIES, HOUSING_INFO
    counter = 0
    for span in spans:
        text = span.get_text()
        if text and '/ night' in text and 'total' not in text:
            price_per_night = None
            amenities = []
            housing_info = []

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

            listings[counter]['price_per_night'] = price_per_night
            listings[counter]['amenities'] = amenities
            listings[counter]['housing_info'] = housing_info

            counter += 1

    return listings, 200


def get_amenities():
    # Build URL
    base_url = 'https://www.airbnb.com/s/homes?query='
    URL = base_url + 'Boston' + '%2C%20' + 'MA' # Can use any city/state

    # Prepare the webdriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(500, 951) # Manually set window size so we can find by class name later

    # Control the page to show all amenities
    driver.get(URL)
    time.sleep(1) # Since we are in a browser, the javascript takes time to run so let's give it time
    error_message = None
    more_filters_button = driver.find_elements_by_xpath('//*[@id="filter-menu-chip-group"]/div[2]/button')[0] # Dangerous, location of filter button may change
    if more_filters_button:
        more_filters_button.click()
        time.sleep(1) # Waiting for page's js to run
        show_all_amenities = driver.find_elements_by_class_name('_6lth7f')[1] # Dangerous, classnames automatically change based on window dimensions, they might also rotate every once and a while for airbnb security
        if show_all_amenities:
            show_all_amenities.click()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        else:
            error_message = 'Unable to access amenities'
    else:
        error_message = 'Unable to access filter button'

    driver.quit() # Close driver so we don't have idle processes

    # Return error message if we cannot access airbnb's amenities
    if error_message:
        return {'error': error_message}, 400

    # Get amenities and IDs from page
    amenities = []
    inputs = soup.find_all('input')
    for i in inputs:
        ids = i.get('id')
        if ids and 'amenities' in ids:
            amenity_id = ids.replace('amenities-', '')
            amenity = i.get('name')
            amenities.append({'amenity': amenity, 'amenity_id': amenity_id})

    return amenities, 200


def get_accessibilities():
    # Build URL
    base_url = 'https://www.airbnb.com/s/homes?query='
    URL = base_url + 'Boston' + '%2C%20' + 'MA' # Can use any city/state

    # Prepare the webdriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(500, 951) # Manually set window size so we can find by class name later

    # Control the page to show all accessibilities
    driver.get(URL)
    time.sleep(1) # Since we are in a browser, the javascript takes time to run so let's give it time
    error_message = None
    more_filters_button = driver.find_elements_by_xpath('//*[@id="filter-menu-chip-group"]/div[2]/button')[0] # Dangerous, location of filter button may change
    if more_filters_button:
        more_filters_button.click()
        time.sleep(1) # Waiting for page's js to run
        show_all_accessibilities = driver.find_elements_by_class_name('_6lth7f')[1] # Dangerous, classnames automatically change based on window dimensions, they might also rotate every once and a while for airbnb security
        if show_all_accessibilities:
            show_all_accessibilities.click()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        else:
            error_message = 'Unable to access accessibilities'
    else:
        error_message = 'Unable to access filter button'

    driver.quit() # Close driver so we don't have idle processes

    # Return error message if we cannot access airbnb's accessibilities
    if error_message:
        return {'error': error_message}, 400

    # Get accessibilities and IDs from page
    accessibilities = []
    inputs = soup.find_all('input')
    for i in inputs:
        ids = i.get('id')
        if ids and 'amenities' in ids:
            accessibility_id = ids.replace('amenities-', '')
            accessibility = i.get('name')
            accessibilities.append({'accessibility': accessibility, 'accessibility_id': accessibility_id})

    return accessibilities, 200


def get_facilities():
    # Build URL
    base_url = 'https://www.airbnb.com/s/homes?query='
    URL = base_url + 'Boston' + '%2C%20' + 'MA' # Can use any city/state

    # Prepare the webdriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(500, 951) # Manually set window size so we can find by class name later

    # Control the page to show all facilities
    driver.get(URL)
    time.sleep(1) # Since we are in a browser, the javascript takes time to run so let's give it time
    error_message = None
    more_filters_button = driver.find_elements_by_xpath('//*[@id="filter-menu-chip-group"]/div[2]/button')[0] # Dangerous, location of filter button may change
    if more_filters_button:
        more_filters_button.click()
        time.sleep(1) # Waiting for page's js to run
        show_all_facilities = driver.find_elements_by_class_name('_6lth7f')[2] # Dangerous, classnames automatically change based on window dimensions, they might also rotate every once and a while for airbnb security
        if show_all_facilities:
            show_all_facilities.click()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        else:
            error_message = 'Unable to access facilities'
    else:
        error_message = 'Unable to access filter button'

    driver.quit() # Close driver so we don't have idle processes

    # Return error message if we cannot access airbnb's facilities
    if error_message:
        return {'error': error_message}, 400

    # Get amenities and IDs from page
    facilities = []
    inputs = soup.find_all('input')
    for i in inputs:
        ids = i.get('id')
        if ids and 'amenities' in ids:
            facility_id = ids.replace('amenities-', '')
            facility = i.get('name')
            facilities.append({'facility': facility, 'facility_id': facility_id})

    return facilities, 200


def get_property_types():
    # Build URL
    base_url = 'https://www.airbnb.com/s/homes?query='
    URL = base_url + 'Boston' + '%2C%20' + 'MA' # Can use any city/state

    # Set up headless chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(500, 951) # Manually set window size so we can find by class name later

    # Control page to show property types
    driver.get(URL)
    time.sleep(1) # Since we are in a browser, the javascript takes time to run so let's give it time
    error_message = None
    more_filters_button = driver.find_elements_by_xpath('//*[@id="filter-menu-chip-group"]/div[2]/button')[0]
    if more_filters_button:
        more_filters_button.click()
        time.sleep(1) # Waiting for page's js to run
        show_all_unique_stays_button = driver.find_elements_by_class_name('_6lth7f')[4] # Dangerous, classnames automatically change based on window dimensions, they might also rotate every once and a while for airbnb security
        if show_all_unique_stays_button:
            show_all_unique_stays_button.click()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        else:
            error_message = 'Unable to access unique stays'

        show_all_property_types_button = driver.find_elements_by_class_name('_6lth7f')[3] # Dangerous, classnames automatically change based on window dimensions, they might also rotate every once and a while for airbnb security
        if show_all_property_types_button:
            show_all_property_types_button.click()
            property_soup = BeautifulSoup(driver.page_source, 'html.parser')
        else:
            error_message = 'Unable to access property types'
    else:
        error_message = 'Unable to access filter button'

    driver.quit() # Close driver to prevent idle processes

    # Return error message if we cannot access property types
    if error_message:
        return {'error': error_message}, 400

    property_types = []
    inputs = property_soup.find_all('input')
    for i in inputs:
        ids = i.get('id')
        if ids and 'property_type_id' in ids:
            property_type_id = ids.replace('property_type_id-', '')
            property_type = i.get('name')
            property_types.append({'property_type': property_type, 'property_type_id': property_type_id})

    return property_types, 200


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
    error_message = None
    more_filters_button = driver.find_elements_by_xpath('//*[@id="filter-menu-chip-group"]/div[2]/button')[0] # Dangerous, location of filter button may change
    if more_filters_button:
        more_filters_button.click()
        time.sleep(1) # Waiting for page's js to run
        show_all_neighborhoods_button = driver.find_elements_by_class_name('_6lth7f')[5] # Dangerous, classnames automatically change based on window dimensions, they might also rotate every once and a while for airbnb security
        if show_all_neighborhoods_button:
            show_all_neighborhoods_button.click()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        else:
            error_message = 'Unable to access neighborhoods'
    else:
        error_message = 'Unable to access filter button'

    driver.quit() # Close driver so we don't have idle processes

    # Return error message if we cannot access airbnb's neighborhoods
    if error_message:
        return {'error': error_message}, 400

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


def get_languages():
    # Build URL
    base_url = 'https://www.airbnb.com/s/homes?query='
    URL = base_url + 'Boston' + '%2C%20' + 'MA' # Can use any city/state

    # Set up headless chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(500, 951) # Manually set window size so we can find by class name later

    # Control page to show languages
    driver.get(URL)
    time.sleep(1) # Since we are in a browser, the javascript takes time to run so let's give it time
    error_message = None
    more_filters_button = driver.find_elements_by_xpath('//*[@id="filter-menu-chip-group"]/div[2]/button')[0]
    if more_filters_button:
        more_filters_button.click()
        time.sleep(1) # Waiting for page's js to run
        show_all_languages_button = driver.find_elements_by_class_name('_6lth7f')[6] # Dangerous, classnames automatically change based on window dimensions, they might also rotate every once and a while for airbnb security
        if show_all_languages_button:
            show_all_languages_button.click()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        else:
            error_message = 'Unable to access languages'
    else:
        error_message = 'Unable to access filter button'

    driver.quit() # Close driver to prevent idle processes

    # Return error message if we cannot access languages
    if error_message:
        return {'error': error_message}, 400

    languages = []
    inputs = soup.find_all('input')
    for i in inputs:
        ids = i.get('id')
        if ids and 'languages' in ids:
            language_id = ids.replace('languages-', '')
            language = i.get('name')
            languages.append({'language': language, 'language_id': language_id})

    return languages
