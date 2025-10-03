from . import db
from flask_login import UserMixin

class BaseModel(db.Model):
  __abstract__ = True
  __allow_unmapped__ = True
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class User(UserMixin, BaseModel):
  username = db.Column(db.String(64), unique=True, nullable=False)
  email = db.Column(db.String(255), unique=True, nullable=False)
  password = db.Column(db.Text(), nullable=False)

  def __repr__(self):
    return f'{self.username}'
  
class Todo(BaseModel):
  content = db.Column(db.String(200), nullable=False)
  completed = db.Column(db.Boolean, default=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  user = db.relationship('User', backref=db.backref('todos', lazy=True))

  def __repr__(self):
    return f'<Todo {self.id}>'

class Blog(BaseModel):
  title = db.Column(db.String(255), nullable=False)
  content = db.Column(db.Text(), nullable=False)
  comment = db.Column(db.Text(), nullable=True)
  created = db.Column(db.DateTime, default=db.func.current_timestamp())
  author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  author = db.relationship('User', backref=db.backref('blogs', lazy=True))

  def __repr__(self):
    return f'<Blog {self.title}>'