# from flask import redirect, url_for, flash, Blueprint, render_template
# from flask_admin import Admin, AdminIndexView, expose
# from flask_admin.contrib.sqla import ModelView
# from flask_login import current_user

# bp =Blueprint('admin_app', __name__, url_prefix='/admin')

# @bp.route('/')
# def index():
#     return render_template('admin/index.html')

# # Custom Admin Index View to secure the main admin page
# class SecureAdminIndexView(AdminIndexView):
#     def is_accessible(self):
#         # Only grant access if the user is authenticated and is an admin
#         return current_user.is_authenticated and current_user.is_admin

#     def inaccessible_callback(self, name, **kwargs):
#         # Redirect non-admins to the home page or a login page
#         flash('You do not have permission to access the admin panel.', 'danger')
#         return redirect(url_for('admin_app.index'))

# # Custom Model View to secure model management pages
# class SecureModelView(ModelView):
#     def is_accessible(self):
#         # Same security check as the index view
#         return current_user.is_authenticated and current_user.is_admin

#     def inaccessible_callback(self, name, **kwargs):
#         # Redirect non-admins
#         flash('You do not have permission to access this resource.', 'danger')
#         return redirect(url_for('admin_app.index'))

# def init_admin(app, db, *models):
#     """
#     Initializes the admin interface.

#     :param app: Flask application instance
#     :param db: SQLAlchemy database instance
#     :param models: A list of model classes to add to the admin interface
#     """
#     admin = Admin(
#         app,
#         name='Admin Panel',
#         template_mode='bootstrap4',
#         index_view=SecureAdminIndexView(name='Dashboard', url='/admin')
#     )

#     # Add all specified models to the admin interface
#     for model_class in models:
#         admin.add_view(SecureModelView(model_class, db.session, category='Models'))

