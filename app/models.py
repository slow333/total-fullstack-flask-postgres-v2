from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel(db.Model):
  __abstract__ = True
  __allow_unmapped__ = True
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class User(UserMixin, BaseModel):
  username = db.Column(db.String(64), unique=True, nullable=False)
  email = db.Column(db.String(255), unique=True, nullable=False)
  password_hash  = db.Column(db.Text(), nullable=False)
  is_admin = db.Column(db.Boolean, default=False, nullable=False)

  def set_password(self, password):
    self.password_hash  = generate_password_hash(password)
    
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return f'<User {self.username}>'

class Todo(BaseModel):
  title = db.Column(db.String(100), nullable=False)
  content = db.Column(db.String(200), nullable=False)
  created = db.Column(db.DateTime, default=db.func.current_timestamp())
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
    return f'<Blog {self.title} for {self.author.username}>'
  
class UserProfile(BaseModel):
  firstname = db.Column(db.String(60), nullable=True)
  lastname = db.Column(db.String(30), nullable=True)
  address = db.Column(db.String(100), nullable=True)
  profile_image = db.Column(db.String(255), nullable=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
  user = db.relationship('User', backref=db.backref('profile', uselist=False))

  def __repr__(self):
    return f'<UserProfile for {self.user.username}>'

class Book(BaseModel):
  title = db.Column(db.String(255), nullable=False)
  author = db.Column(db.String(255), nullable=False, default='Unknown')
  language = db.Column(db.String(50))
  published_date = db.Column(db.Date)

  def __repr__(self):
    return f'<Book {self.title} by {self.author}>'
  
