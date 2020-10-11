import sqlite3
import json


class Items:
  def __init__(self, _id, name, price):
    self.id = _id
    self.name = name
    self.price = price

  @classmethod
  def create_item(cls, item):
    get_item = cls.find_item(item['name'])
    if get_item:
      return {'message': 'Item already exists'}
    connection = sqlite3.connect('store.db')
    cursor = connection.cursor()
    create_item_query = 'Insert into items values(NULL,?,?)'
    cursor.execute(create_item_query, (item['name'], item['price']))
    connection.commit()
    connection.close()
    return item

  @classmethod
  def find_item(cls, itemName):
    find_item_query = 'Select * from items where name = ?'
    connection = sqlite3.connect('store.db')
    cursor = connection.cursor()
    result = cursor.execute(find_item_query, (itemName,))
    row = result.fetchone()
    if row:
      item = {'item': {'name': row[0], 'price': row[1]}}
    else:
      item = None

    return item

  @classmethod
  def delete_item(cls, itemName):
    item = cls.find_item(itemName)
    if item is None:
      return {'message': 'No item found!'}
    connection = sqlite3.connect('store.db')
    cursor = connection.cursor()
    delete_query = 'Delete from items where name = ?'
    cursor.execute(delete_query, (itemName,))
    connection.commit()
    connection.close()
    return {'message': 'item is successfully deleted!'}

  @classmethod
  def get_all(cls):
    connection = sqlite3.connect('store.db')
    cursor = connection.cursor()
    select_query = 'Select * from items'
    result = cursor.execute(select_query)
    items = {'items': []}
    if result is not None:
      for row in result:
        items['items'].append({'id': row[0], 'name': row[1], 'price': row[2]})
    connection.commit()
    connection.close()
    return items

  @classmethod
  def create_or_update(cls, item):
    get_item = cls.find_item(item['name'])
    connection = sqlite3.connect('store.db')
    cursor = connection.cursor()
    if get_item is None:
      create_item_query = 'Insert into items values(NULL,?,?)'
      cursor.execute(create_item_query, (item['name'], item['price']))
    else:
      update_item_query = 'Update items set price = ? where name = ?'
      cursor.execute(update_item_query, (item['price'], item['name']))
    connection.commit()
    connection.close()
    return item