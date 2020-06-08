from airbnbapi import api
from flask_restful import Resource, reqparse
from flask import jsonify
from . import controllers

class Hello(Resource):
    def get(self):

        return jsonify({'message': 'hello world'})

    # Corresponds to POST request
    def post(self):

        data = request.get_json()     # status code
        return jsonify({'data': data}), 201


# # another resource to calculate the square of a number
# class Square(Resource):
#
#     def get(self, num):
#
#         return jsonify({'square': num**2})

# Get Airbnb Listings
class ListingsAPI(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('city', required=True)
        parser.add_argument('state', required=True)
        parser.add_argument('checkin')
        parser.add_argument('checkout')
        parser.add_argument('adults')
        parser.add_argument('page')
        parser.add_argument('search_type')
        args = parser.parse_args(strict=True)
        return controllers.get_listings(args)


# adding the defined resources along with their corresponding urls
api.add_resource(Hello, '/')
# api.add_resource(Square, '/square/<int:num>')
api.add_resource(ListingsAPI, '/getListings')
