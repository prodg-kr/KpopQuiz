import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """데이터베이스 초기화"""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully!")


def get_db_path():
    """데이터베이스 경로 반환"""
    base_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.dirname(base_dir)
    return os.path.join(parent_dir, 'kpop_quiz.db')
