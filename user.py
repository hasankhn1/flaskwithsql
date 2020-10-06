import sqlite3
from flask_restful import Resource, reqparse


class User:
  def __init__(self, _id, username, password):
    self.id = _id
    self.username = username
    self.password = password

  @classmethod
  def find_by_username(cls, username):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    query = 'Select * from users where username = ?'

    result = cursor.execute(query, (username,))

    row = result.fetchone()

    if row:
      user = cls(*row)
    else:
      user = None

    connection.close()
    return user

  @classmethod
  def find_by_id(cls, _id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    query = 'Select * from users where id = ?'

    result = cursor.execute(query, (_id,))

    row = result.fetchone()

    if row:
      user = cls(*row)
    else:
      user = None

    connection.close()
    return user


class UserRegister(Resource):
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str,
                        required=True, help='Username is required')
    parser.add_argument('password', type=str,
                        required=True, help='Password is required')

    data = parser.parse_args()
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    create_user_query = 'Insert into users values(NULL, ?,?)'
    cursor.execute(create_user_query, (data['username'], data['password']))

    connection.commit()
    connection.close()
    return {'message': 'User is successfully registered'}
