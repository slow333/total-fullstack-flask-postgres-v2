import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

class Config:
  """애플리케이션 환경 설정"""
  # Flask 앱의 보안을 위한 시크릿 키
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

  # 데이터베이스 설정
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
  SQLALCHEMY_TRACK_MODIFICATIONS = False