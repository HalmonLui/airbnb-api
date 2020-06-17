from urllib.parse import urlencode, quote

def build_url(args):
    URL = 'https://www.airbnb.com/s/homes?'

    params = {}
    # Add pagination
    if args['search_type']:
        params['search_type'] = args['search_type']
        if  args['search_type'] == 'pagination' and args['page']:
            items_offset = str(int(args['page']) * 20)
            params['items_offset'] = items_offset

    # Add location, these are required fields
    if args['city'] and args['state']:
        address = args['city'] + ', ' +  args['state']
        params['query'] = address

    # Add logistics
    if args['checkin'] and args['checkout']:
        params['checkin'] = args['checkin']
        params['checkout'] = args['checkout']

    # Add adults, there is default='1' but check just for safety
    if args['adults']:
        params['adults'] = args['adults']

    # Add min_price
    if args['min_price']:
        params['min_price'] = args['min_price']

    # Add max_price
    if args['max_price']:
        params['max_price'] = args['max_price']

    # Add min_bedrooms
    if args['min_beds']:
        params['min_beds'] = args['min_beds']

    # Add min_bedrooms
    if args['min_bedrooms']:
        params['min_bedrooms'] = args['min_bedrooms']

    # Add min_bathrooms
    if args['min_bathrooms']:
        params['min_bathrooms'] = args['min_bathrooms']

    # Add flexible_cancellation
    if args['flexible_cancellation']:
        params['flexible_cancellation'] = args['flexible_cancellation']

    # Add instant booking
    if args['instant_booking']:
        params['ib'] = args['instant_booking']

    # Add work trip
    if args['work_trip']:
        params['work_trip'] = args['work_trip']

    # Add superhost
    if args['superhost']:
        params['superhost'] = args['superhost']

    # Add amenities
    if args['amenities']:
        amenities = args['amenities'].split(',')
        if 'amenities[]' in params and params['amenities[]']:
            params['amenities[]'].extend(amenities)
        else:
            params['amenities[]'] = amenities

    # Add accessibilities
    if args['accessibilities']:
        accessibilities = args['accessibilities'].split(',')
        if 'amenities[]' in params and params['amenities[]']:
            params['amenities[]'].extend(accessibilities)
        else:
            params['amenities[]'] = accessibilities

    # Add facilities
    if args['facilities']:
        facilities = args['facilities'].split(',')
        if 'amenities[]' in params and params['amenities[]']:
            params['amenities[]'].extend(facilities)
        else:
            params['amenities[]'] = facilities

    # Add property types
    if args['property_types']:
        property_types = args['property_types'].split(',')
        params['property_type_id[]'] = property_types

    # Add house_rules
    if args['house_rules']:
        house_rules = args['house_rules'].split(',')
        if 'amenities[]' in params and params['amenities[]']:
            params['amenities[]'].extend(house_rules)
        else:
            params['amenities[]'] = house_rules

    # Add neighborhoods
    if args['neighborhoods']:
        neighborhoods = args['neighborhoods'].split(',')
        params['neighborhood_ids[]'] = neighborhoods

    # Add languages
    if args['languages']:
        languages = args['languages'].split(',')
        params['languages[]'] = languages

    URL += urlencode(params, True, quote_via=quote)
    # For debugging let's see the URL
    print(URL, flush=True)
    return URL
