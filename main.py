from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
# import ast

app = Flask(__name__)
api = Api(app)

# /users
users_path = 'C:\\Users\\PC\\Desktop\\Data\\Users.csv'
# /locations
locations_path = 'C:\\Users\\PC\\Desktop\\Data\\Locations.csv'


class Users(Resource):
    def get(self):
        data = pd.read_csv(users_path)
        data = data.to_dict()
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('usrname', type=str, required=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('city', type=str, required=True)
        args = parser.parse_args()
        data = pd.read_csv(users_path)

        if args['usrname'] in list(data['username']):
            return {'message': f"{args['usrname']} already exists"}, 409
        else:
            data = data.append({'username': args['usrname'], 'name': args['name'], 'city': args['city'],
                                'locations': []}, ignore_index=True)
            data.to_csv(users_path, index=False)
            return {'data': data.to_dict()}, 200

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('usrnam', type=str, required=True)
        args = parser.parse_args()
        data = pd.read_csv(users_path)

        if args['usrnam'] in list(data['username']):
            data = data[data['username'] != args['usrnam']]
            data.to_csv(users_path, index=False)
            return {'data': data.to_dict()}, 200
        else:
            return {'message': f"username {args['usrnam']} does not exist"}, 404


class Locations(Resource):
    def get(self):
        data = pd.read_csv(locations_path)
        return {'data': data.to_dict()}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('rating', type=float, required=True)
        args = parser.parse_args()
        data = pd.read_csv(locations_path)

        if args['id'] in list(data['locationId']):
            return {'message': f"{args['id']} already exists"}, 409
        else:
            data = data.append({'locationId': args['id'], 'name': args['name'], 'rating': args['rating']},
                               ignore_index=True)
            data.to_csv(locations_path, index=False)
            return {'data': data.to_dict()}, 200

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()
        data = pd.read_csv(locations_path)

        if args['id'] in list(data['locationId']):
            data = data[data['locationId'] != args['id']]
            data.to_csv(locations_path, index=False)
            return {'data': data.to_dict()}, 200
        else:
            return {'message': f";location Id {args['id']} does not exist"}, 404


api.add_resource(Users, '/users')
api.add_resource(Locations, '/locations')

if __name__ == "__main__":
    app.run(debug=True)
