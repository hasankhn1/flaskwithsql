import sqlite3
from flask_restful import Resource, reqparse, request
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_claims

_parser = reqparse.RequestParser()
_parser.add_argument('username', type=str,
                    required=True, help='Username is required')
_parser.add_argument('password', type=str,
                    required=True, help='Password is required')

class UserRegister(Resource):
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('isAdmin', type=str,
                    required=True, help='isAdmin is required')
    data = _parser.parse_args()
    isAdmin = parser.parse_args()
    print(isAdmin)
    if UserModel.find_by_username(data['username']):
      return {'message': 'Username already exists!'}
    user = UserModel(data['username'],data['password'], isAdmin['isAdmin'])
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

  @jwt_required
  def delete(self, user_id):
    claims = get_jwt_claims()
    if not claims['isAdmin']:
      return {'message': 'You are unauthorized'}
    user = UserModel.user_by_id(user_id)
    if user.isAdmin:
      return {'message': 'Admin cannot delete himself.'}
    if user is None:
      return {'message': 'No User found.'}
    user.delete_by_userid(user_id)
    return {'message': 'User is successsfully deleted.'}


class UserList(Resource):
  def get(self):
    return [user.json() for user in UserModel.query.all()]


class UserLogin(Resource):
  @classmethod
  def post(cls):
    data = _parser.parse_args()

    user = UserModel.find_by_username(data['username'])
    if user is None:
      return {'message': 'User not found'}
    if safe_str_cmp(user.password, data['password']):
      print(user.id)
      print(user.isAdmin)
      access_token = create_access_token(identity={'userId': user.id, 'isAdmin': user.isAdmin}, fresh=True)
      refrest_token = create_refresh_token({'userId': user.id, 'isAdmin': user.isAdmin})
      return {
        'access_token': access_token,
        'refresh_token': refrest_token
      },200
    
    return {'message': 'Invalid credentials'},401
