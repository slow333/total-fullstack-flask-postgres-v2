from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_mail import Mail # type: ignore
from flask_login import LoginManager
from .admin import init_admin

# SQLAlchemy 객체 생성
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.login_users'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
  app = Flask(__name__)
  
  # 설정 클래스로부터 설정을 로드
  app.config.from_object(config_class)

  # SQLAlchemy 객체를 앱과 연결
  db.init_app(app)
  mail.init_app(app)
  login_manager.init_app(app)

  # 블루프린트나 다른 라우트를 여기서 등록
  with app.app_context():
    from .models import User, Blog, Todo, UserProfile
    # Pass the app, db, and all models you want to manage
    init_admin(app, db, User, Blog, Todo, UserProfile) # Add other models like Post, Comment, etc.

    @login_manager.user_loader
    def load_user(user_id):
      return User.query.get(int(user_id))
    
    # ========= 인증 관련 블루프린트 등록 ==============
    from .routes.auths import auth
    app.register_blueprint(auth.bp)

    from .routes.auths import todo
    app.register_blueprint(todo.bp)

    from .routes.auths import user_profile
    app.register_blueprint(user_profile.bp)

    from .routes.auths import blog
    app.register_blueprint(blog.bp)

    # ========= 콘텐츠 관련 블루프린트 등록 ==============
    from .routes.contents import database_bp
    app.register_blueprint(database_bp.bp)

    from .routes.contents import dom_bp
    app.register_blueprint(dom_bp.bp)

    from .routes.contents import js_bp
    app.register_blueprint(js_bp.bp)

    from .routes.contents import home_bp
    app.register_blueprint(home_bp.bp)

    from .routes.contents import java_bp
    app.register_blueprint(java_bp.bp)

    from .routes.contents import python_bp
    app.register_blueprint(python_bp.bp)

    from .routes.contents import spring_bp
    app.register_blueprint(spring_bp.bp)

    @app.route('/')
    @app.route('/home')
    def home():
      return render_template('index.html')
    
    @app.route('/apps/')
    def apps_home():
      return render_template('apps/apps_home.html')
    
    # 데이터베이스 테이블 생성
    db.create_all()

  return app