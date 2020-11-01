from db import db


class StoreModel(db.Model):
  __tablename__ = 'stores'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('UserModel')
  items = db.relationship('ItemModel', lazy='dynamic')

  def __init__(self, name, user_id):
    self.name = name
    self.user_id = user_id

  def json(self):
    return {'id':self.id,'name': self.name, 'user_id': self.user_id, 'items': [item.json() for item in self.items.all()]}

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def find_store(cls, name, user_id):
    return cls.query.filter_by(name=name,user_id=user_id).first()

  def delete_store(self):
    db.session.delete(self)
    db.session.commit()