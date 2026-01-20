#!/usr/bin/env python3
"""10,000점 정규화 점수 업데이트 스크립트"""
import sqlite3
import os

# DB 경로
db_path = os.path.join(os.path.dirname(__file__), 'kpop_quiz.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 활성 문제 난이도별 카운트
cursor.execute("SELECT difficulty, COUNT(*) FROM questions WHERE is_active = 1 GROUP BY difficulty")
difficulty_counts = {row[0]: row[1] for row in cursor.fetchall()}

easy_count = difficulty_counts.get('easy', 0)
medium_count = difficulty_counts.get('medium', 0)
hard_count = difficulty_counts.get('hard', 0)
total_count = easy_count + medium_count + hard_count

print(f"=== 문제 분포 ===")
print(f"Total: {total_count}")
print(f"Easy: {easy_count}")
print(f"Medium: {medium_count}")
print(f"Hard: {hard_count}")
print()

# 10,000점 정규화 계산
# 난이도 가중치: Easy=1, Medium=2, Hard=3
weight_sum = easy_count * 1 + medium_count * 2 + hard_count * 3

# 각 난이도별 기본 점수
base_point = 10000 / weight_sum
easy_points = round(base_point * 1)
medium_points = round(base_point * 2)
hard_points = round(base_point * 3)

# 실제 합산
actual_total = easy_count * easy_points + medium_count * medium_points + hard_count * hard_points
diff = 10000 - actual_total

print(f"=== 10,000점 정규화 ===")
print(f"Weight Sum: {weight_sum}")
print(f"Base Point: {base_point:.2f}")
print(f"Easy points: {easy_points}")
print(f"Medium points: {medium_points}")
print(f"Hard points: {hard_points}")
print(f"Actual total: {actual_total}")
print(f"Difference: {diff}")
print()

# 보정: 차이를 Hard 문제에 분산
if diff != 0 and hard_count > 0:
    hard_points += diff // hard_count
    remainder = diff % hard_count
    print(f"=== 보정 후 ===")
    print(f"Hard points (adjusted): {hard_points}")
    print(f"Remainder to distribute: {remainder}")
    
    actual_total = easy_count * easy_points + medium_count * medium_points + hard_count * hard_points + remainder
    print(f"Final total: {actual_total}")
    print()

# DB 업데이트
print("=== DB 업데이트 중 ===")
cursor.execute("UPDATE questions SET points = ? WHERE difficulty = 'easy' AND is_active = 1", (easy_points,))
cursor.execute("UPDATE questions SET points = ? WHERE difficulty = 'medium' AND is_active = 1", (medium_points,))
cursor.execute("UPDATE questions SET points = ? WHERE difficulty = 'hard' AND is_active = 1", (hard_points,))

conn.commit()
print(f"Easy 문제 {easy_count}개 → {easy_points}점")
print(f"Medium 문제 {medium_count}개 → {medium_points}점")
print(f"Hard 문제 {hard_count}개 → {hard_points}점")
print()

# 검증
cursor.execute("SELECT SUM(points) FROM questions WHERE is_active = 1")
final_sum = cursor.fetchone()[0]
print(f"=== 검증 ===")
print(f"Total points in DB: {final_sum}")
print(f"Target: 10000")
print(f"Match: {'✓' if final_sum == 10000 else '✗'}")

conn.close()
