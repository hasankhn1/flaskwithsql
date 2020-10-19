from db import db


class StoreModel(db.Model):
  __tablename__ = 'stores'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  items = db.relationship('ItemModel', lazy='dynamic')

  def __init__(self, name, _id=None):
    self.name = name
    self.id = _id

  def json(self):
    return {'_id':self.id,'name': self.name, 'items': [item.json() for item in self.items.all()]}

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def find_store(cls, name):
    return cls.query.filter_by(name=name).first()

  def delete_store(self):
    db.session.delete(self)
    db.session.commit()