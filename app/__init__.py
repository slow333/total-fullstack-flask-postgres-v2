from flask import Flask
from config import Config
from flask_admin import Admin
from .extensions import db, mail, login_manager

def create_app(config_class=Config):
  app = Flask(__name__)
  
  # 설정 클래스로부터 설정을 로드
  app.config.from_object(config_class)

  # SQLAlchemy 객체를 앱과 연결
  db.init_app(app)
  mail.init_app(app)
  login_manager.init_app(app)

  from .models import SecureAdminIndexView
  admin = Admin(app, name='Admin Panel', template_mode='bootstrap3',
          index_view=SecureAdminIndexView(name='Dashboard', url='/admin')
  )
  # Add all specified models to the admin interface
  from .models import User, Blog, Todo, UserProfile, Book, UserView, UserProfileView, BlogView, TodoView, BookView
  admin.add_view(UserView(User, db.session, category='Models'))
  admin.add_view(BlogView(Blog, db.session, category='Models'))
  admin.add_view(TodoView(Todo, db.session, category='Models'))
  admin.add_view(UserProfileView(UserProfile, db.session, category='Models'))
  admin.add_view(BookView(Book, db.session, category='Models'))

  # 블루프린트나 다른 라우트를 여기서 등록
  with app.app_context():

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
      return User.query.get(int(user_id))
    
    # Register all blueprints from the routes module
    from . import routes # This will now import your new routes.py
    routes.init_app(app)

    # 데이터베이스 테이블 생성
    db.create_all()

  return app