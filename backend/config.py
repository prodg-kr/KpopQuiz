"""
Flask 설정 파일
"""

import os
from backend.database import get_db_path


class Config:
    """기본 설정"""
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{get_db_path()}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False  # 한글 문자 처리
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    """개발 환경 설정"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """테스트 환경 설정"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """운영 환경 설정"""
    DEBUG = False


# 현재 설정
ENV = os.getenv('FLASK_ENV', 'development')
if ENV == 'testing':
    config = TestingConfig()
elif ENV == 'production':
    config = ProductionConfig()
else:
    config = DevelopmentConfig()
