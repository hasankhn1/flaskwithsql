from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.store import StoreModel


class Store(Resource):
  request_parser = reqparse.RequestParser()
  request_parser.add_argument('user_id', type=str, required=True, help="User id is required")
  
  @jwt_required
  def post(self, name):
    claims = get_jwt_claims()
    if not claims['isAdmin']:
      return {'message': 'You are unauthorized'}
    data = Store.request_parser.parse_args()
    if StoreModel.find_store(name,data['user_id']):
      return {'message': 'Store name already exists!'}, 400
    store = StoreModel(name,data['user_id'])
    try:
      store.save_to_db()
    except:
      return {'message': 'An error occured while creating store'}, 500
    return {'message': 'Store with name \'{}\' is created.'.format(name)}

  @jwt_required
  def get(self, name):
    user_id = request.args.get('user_id')
    store = StoreModel.find_store(name,user_id)
    if store is None:
      return {'message': 'A store with name {} doesn\'t exists'.format(name)}
    return store.json(), 200

  @jwt_required
  def delete(self, name):
    claims = get_jwt_claims()
    if not claims['isAdmin']:
      return {'message': 'You are unauthorized'}
    user_id = request.args.get('user_id')
    store = StoreModel.find_store(name,user_id)
    if store:
      store.delete_store()
      return {'message': 'Store {} is successfully deleted.'.format(name)}
    return {'message': 'Store {} is not found.'.format(name)}


class StoreList(Resource):
  def get(self):
    user_id = request.args.get('user_id')
    return [store.json() for store in StoreModel.query.filter_by(user_id= user_id)]
