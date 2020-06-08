def build_get_listings_url(args):
    baseurl = 'https://www.airbnb.com/s/homes?'

    # Add pagination
    if 'search_type' in args and args['search_type']:
        URL = baseurl + 'search_type=' + args['search_type']
        if  args['search_type'] == 'pagination' and 'page' in args and args['page']:
            items_offset = str(int(args['page']) * 20)
            URL = URL + '&items_offset=' + items_offset

    # Add location, these are required fields
    query = args['city'] + '%2C%20' + args['state']
    URL = URL + '&query=' + query

    # Add logistics
    if 'checkin' in args and args['checkin'] and 'checkout' in args and args['checkout']:
        URL = URL + '&checkin=' + args['checkin'] + '&checkout=' + args['checkout']

    # Add adults, there is default='1' but check just for safety
    if 'adults' in args and args['adults']:
        URL = URL + '&adults=' + args['adults']

    return URL
