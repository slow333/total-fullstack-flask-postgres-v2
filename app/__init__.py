from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# SQLAlchemy 객체 생성
db = SQLAlchemy()

def create_app(config_class=Config):
  app = Flask(__name__)
  
  # 설정 클래스로부터 설정을 로드
  app.config.from_object(config_class)

  # SQLAlchemy 객체를 앱과 연결
  db.init_app(app)

  # 블루프린트나 다른 라우트를 여기서 등록
  with app.app_context():
    from .routes.auths import todo
    app.register_blueprint(todo.bp)

    # 데이터베이스 테이블 생성
    db.create_all()

  return app