from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api, reqparse
from models.item import ItemModel


class Item(Resource):
  request_parser = reqparse.RequestParser()
  request_parser.add_argument('price',
                              type=float,
                              required=True,
                              help='This is required')

  @jwt_required()
  def get(self, name):
    item = ItemModel.find_item(name)
    if item:
      return item.json()
    return {'message': 'Item Not found'}, 404

  def post(self, name):
    if ItemModel.find_item(name):
      return {'message': 'Item already exists!'}
    data = Item.request_parser.parse_args()
    item = ItemModel(name, data['price'])
    item.create_item()
    return item.json(), 201

  def delete(self, name):
    if ItemModel.find_item(name):
      return ItemModel.delete_item(name)
    return {'message':'Item not found!'}, 400

  def put(self, name):
    data = Item.request_parser.parse_args()
    item = {'name': name, 'price': data['price']}
    item = ItemModel.create_or_update(item)
    return item, 200


class ItemList(Resource):
  def get(self):
    return ItemModel.get_all(), 200
