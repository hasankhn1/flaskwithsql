import os
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager
from security import authenticate, identity
from resources.user import UserRegister, User, UserList, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.secret_key = 'jose'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///store.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

jwt = JWTManager(app)

@jwt.user_claims_loader
def get_user_claims(identity):
  if identity['isAdmin'] == True:
    return {'isAdmin': True}
  return {'isAdmin': False}

api.add_resource(StoreList, '/stores/')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin,'/login')

if __name__ == '__main__':
  from db import db
  db.init_app(app)
  app.run(port=5000, debug=True)
