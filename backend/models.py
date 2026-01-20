from datetime import datetime
from database import db


class Category(db.Model):
    """카테고리 모델 (artist, song, general)"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 관계
    questions = db.relationship('Question', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }


class Question(db.Model):
    """문제 모델"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text)
    difficulty = db.Column(db.String(20), default='easy')  # easy, medium, hard
    
    # 새로운 스테이지 기반 시스템
    stage = db.Column(db.Integer, index=True) # 스테이지 번호
    is_active = db.Column(db.Boolean, default=True, index=True)  # 활성 문제 여부
    points = db.Column(db.Integer, default=100)  # 문제당 점수 (100점 고정)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계
    options = db.relationship('Option', backref='question', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_options=True):
        data = {
            'id': self.id,
            'category_id': self.category_id,
            'category': self.category.name,
            'question': self.question,
            'explanation': self.explanation,
            'difficulty': self.difficulty,
            'stage': self.stage, # 스테이지 정보 추가
            'is_active': self.is_active,
            'points': self.points,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        if include_options:
            data['options'] = [opt.to_dict() for opt in sorted(self.options, key=lambda x: x.order_num)]
        return data


class Option(db.Model):
    """선택지 모델"""
    __tablename__ = 'options'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    option_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    order_num = db.Column(db.Integer, nullable=False)  # 선택지 순서 (0, 1, 2, 3)
    
    def to_dict(self):
        return {
            'id': self.id,
            'option_text': self.option_text,
            'is_correct': self.is_correct,
            'order_num': self.order_num
        }


class UserScore(db.Model):
    """사용자 점수 기록 (추후 기능)"""
    __tablename__ = 'user_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer)
    total_questions = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'score': self.score,
            'total_questions': self.total_questions,
            'category_id': self.category_id,
            'created_at': self.created_at.isoformat()
        }
