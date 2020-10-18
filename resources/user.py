import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str,
                        required=True, help='Username is required')
    parser.add_argument('password', type=str,
                        required=True, help='Password is required')

    data = parser.parse_args()
    if UserModel.find_by_username(data['username']):
      return {'message': 'Username already exists!'}
    user = UserModel(**data)
    user.save_to_db()
    return {'message': 'User is successfully registered!'}