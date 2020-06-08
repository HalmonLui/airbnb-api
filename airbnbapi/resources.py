from airbnbapi import api
from flask_restful import Resource, reqparse
from flask import jsonify
# @app.route('/')
# def index():
#     return 'Hello World!'

# @app.route('/getListings')
# parser = reqparse.RequestParser()
# parser.add_argument('city', required=True)
# parser.add_argument('state', required=True)
# parser.add_argument('checkin')
# parser.add_argument('checkout')
# parser.add_argument('adults')
# parser.add_argument('page')
# parser.add_argument('search_type')
# args = parser.parse_args(strict=True)

# api.add_resource(UserAPI, '/users/<int:id>', endpoint = 'user')
# class ListingsAPI(Resource):
#     def get(self, id):
#         pass
#
#     def put(self, id):
#         pass
#
#     def delete(self, id):
#         pass



class Hello(Resource):
    def get(self):

        return jsonify({'message': 'hello world'})

    # Corresponds to POST request
    def post(self):

        data = request.get_json()     # status code
        return jsonify({'data': data}), 201


# another resource to calculate the square of a number
class Square(Resource):

    def get(self, num):

        return jsonify({'square': num**2})


# adding the defined resources along with their corresponding urls
api.add_resource(Hello, '/')
api.add_resource(Square, '/square/<int:num>')
