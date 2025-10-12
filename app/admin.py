from flask import redirect, url_for, flash, Blueprint, render_template
from flask_admin import Admin, AdminIndexView, expose
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField

# Custom Admin Index View to secure the main admin page
class SecureAdminIndexView(AdminIndexView):
  def is_accessible(self):
    return current_user.is_authenticated and current_user.is_admin

  def inaccessible_callback(self, name, **kwargs):
    flash('You do not have permission to access the admin panel.', 'danger')
    return redirect(url_for('auth.login_users'))

# Custom Model View to secure model management pages
class SecureModelView(ModelView):
  def is_accessible(self):
    return current_user.is_authenticated and current_user.is_admin

  def inaccessible_callback(self, name, **kwargs):
    flash('You do not have permission to access this resource.', 'danger')
    return redirect(url_for('auth.login_users'))

class UserView(SecureModelView):
  # 이 메서드가 빠지면 `TypeError` 발생 가능성이 높아집니다.
  def __init__(self, model, session, **kwargs):
    # **kwargs를 통해 Flask-Admin의 추가 인자를 모두 받아서  부모 클래스의 생성자에 전달합니다.
    super().__init__(model, session, **kwargs)
  form_extra_fields = {
    'password': PasswordField('Password')
  }  
  # set password-hash
  def on_model_change(self, form, model, is_created):
    if form.password.data:
      model.set_password(form.password.data)
    elif not is_created:
      del form.password

class BlogView(SecureModelView):
  form_ajax_refs = {
    'author': {
      'fields': ['username', 'email'], # Fields to search against in the User model
      'placeholder': 'Please select a user',
      'page_size': 10,
      'minimum_input_length': 1, # Start searching after typing at least 1 character
    }
  }
class TodoView(SecureModelView):
  form_ajax_refs = {
    'user': {
      'fields': ['username', 'email'], 
      'placeholder': 'Please select a user',
      'page_size': 10,
      'minimum_input_length': 1, 
    }
  }
class UserProfileView(SecureModelView):
  # Use AJAX for the 'user' relationship
  # This will render a search box instead of a dropdown
  form_ajax_refs = {
    'user': {
      'fields': ['username', 'email'], 
      'placeholder': 'Please select a user',
      'page_size': 10,
      'minimum_input_length': 1, 
    }
  }

class BookView(SecureModelView):
  pass

def init_admin(app, db):
  admin = Admin(
      app,
      name='Admin Panel',
      template_mode='bootstrap4',
      index_view=SecureAdminIndexView(name='Dashboard', url='/admin')
  )

  # Add all specified models to the admin interface
  from .models import User, Blog, Todo, UserProfile, Book
  admin.add_view(UserView(User, db.session, category='Models'))
  admin.add_view(BlogView(Blog, db.session, category='Models'))
  admin.add_view(TodoView(Todo, db.session, category='Models'))
  admin.add_view(UserProfileView(UserProfile, db.session, category='Models'))
  admin.add_view(BookView(Book, db.session, category='Models'))