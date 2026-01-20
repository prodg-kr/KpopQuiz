#!/usr/bin/env python3
"""문제 분포 분석 및 10,000점 정규화 점수 계산"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import app
from backend.models import Question

with app.app_context():
    # 활성 문제 조회
    questions = Question.query.filter_by(is_active=True).all()
    
    # 난이도별 분포
    easy_count = sum(1 for q in questions if q.difficulty == 'easy')
    medium_count = sum(1 for q in questions if q.difficulty == 'medium')
    hard_count = sum(1 for q in questions if q.difficulty == 'hard')
    total_count = len(questions)
    
    print(f"=== 문제 분포 ===")
    print(f"Total: {total_count}")
    print(f"Easy: {easy_count}")
    print(f"Medium: {medium_count}")
    print(f"Hard: {hard_count}")
    print()
    
    # 10,000점 정규화 계산
    # 난이도 가중치: Easy=1, Medium=2, Hard=3
    weight_sum = easy_count * 1 + medium_count * 2 + hard_count * 3
    
    # 각 난이도별 기본 점수 (10,000점 기준)
    easy_points = round((10000 / weight_sum) * 1)
    medium_points = round((10000 / weight_sum) * 2)
    hard_points = round((10000 / weight_sum) * 3)
    
    # 실제 합산 점수
    actual_total = easy_count * easy_points + medium_count * medium_points + hard_count * hard_points
    
    print(f"=== 10,000점 정규화 ===")
    print(f"Weight Sum: {weight_sum}")
    print(f"Easy points: {easy_points}")
    print(f"Medium points: {medium_points}")
    print(f"Hard points: {hard_points}")
    print(f"Actual total: {actual_total}")
    print(f"Difference: {10000 - actual_total}")
    print()
    
    # 보정 (차이를 Hard 문제에 분산)
    if actual_total != 10000:
        diff = 10000 - actual_total
        hard_points += diff // hard_count if hard_count > 0 else 0
        remainder = diff % hard_count if hard_count > 0 else diff
        
        print(f"=== 보정 후 ===")
        print(f"Hard points (adjusted): {hard_points}")
        print(f"Remainder: {remainder}")
        
        actual_total = easy_count * easy_points + medium_count * medium_points + hard_count * hard_points + remainder
        print(f"Final total: {actual_total}")
