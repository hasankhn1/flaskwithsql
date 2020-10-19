from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):

  def post(self, name):
    if StoreModel.find_store(name):
      return {'message': 'Store name already exists!'}, 400
    store = StoreModel(name)
    try:
      store.save_to_db()
    except:
      return {'message': 'An error occured while creating store'}, 500
    return {'message': 'Store with name \'{}\' is created.'.format(name)}

  @jwt_required()
  def get(self, name):
    store = StoreModel.find_store(name)
    if store is None:
      return {'message': 'A store with name {} doesn\'t exists'.format(name)}
    return store.json(), 200

  def delete(self, name):
    store = StoreModel.find_store(name)
    if store:
      store.delete_store()
      return {'message': 'Store {} is successfully deleted.'.format(name)}
    return {'message': 'Store {} is not found.'.format(name)}


class StoreList(Resource):
  def get(self):
    return [store.json() for store in StoreModel.query.all()]
