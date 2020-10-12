import sqlite3
import json


class ItemModel:
  def __init__(self, name, price):
    self.name = name
    self.price = price

  def json(self):
    return {'name': self.name, 'price': self.price}

  def create_item(self):
    connection = sqlite3.connect('store.db')
    cursor = connection.cursor()
    create_item_query = 'Insert into items values(NULL,?,?)'
    cursor.execute(create_item_query, (self.name, self.price))
    connection.commit()
    connection.close()

  @classmethod
  def find_item(cls, itemName):
    find_item_query = 'Select * from items where name = ?'
    connection = sqlite3.connect('store.db')
    cursor = connection.cursor()
    result = cursor.execute(find_item_query, (itemName,))
    row = result.fetchone()
    if row:
      item = cls(row[1], row[2])
    else:
      item = None

    return item

  @classmethod
  def delete_item(cls, itemName):
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
