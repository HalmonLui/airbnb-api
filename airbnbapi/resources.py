from airbnbapi import api
from flask_restful import Resource, reqparse
from flask import jsonify
from . import controllers

class Index(Resource):
    def get(self):
        return jsonify({'message': 'Unofficial Airbnb API, visit https://github.com/HalmonLui/airbnb-api for more information'})


# Get Airbnb Listings
class ListingsAPI(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('city', required=True)
        parser.add_argument('state', required=True)
        parser.add_argument('checkin')
        parser.add_argument('checkout')
        parser.add_argument('adults', default='1')
        parser.add_argument('page', default='0')
        parser.add_argument('search_type', default='pagination')
        parser.add_argument('min_price')
        parser.add_argument('max_price')
        parser.add_argument('flexible_cancellation')
        parser.add_argument('instant_booking')
        parser.add_argument('work_trip')
        parser.add_argument('superhost')
        parser.add_argument('neighborhoods')
        args = parser.parse_args(strict=True)
        return controllers.get_listings(args)


# Get Neighborhoods and IDs
class NeighborhoodsAPI(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('city', required=True)
        parser.add_argument('state', required=True)
        args = parser.parse_args(strict=True)
        return controllers.get_neighborhoods(args)


# adding the defined resources along with their corresponding urls
api.add_resource(Index, '/')
api.add_resource(ListingsAPI, '/getListings')
# api.add_resource(SpecificListingAPI, '/getListing/<int:num>')
api.add_resource(NeighborhoodsAPI, '/getNeighborhoods')
