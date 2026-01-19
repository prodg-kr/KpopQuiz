#!/usr/bin/env python
# -*- coding: utf-8 -*-

readme_content = """# 🎵 KpopQuiz

2020년 이후 데뷔한 여자 걸그룹 중심의 K-pop 퀴즈 애플리케이션입니다.

## 🚀 시작하기

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 데이터베이스 초기화
```bash
python init_db.py
```

### 3. 백엔드 실행
```bash
python backend/app.py
```

서버: `http://localhost:5000`

## 📁 프로젝트 구조

```
KpopQuiz/
├── backend/          # Flask 백엔드
├── frontend/         # 프론트엔드
├── questions.json    # 100개 문제 데이터
├── kpop_quiz.db      # SQLite DB (자동 생성)
├── init_db.py        # DB 초기화 스크립트
└── requirements.txt
```

## 🔌 주요 API

- `GET /api/categories` - 카테고리 조회
- `GET /api/quiz?category=artist&limit=10` - 퀴즈 문제 조회
- `POST /api/quiz/{id}/check` - 답변 검증
- `GET /api/quiz/stats` - 통계
- `POST /api/admin/questions` - 문제 추가

## 📊 데이터베이스

- **Categories**: artist, song, general
- **Questions**: 100개 문제
- **Options**: 정규화된 선택지
- **UserScores**: 사용자 점수 기록

## 🎯 포함된 여자 걸그룹

AESPA, NewJeans, IVE, Le Sserafim, STAYC, BABYMONSTER, FIFTY FIFTY, LOONA

**총 100개 문제**: 34(아티스트) + 33(노래) + 33(일반)

## 🔧 기술 스택
- Flask, SQLAlchemy, SQLite
- HTML5, CSS3, JavaScript

---
**v2.0.0** | 2026-01-19
"""

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)

print("✅ README.md 업데이트 완료")
