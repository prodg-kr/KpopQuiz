import sqlite3
conn = sqlite3.connect('kpop_quiz.db')
c = conn.cursor()

# 첫 41개 Hard 문제를 122점으로, 나머지를 121점으로
c.execute('UPDATE questions SET points = 122 WHERE difficulty = "hard" AND is_active = 1')
c.execute('SELECT id FROM questions WHERE difficulty = "hard" AND is_active = 1 ORDER BY id LIMIT 17')
ids_to_reduce = [row[0] for row in c.fetchall()]

for qid in ids_to_reduce:
    c.execute('UPDATE questions SET points = 121 WHERE id = ?', (qid,))

conn.commit()

# 검증
c.execute('SELECT SUM(points) FROM questions WHERE is_active = 1')
total = c.fetchone()[0]
print(f'Total points: {total}')

c.execute('SELECT difficulty, points, COUNT(*) FROM questions WHERE is_active = 1 GROUP BY difficulty, points')
for row in c.fetchall():
    print(f'{row[0]}: {row[1]}pt x {row[2]} = {row[1] * row[2]}')

conn.close()
