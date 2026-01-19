#!/usr/bin/env python3
"""순수 SQLite로 DB 동기화"""
import json
import sqlite3
from pathlib import Path

def sync_db():
    db_path = Path('kpop_quiz.db')
    
    # 기존 DB 파일 삭제
    if db_path.exists():
        db_path.unlink()
        print("🗑️  기존 DB 파일 삭제 완료\n")
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY,
        category_id INTEGER,
        question TEXT NOT NULL,
        explanation TEXT,
        difficulty TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(category_id) REFERENCES categories(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS options (
        id INTEGER PRIMARY KEY,
        question_id INTEGER,
        option_text TEXT NOT NULL,
        is_correct BOOLEAN,
        order_num INTEGER,
        FOREIGN KEY(question_id) REFERENCES questions(id)
    )
    ''')
    
    # 기존 데이터 삭제
    cursor.execute('DELETE FROM options')
    cursor.execute('DELETE FROM questions')
    cursor.execute('DELETE FROM categories')
    conn.commit()
    
    # JSON 로드
    with open('questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 카테고리 추가
    categories = {'artist': 1, 'song': 2, 'general': 3}
    for cat_name, cat_id in categories.items():
        cursor.execute(
            'INSERT INTO categories (id, name, description) VALUES (?, ?, ?)',
            (cat_id, cat_name, f'{cat_name} 카테고리')
        )
    
    conn.commit()
    
    # 문제 추가
    question_id = 1
    for category_name in ['artist', 'song', 'general']:
        cat_id = categories[category_name]
        
        for q in data['categories'][category_name]:
            cursor.execute(
                'INSERT INTO questions (id, category_id, question, explanation, difficulty) VALUES (?, ?, ?, ?, ?)',
                (question_id, cat_id, q['question'], q.get('explanation', ''), q.get('difficulty', 'easy'))
            )
            
            # 선택지 추가
            for idx, opt_text in enumerate(q['options']):
                cursor.execute(
                    'INSERT INTO options (question_id, option_text, is_correct, order_num) VALUES (?, ?, ?, ?)',
                    (question_id, opt_text, 1 if idx == q['answer'] else 0, idx)
                )
            
            question_id += 1
    
    conn.commit()
    
    # 결과 확인
    cursor.execute('SELECT COUNT(*) FROM questions')
    total = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT c.name, COUNT(q.id)
        FROM categories c
        LEFT JOIN questions q ON c.id = q.category_id
        GROUP BY c.id
    ''')
    categories_count = cursor.fetchall()
    
    conn.close()
    
    print("\n" + "="*50)
    print("✅ 데이터베이스 동기화 완료!")
    print("="*50)
    for cat_name, count in categories_count:
        print(f"  {cat_name}: {count}개")
    print("="*50)
    print(f"📊 총 문제: {total}개\n")

if __name__ == '__main__':
    try:
        sync_db()
    except Exception as e:
        print(f"❌ 오류: {e}")
        import traceback
        traceback.print_exc()
