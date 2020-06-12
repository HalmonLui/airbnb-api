# Unofficial Airbnb REST Api

This is an unofficial airbnb RESTful api which scrapes the [airbnb site](https://www.airbnb.com/) to retrieve data

Application was built with Python3, Flask, BeautifulSoup, and Selenium.

Warning: Using this application may be against Airbnb's terms of services.


## Install

    git clone https://github.com/HalmonLui/airbnb-api.git
    cd airbnb-api
    pip -r requirements.txt

  Note: For some endpoints, you need selenium with the Chrome driver in your PATH. Follow [this tutorial](https://zwbetz.com/download-chromedriver-binary-and-add-to-your-path-for-automated-functional-testing/) to learn how.

## Run the app

    export FLASK_APP=airbnbapi
    flask run


# REST API

## Get Listings

### Request

`GET /getListings`

    curl -X GET 'http://localhost:5000/getListings?city=Boston&state=MA'

### Parameters

  - **city** *required, str*\
  Valid city, ex: Boston
  - **state** *required, str*\
    Valid state code, ex: MA
  - **checkin** *optional, str*\
    Checkin date, YYYY-MM-DD
  - **checkout** *optional, str*\
    Checkout date, YYYY-MM-DD
  - **adults** *optional, int, default is 1*\
    Number of adults
  - **page** *optional, int, default is 0*\
    Each page shows 20 items at a time
  - **min_price** *optional, int*\
    Minimum price per night
  - **max_price** *optional, int*\
    Maximum price per night
  - **min_beds** *optional, int*\
    Minimum number of beds
  - **min_bedrooms** *optional, int*\
    Minimum number of bedrooms
  - **min_bathrooms** *optional, int*\
    Minimum number of bathrooms
  - **flexible_cancellation** *optional, bool*\
    Stay has flexible cancellation
  - **instant_booking** *optional, bool*\
    Book without waiting for host approval
  - **work_trip** *optional, bool*\
    Traveling for work, 5 star ratings from business travelers
  - **superhost** *optional, bool*\
    Host is a superhost
  - **amenities** *optional*\
    Comma separated list of amenity_ids (can retrieve from /getAmenities endpoint), ex: 44,45
  - **accessibility** *optional*\
    Comma separated list of accessibility_ids (can retrieve from /getAccessibilities endpoint) ex:
  - **facilities** *optional*\
    Comma separated list of facility_ids (can retrieve from /getFacilities endpoint), ex: 7,9
  - **property_types** *optional*\
    Comma separated list of property_type_ids (can retrieve from /getPropertyTypes endpoint), ex: 8,5
  - **neighborhoods** *optional*\
    Comma separated list of neighborhood_ids (can retrieve from /getNeighborhoods endpoint), ex: 578,579
  - **languages** *optional*\
    Comma separated list of language_ids (can retrieve from /getLanguages endpoint), ex: 1,2

### Response
```json
  [
      {
          "listing_name": "Super Spacious Listing For My Airbnb API",
          "url": "https://www.airbnb.com/rooms/1858?adults=1&previous_page_section_name=100&federated_search_id=f41f2c-39b5-4fce-a928-8540423f1",
          "price_per_night": "27",
          "amenities": [
              "Wifi",
              "Kitchen"
          ],
          "housing_info": [
              "2 guests",
              "1 bedroom",
              "1 bed",
              "2 shared baths"
          ],
          "is_superhost": "True",
          "listing_type": "Private room",
          "rating": "4.89",
          "num_reviews": "434"
      },
      {
          "listing_name": "Downtown Room",
          "url": "https://www.airbnb.com/rooms/1562?adults=1&previous_page_section_name=100&federated_search_id=fbf2c-39b5-ce-a928-853f1",
          "price_per_night": "39",
          "amenities": [
              "Free parking",
              "Wifi",
              "Kitchen"
          ],
          "housing_info": [
              "3 guests",
              "1 bedroom",
              "2 beds",
              "2 shared baths"
          ],
          "is_superhost": "True",
          "listing_type": "Private room",
          "rating": "4.89",
          "num_reviews": "615"
      },
      ...
  ]
```

## Get Deep Listings

### Request

`Get /getDeepListings`

    curl -X GET 'http://localhost:5000/getListings?city=Boston&state=MA'

### Response
```json
In progress...
```

## Get Specific Listing

### Request

`GET /getListing/<id>`

    curl -X GET 'http://localhost:5000/getListing?id=123456'

### Response
```json
In progress...
```

## Get Amenities
Airbnb uses unique ids for each amenity, these are needed to query listings by host amenities.\
Note: If endpoint doesn't work, make sure you [installed](https://github.com/HalmonLui/airbnb-api#install) correctly.
### Request

`GET /getAmenities`

    curl -X GET 'http://localhost:5000/getAmenities'

### Response
```json
  [
      {
          "amenity": "Kitchen",
          "amenity_id": "8"
      },
      {
          "amenity": "Shampoo",
          "amenity_id": "41"
      },
      {
          "amenity": "Heating",
          "amenity_id": "30"
      },
      {
          "amenity": "Air conditioning",
          "amenity_id": "5"
      },
      {
          "amenity": "Washer",
          "amenity_id": "33"
      },
      ...
  ]
```

## Get Accessibilities
Airbnb uses unique ids for each accessibility, these are needed to query listings by host accessibility.\
Note: If endpoint doesn't work, make sure you [installed](https://github.com/HalmonLui/airbnb-api#install) correctly.
### Request

`GET /getAccessibilities`

    curl -X GET 'http://localhost:5000/getAccessibilities'

### Response
```json
  [
      {
          "accessibility": "No stairs or steps to enter",
          "accessibility_id": "110"
      },
      {
          "accessibility": "Well-lit path to entrance",
          "accessibility_id": "113"
      },
      {
          "accessibility": "Wide entrance for guests",
          "accessibility_id": "111"
      },
      {
          "accessibility": "Step-free path to entrance",
          "accessibility_id": "112"
      },
      {
          "accessibility": "Wide hallways",
          "accessibility_id": "109"
      },
      ...
  ]
```

## Get Facilities
Airbnb uses unique ids for each facility, these are needed to query listings by host facilities.\
Note: If endpoint doesn't work, make sure you [installed](https://github.com/HalmonLui/airbnb-api#install) correctly.
### Request

`GET /getFacilities`

    curl -X GET 'http://localhost:5000/getFacilities'

### Response
```json
  [
      {
          "facility": "Free parking on premises",
          "facility_id": "9"
      },
      {
          "facility": "Gym",
          "facility_id": "15"
      },
      {
          "facility": "Hot tub",
          "facility_id": "25"
      },
      {
          "facility": "Pool",
          "facility_id": "7"
      }
  ]
```

## Get Property Types
Airbnb uses unique property type ids for each property type and unique stay, these are needed to query listings by host property type.\
Note: If endpoint doesn't work, make sure you [installed](https://github.com/HalmonLui/airbnb-api#install) correctly.
### Request

`GET /getPropertyTypes`

    curl -X GET 'http://localhost:5000/getPropertyTypes'

### Response
```json
  [
      {
          "property_type": "House",
          "property_type_id": "2"
      },
      {
          "property_type": "Apartment",
          "property_type_id": "1"
      },
      {
          "property_type": "Bed and breakfast",
          "property_type_id": "3"
      },
      {
          "property_type": "Boutique hotel",
          "property_type_id": "43"
      },
      {
          "property_type": "Bungalow",
          "property_type_id": "38"
      },
      ...
  ]
```

## Get Neighborhoods
Airbnb uses unique neighborhood ids for each neighborhood, these are needed to query listings by neighborhood.\
Note: If endpoint doesn't work, make sure you [installed](https://github.com/HalmonLui/airbnb-api#install) correctly.
### Request

`GET /getNeighborhoods`

    curl -X GET 'http://localhost:5000/getNeighborhoods?city=Boston&state=MA'

### Parameters

  - **city** *required*\
  Valid city, ex: Boston
  - **state** *required*\
    Valid state code, ex: MA

### Response
```json
  [
    {
      "neighborhood": "Allston-Brighton",
      "neighborhood_id": "578"
    },
    {
      "neighborhood": "East Boston",
      "neighborhood_id": "579"
    },
    {
      "neighborhood": "Winthrop",
      "neighborhood_id": "580"
    },
    {
      "neighborhood": "Theater District",
      "neighborhood_id": "453"
    },
    {
      "neighborhood": "Cambridge",
      "neighborhood_id": "581"
    },
    ...
  ]
```

## Get Languages
Airbnb uses unique language ids for each language, these are needed to query listings by host language.\
Note: If endpoint doesn't work, make sure you [installed](https://github.com/HalmonLui/airbnb-api#install) correctly.
### Request

`GET /getLanguages`

    curl -X GET 'http://localhost:5000/getLanguages'

### Response
```json
  [
    {
      "language": "English",
      "language_id": "1"
    },
    {
      "language": "French",
      "language_id": "2"
    },
    {
      "language": "German",
      "language_id": "4"
    },
    {
      "language": "Japanese",
      "language_id": "8"
    },
    {
      "language": "Italian",
      "language_id": "16"
    },
    ...
  ]
```
