"""
DB 초기화 및 데이터 마이그레이션 스크립트
python init_db.py 로 실행
"""

import sys
import os
import json

# 경로 설정
sys.path.insert(0, os.path.dirname(__file__))

from backend.app import app, db
from backend.models import Category, Question, Option


def load_json_data():
    """JSON 파일에서 데이터 로드"""
    json_path = os.path.join(
        os.path.dirname(__file__),
        'questions.json'
    )
    
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def init_database():
    """데이터베이스 초기화 및 데이터 마이그레이션"""
    with app.app_context():
        print("\n🔧 데이터베이스 초기화 시작...\n")
        
        # 데이터베이스 생성
        db.create_all()
        print("✅ 데이터베이스 테이블 생성 완료")
        
        # 기존 데이터 삭제
        print("🗑️  기존 데이터 삭제 중...")
        Question.query.delete()
        Category.query.delete()
        db.session.commit()
        
        # JSON 데이터 로드
        print("📂 JSON 데이터 로드 중...")
        data = load_json_data()
        
        total_questions = 0
        
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
                
                total_questions += 1
            
            print(f"  ✅ {category_name.upper()}: {len(questions_list)}개 문제")
        
        # 커밋
        db.session.commit()
        
        # 통계
        total_categories = Category.query.count()
        total_q = Question.query.count()
        print(f"\n📊 최종 통계:")
        print(f"  - 카테고리: {total_categories}개")
        print(f"  - 전체 문제: {total_q}개")
        print(f"\n✨ 데이터베이스 초기화 완료!\n")


if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}\n")
        import traceback
        traceback.print_exc()
