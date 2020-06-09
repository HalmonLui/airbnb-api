# Unofficial Airbnb Scraper REST Api

This is an unofficial airbnb RESTful api which scrapes the airbnb site to retrieve data

Application was built with Python3 and Flask.

Warning: Using this application may be against Airbnb's terms of services.


## Install

    git clone https://github.com/HalmonLui/airbnb-api.git
    cd airbnb-api
    pip -r requirements.txt

## Run the app

    export FLASK_APP=airbnbapi
    flask run

# REST API

## Get Listings

### Request

`GET /getListings`

    curl -X GET 'http://localhost:5000/getListings?city=Boston&state=MA'

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

`Get /getDeepListings/`

    curl -X GET 'http://localhost:5000/getListings?city=Boston&state=MA'

### Response


## Get Specific Listing

### Request

`GET /getListing/<id>`

    curl -X GET 'http://localhost:5000/getListing?id=123456'

### Response
