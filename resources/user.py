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


class User(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('user_id', type=int, required=True,
                      help="User id is required")

  def get(self, user_id):
    user = UserModel.user_by_id(user_id)
    if user is None:
      return {'message': 'No User found.'}
    return user.json()


  def delete(self, user_id):
      user = UserModel.user_by_id(user_id)
      if user is None:
        return {'message': 'No User found.'}
      user.delete_by_userid(user_id)
      return {'message': 'User is successsfully deleted.'}

class UserList(Resource):
  def get(self):
    return [user.json() for user in UserModel.query.all()]