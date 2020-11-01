from flask_jwt_extended import jwt_required, get_jwt_claims
from flask_restful import Resource, Api, reqparse, request
from models.item import ItemModel


class Item(Resource):
  _request_parser = reqparse.RequestParser()
  _request_parser.add_argument('store_id',
                              type=str,
                              required=True,
                              help='Store id is required for items')
  _request_parser.add_argument('user_id',
                              type=str,
                              required=True,
                              help='User id is required for items')

  @jwt_required
  def get(self, name):
    store_id = request.args.get('store_id')
    user_id = request.args.get('user_id')
    if store_id is None or user_id is None:
      return {'message': 'please provide store id and user id'}
    item = ItemModel.find_item(name,store_id, user_id)
    if item:
      return item.json()
    return {'message': 'Item Not found'}, 404

  def post(self, name):
    data = Item._request_parser.parse_args()
    if ItemModel.find_item(name,data['store_id'], data['user_id']):
      return {'message': 'An item with name {} already exists'.format(name)}, 400
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('price',
                              type=str,
                              required=True,
                              help='Price is required for items')
    price_data = request_parser.parse_args()
    item = ItemModel(name, price_data['price'], **data)
    item.save_to_db()
    return item.json(), 201

  def delete(self, name):
    store_id = request.args.get('store_id')
    user_id = request.args.get('user_id')
    if store_id is None or user_id is None:
      return {'message': 'please provide store id and user id.'}
    item = ItemModel.find_item(name, store_id, user_id)
    if item:
      try:
        item.delete_item()
      except:
        return {'message': 'An error occured while deleting the item'}, 500
      return {'message': '{} is successfully deleted.'.format(name)}
    return {'message': 'Item not found!'}, 400

  def put(self, name):
    data = Item._request_parser.parse_args()
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('price',
                              type=str,
                              required=True,
                              help='Price is required for items')
    price_data = request_parser.parse_args()
    
    item = ItemModel.find_item(name,data['store_id'],data['user_id'])
    if item is None:
      item = ItemModel(name, price_data['price'], **data)
    else:
      item.price = price_data['price']
      item.store_id = data['store_id']
      item.user_id = data['user_id']
    item.save_to_db()
    return item.json(), 201


class ItemList(Resource):
  @jwt_required
  def get(self):
    claims = get_jwt_claims()
    if not claims['isAdmin']:
      return {'message':"You are unauthorized"}, 401
    store_id = request.args.get('store_id')
    user_id = request.args.get('user_id')
    if store_id is None or  user_id is None:
      return {'message': 'please provide store id and user id.'}
    return {'items': [x.json() for x in ItemModel.query.filter_by(store_id=store_id, user_id=user_id)]}
