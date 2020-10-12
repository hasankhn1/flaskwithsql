import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
  def post(self):
    message = ''
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str,
                        required=True, help='Username is required')
    parser.add_argument('password', type=str,
                        required=True, help='Password is required')

    data = parser.parse_args()
    row = UserModel.find_by_username(data['username'])
    data = parser.parse_args()
    connection = sqlite3.connect('store.db')
    cursor = connection.cursor()
    if row is None:
      create_user_query = 'Insert into users values(NULL, ?,?)'
      cursor.execute(create_user_query, (data['username'], data['password']))
      connection.commit()
      message = 'User is successfully registered'
    else:
      message = 'Username is already taken'
    connection.close()
    return {'message': message}
