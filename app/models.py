from .extensions import db
from flask_login import UserMixin
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, flash
from flask_login import current_user
from flask_wtf import FlaskForm

class BaseModel(db.Model):
  __abstract__ = True
  __allow_unmapped__ = True
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class User(UserMixin, BaseModel):
  is_admin = db.Column(db.Boolean, default=False, nullable=False)
  username = db.Column(db.String(64), unique=True, nullable=False)
  email = db.Column(db.String(255), unique=True, nullable=False)
  password = db.Column(db.Text(), nullable=False)

  def __repr__(self):
    return f'{self.username}'
  
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
  
# Custom Admin Index View to secure the main admin page
class SecureAdminIndexView(AdminIndexView):
  def is_accessible(self):
    # Only grant access if the user is authenticated and is an admin
    return current_user.is_authenticated and current_user.is_admin

  def inaccessible_callback(self, name, **kwargs):
    # Redirect non-admins to the home page or a login page
    flash('You do not have permission to access the admin panel.', 'danger')
    return redirect(url_for('auth.login_users'))

# Custom Model View to secure model management pages
class SecureModelView(ModelView):
  def is_accessible(self):
    # Same security check as the index view
    return current_user.is_authenticated and current_user.is_admin

  def inaccessible_callback(self, name, **kwargs):
    # Redirect non-admins
    flash('You do not have permission to access this resource.', 'danger')
    return redirect(url_for('auth.login_users'))

class UserView(SecureModelView):
  # can_delete = False
  # can_edit = True
  # can_create = True
  # can_view_details = True
  # column_exclude_list = ['password', ]
  # column_searchable_list = ['username', 'email']
  #enable inline editing in the list view: is not working
  # Explicitly define columns for the create/edit form to avoid relationship errors.
  # This prevents Flask-Admin from trying to render the 'profile' relationship.
  form_columns = ['username', 'email', 'is_admin']