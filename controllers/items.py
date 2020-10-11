from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api, reqparse
from models.items import Items


class Item(Resource):
  request_parser = reqparse.RequestParser()
  request_parser.add_argument('price',
                              type=float,
                              required=True,
                              help='This is required')

  @jwt_required()
  def get(self, name):
    item = Items.find_item(name)
    if item is None:
      item = {'message': 'No item found!'}
    return item, 200 if item else 404

  def post(self, name):
    data = Item.request_parser.parse_args()
    item = {'name': name, 'price': data['price']}
    created_item = Items.create_item(item)
    return created_item, 201

  def delete(self, name):
    item = Items.delete_item(name)
    return item, 200 if item else 400

  def put(self, name):
    data = Item.request_parser.parse_args()
    item = {'name': name, 'price': data['price']}
    item = Items.create_or_update(item)
    return item, 200


class ItemList(Resource):
  def get(self):
    return Items.get_all(), 200
