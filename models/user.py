from db import db


class UserModel(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80))
  password = db.Column(db.String(80))
  isAdmin = db.Column(db.Boolean)
  stores = db.relationship('StoreModel', lazy='dynamic')
  def __init__(self, username, password, isAdmin= False):
    isAdmin = False if isAdmin == "false" else True
    print(isAdmin)
    self.username = username
    self.password = password
    self.isAdmin = isAdmin

  def json(self):
    return {'id': self.id, 'username': self.username, 'isAdmin': self.isAdmin}

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def find_by_username(cls, username):
    return cls.query.filter_by(username=username).first()

  @classmethod
  def user_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()

  def delete_by_userid(self, user_id):
    db.session.delete(self)
    db.session.commit()
