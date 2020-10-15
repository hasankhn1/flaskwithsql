from flask_jwt import jwt_required
from flask_restful import Resource, Api, reqparse
from models.item import ItemModel


class Item(Resource):
  request_parser = reqparse.RequestParser()
  request_parser.add_argument('price',
                              type=float,
                              required=True,
                              help='This is required')
  request_parser.add_argument('store_id',
                              type=int,
                              required=True,
                              help='Store id is required for items')

  @jwt_required()
  def get(self, name):
    item = ItemModel.find_item(name)
    if item:
      return item.json()
    return {'message': 'Item Not found'}, 404

  def post(self, name):
    if ItemModel.find_item(name):
      return {'message': 'An item with name {} already exists'.format(name)}, 400
    data = Item.request_parser.parse_args()
    item = ItemModel(name, **data)
    try:
      item.save_to_db()
    except:
      return {'message': 'An error occured while inserting the item.'}, 500
    return item.json(), 201

  def delete(self, name):
    item = ItemModel.find_item(name)
    if item:
      try:
        item.delete_item()
      except:
        return {'message': 'An error occured while deleting the item'}, 500
      return {'message': '{} is successfully deleted.'.format(name)}
    return {'message': 'Item not found!'}, 400

  def put(self, name):
    data = Item.request_parser.parse_args()
    item = ItemModel.find_item(name)
    if item is None:
      item = ItemModel(name, **data)
    else:
      item.price = data['price']
      item.store_id = data['store_id']
    item.save_to_db()
    return item.json(), 201


class ItemList(Resource):
  def get(self):
    return {'items': [x.json() for x in ItemModel.query.all()]}
