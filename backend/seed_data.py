"""
JSON 데이터를 SQLite DB로 마이그레이션하는 스크립트
python seed_data.py 로 실행
"""

import json
import os
from app import app, db
from models import Category, Question, Option


def load_json_data():
    """JSON 파일에서 데이터 로드"""
    json_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'questions.json'
    )
    
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def seed_database():
    """데이터베이스에 데이터 시드"""
    with app.app_context():
        # 기존 데이터 삭제
        Question.query.delete()
        Category.query.delete()
        db.session.commit()
        print("🗑️  기존 데이터 삭제 완료")
        
        # JSON 데이터 로드
        data = load_json_data()
        
        # 카테고리별로 처리
        for category_name, questions_list in data['categories'].items():
            # 카테고리 생성
            category = Category(
                name=category_name,
                description=f"{category_name.upper()} 카테고리"
            )
            db.session.add(category)
            db.session.flush()  # ID 생성
            
            # 문제 추가
            for q in questions_list:
                question = Question(
                    category_id=category.id,
                    question=q['question'],
                    explanation=q.get('explanation', ''),
                    difficulty=q.get('difficulty', 'easy')
                )
                db.session.add(question)
                db.session.flush()
                
                # 선택지 추가
                for idx, option_text in enumerate(q['options']):
                    option = Option(
                        question_id=question.id,
                        option_text=option_text,
                        is_correct=(idx == q['answer']),
                        order_num=idx
                    )
                    db.session.add(option)
            
            print(f"✅ {category_name}: {len(questions_list)}개 문제 추가")
        
        # 커밋
        db.session.commit()
        
        # 통계
        total_categories = Category.query.count()
        total_questions = Question.query.count()
        print(f"\n📊 최종 통계:")
        print(f"  - 카테고리: {total_categories}개")
        print(f"  - 전체 문제: {total_questions}개")


if __name__ == '__main__':
    seed_database()
