from flask import Flask, jsonify, request, render_template_string, send_from_directory
from flask_cors import CORS
import random
import json
import os
from database import db, init_db
from models import Category, Question, Option, UserScore
from config import config


def load_json_to_db(app):
    """JSON 파일의 데이터를 DB에 동기화"""
    with app.app_context():
        try:
            # JSON 로드
            json_path = os.path.join(os.path.dirname(__file__), '..', 'questions.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 기존 데이터 삭제
            Question.query.delete()
            Option.query.delete()
            Category.query.delete()
            db.session.commit()
            
            # 카테고리별로 처리
            for category_name in ['artist', 'song', 'general']:
                category = Category(
                    name=category_name,
                    description=f"{category_name} 카테고리"
                )
                db.session.add(category)
                db.session.flush()
                
                # 문제 추가
                for q in data['categories'][category_name]:
                    difficulty = q.get('difficulty', 'easy')
                    # 난이도별 차등 점수 자동 설정
                    points_map = {'easy': 1, 'medium': 2, 'hard': 3}
                    points = points_map.get(difficulty, 1)
                    
                    question = Question(
                        category_id=category.id,
                        question=q['question'],
                        explanation=q.get('explanation', ''),
                        difficulty=difficulty,
                        is_active=True,  # 기본값: 활성
                        points=points  # 차등 점수
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
            
            db.session.commit()
            print(f"DB sync complete: {Question.query.count()} questions loaded")
        except Exception as e:
            print(f"DB sync failed: {e}")


def create_app():
    """Flask 앱 생성"""
    app = Flask(__name__)
    
    # 설정 로드
    app.config.from_object(config)
    
    # DB 초기화
    init_db(app)
    
    # JSON 데이터를 DB에 동기화
    load_json_to_db(app)
    
    # CORS 활성화 (프론트엔드에서 접근 가능)
    # 모든 오리진에서의 요청 허용 (개발 환경)
    CORS(app, 
         origins="*",
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type"])
    
    return app


app = create_app()


# ==================== 정적 파일 제공 ====================

@app.route('/')
def index():
    """홈페이지 - index.html 제공"""
    try:
        # 프로젝트 루트의 index.html 읽기
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(parent_dir, 'index.html'), 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>", 500


# ==================== API 라우트 ====================

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """모든 카테고리 조회"""
    try:
        categories = Category.query.all()
        return jsonify({
            'success': True,
            'data': [cat.to_dict() for cat in categories]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/quiz', methods=['GET'])
def get_quiz():
    """퀴즈 문제 조회 (활성 문제만, SQL 레벨 랜덤화)
    
    쿼리 파라미터:
    - limit: 가져올 문제 수 (기본값: 100)
    
    변경사항:
    - 난이도 필터 제거 (모든 난이도 출제)
    - is_active=True 문제만 조회 (일일 업데이트 지원)
    - SQL RANDOM()으로 서버 레벨 랜덤화
    """
    try:
        # 쿼리 파라미터
        limit = int(request.args.get('limit', 100))
        
        # 활성 문제만 조회 + SQL 레벨 랜덤화
        # SQLite의 경우 func.random() 사용
        from sqlalchemy import func
        questions = Question.query.filter_by(is_active=True)\
            .order_by(func.random())\
            .limit(limit)\
            .all()
        
        # 응답 구성 (points 필드 포함)
        quiz_data = []
        for q in questions:
            q_dict = q.to_dict()
            # 선택지 정보 포함 (order_num 기준으로 정렬)
            q_dict['options'] = [
                {
                    'id': opt['id'],
                    'option_text': opt['option_text'],
                    'order_num': opt['order_num'],
                    'is_correct': opt['is_correct']
                }
                for opt in q_dict['options']
            ]
            quiz_data.append(q_dict)
        
        return jsonify({
            'success': True,
            'data': quiz_data,
            'count': len(quiz_data)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/quiz/<int:question_id>/check', methods=['POST'])
def check_answer(question_id):
    """답변 검증
    
    POST body:
    {
        "selected_option_id": 1
    }
    """
    try:
        data = request.get_json()
        selected_option_id = data.get('selected_option_id')
        
        if not selected_option_id:
            return jsonify({'success': False, 'error': '선택한 옵션 ID가 필요합니다'}), 400
        
        # 질문과 선택지 조회
        question = Question.query.get(question_id)
        if not question:
            return jsonify({'success': False, 'error': '문제를 찾을 수 없습니다'}), 404
        
        option = Option.query.get(selected_option_id)
        if not option or option.question_id != question_id:
            return jsonify({'success': False, 'error': '선택지를 찾을 수 없습니다'}), 404
        
        # 정답 여부 확인
        is_correct = option.is_correct
        correct_option = next((opt for opt in question.options if opt.is_correct), None)
        
        return jsonify({
            'success': True,
            'is_correct': is_correct,
            'explanation': question.explanation,
            'correct_option_id': correct_option.id if correct_option else None,
            'correct_option_text': correct_option.option_text if correct_option else None
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/quiz/stats', methods=['GET'])
def get_stats():
    """통계 조회"""
    try:
        total_questions = Question.query.count()
        total_categories = Category.query.count()
        
        stats_by_category = []
        for cat in Category.query.all():
            q_count = Question.query.filter_by(category_id=cat.id).count()
            stats_by_category.append({
                'category': cat.name,
                'count': q_count
            })
        
        return jsonify({
            'success': True,
            'total_questions': total_questions,
            'total_categories': total_categories,
            'by_category': stats_by_category
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== 관리자 API ====================

@app.route('/api/admin/questions', methods=['POST'])
def add_question():
    """새로운 문제 추가 (관리자용)
    
    POST body:
    {
        "category": "artist",
        "question": "문제 텍스트",
        "options": ["선택지1", "선택지2", "선택지3", "선택지4"],
        "answer": 0,
        "explanation": "설명",
        "difficulty": "easy"
    }
    """
    try:
        data = request.get_json()
        
        # 유효성 검사
        required = ['category', 'question', 'options', 'answer']
        if not all(key in data for key in required):
            return jsonify({'success': False, 'error': '필수 필드가 부족합니다'}), 400
        
        # 카테고리 조회
        category = Category.query.filter_by(name=data['category']).first()
        if not category:
            return jsonify({'success': False, 'error': '카테고리를 찾을 수 없습니다'}), 404
        
        # 문제 생성
        question = Question(
            category_id=category.id,
            question=data['question'],
            explanation=data.get('explanation', ''),
            difficulty=data.get('difficulty', 'easy')
        )
        db.session.add(question)
        db.session.flush()
        
        # 선택지 생성
        for idx, option_text in enumerate(data['options']):
            option = Option(
                question_id=question.id,
                option_text=option_text,
                is_correct=(idx == data['answer']),
                order_num=idx
            )
            db.session.add(option)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '문제가 추가되었습니다',
            'question_id': question.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/admin/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    """문제 수정 (관리자용)"""
    try:
        question = Question.query.get(question_id)
        if not question:
            return jsonify({'success': False, 'error': '문제를 찾을 수 없습니다'}), 404
        
        data = request.get_json()
        
        # 필드 업데이트
        if 'question' in data:
            question.question = data['question']
        if 'explanation' in data:
            question.explanation = data['explanation']
        if 'difficulty' in data:
            question.difficulty = data['difficulty']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '문제가 업데이트되었습니다',
            'data': question.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/admin/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """문제 삭제 (관리자용)"""
    try:
        question = Question.query.get(question_id)
        if not question:
            return jsonify({'success': False, 'error': '문제를 찾을 수 없습니다'}), 404
        
        db.session.delete(question)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '문제가 삭제되었습니다'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== 헬스 체크 ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """헬스 체크"""
    return jsonify({
        'status': 'OK',
        'database': 'connected'
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
