# 🎤 KpopQuiz - K-pop 지식 퀴즈 게임

> **BTS, BLACKPINK, NewJeans** 등 K-pop 아티스트에 대한 지식을 테스트하는 재미있는 퀴즈 게임!

[![GitHub Pages](https://img.shields.io/badge/Play%20Now-GitHub%20Pages-blue?style=flat-square&logo=github)](https://prodg-kr.github.io/KpopQuiz/)

## ✨ 주요 기능

- 🎯 **110개의 다양한 문제** (아티스트, 노래, 일반 지식)
- 🎨 **모던 UI** - 어두운 테마, 반응형 디자인
- 📊 **실시간 스코어** - 정답/오답 카운팅
- 📱 **완벽한 모바일 지원** - 모든 기기에서 최적화
- 🎵 **카테고리 필터링** - 원하는 카테고리만 선택
- 🎪 **난이도 선택** - Easy, Medium, Hard

## 🚀 빠른 시작

### 옵션 1: 온라인 플레이 (권장)
👉 [GitHub Pages에서 바로 플레이](https://prodg-kr.github.io/KpopQuiz/)

### 옵션 2: 로컬 실행 (VS Code Live Server)
```bash
1. 이 저장소를 클론합니다
   git clone https://github.com/prodg-kr/KpopQuiz.git
   cd KpopQuiz

2. VS Code에서 index.html을 열기
3. Live Server 확장 설치 (Install)
4. index.html 우클릭 → "Open with Live Server"
5. 브라우저에서 http://127.0.0.1:5500 열기
```

### 옵션 3: 백엔드 API와 함께 실행
```bash
# Python 3.11+ 필요
1. 저장소 클론
   git clone https://github.com/prodg-kr/KpopQuiz.git
   cd KpopQuiz

2. 의존성 설치
   pip install -r requirements.txt

3. Flask 서버 실행
   python run_server.py

4. 브라우저에서 http://localhost:5000 열기
```

## 📁 프로젝트 구조
```
KpopQuiz/
├── index.html           # 프론트엔드 (Vue.js 기반 SPA)
├── questions.json       # 110개 문제 데이터 (JSON)
├── requirements.txt     # Python 의존성
├── run_server.py        # Flask 서버 실행 스크립트
├── sync_questions.py    # DB 동기화 스크립트
├── kpop_quiz.db         # SQLite 데이터베이스
└── backend/
    ├── app.py           # Flask 메인 앱 (11개 API 엔드포인트)
    ├── models.py        # SQLAlchemy ORM 모델
    ├── database.py      # DB 초기화
    ├── config.py        # Flask 설정
    ├── seed_data.py     # 시드 데이터
    └── routes/          # 라우트 정의 (선택사항)
```

## 🎮 게임 화면

### 메인 화면
- 카테고리 선택 (Artist, Song, General)
- 난이도 선택 (Easy, Medium, Hard)
- 문제 개수 선택

### 퀀즈 화면
- 실시간 점수 표시
- 4개 선택지
- 다음 문제 버튼
- 진행 상황 표시

### 결과 화면
- 최종 점수
- 정답/오답 비율
- 다시하기 버튼

## 📊 데이터 구조

### 문제 데이터 (questions.json)
```json
{
  "version": "2.0.0",
  "totalQuestions": 110,
  "categories": {
    "artist": [
      {
        "id": "art001",
        "question": "질문 텍스트",
        "options": ["선택지1", "선택지2", "선택지3", "선택지4"],
        "answer": 1,
        "explanation": "설명",
        "difficulty": "easy"
      }
    ],
    "song": [...],
    "general": [...]
  }
}
```

### DB 스키마
```
Categories
├── id (PK)
├── name (UNIQUE)
└── description

Questions
├── id (PK)
├── category_id (FK)
├── question
├── explanation
├── difficulty
└── created_at, updated_at

Options
├── id (PK)
├── question_id (FK)
├── option_text
├── is_correct
└── order_num
```

## 🔌 API 엔드포인트

### 헬스 체크
```
GET /api/health
```

### 카테고리
```
GET /api/categories
```

### 퀴즈
```
GET /api/quiz?category=artist&difficulty=medium&limit=10&random=true
```

### 점수 확인
```
GET /api/quiz/stats
```

### 어드민 (문제 관리)
```
POST   /api/admin/questions         # 새 문제 추가
PUT    /api/admin/questions/<id>    # 문제 수정
DELETE /api/admin/questions/<id>    # 문제 삭제
```

## 🛠️ 개발 환경 설정

### 요구 사항
- Python 3.11+
- Node.js (선택사항, 빌드 시에만)
- VS Code (권장)

### 설치

```bash
# 1. 저장소 클론
git clone https://github.com/prodg-kr/KpopQuiz.git
cd KpopQuiz

# 2. Python 환경 설정
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 3. 의존성 설치
pip install -r requirements.txt

# 4. DB 동기화 (선택)
python sync_questions.py

# 5. Flask 서버 실행
python run_server.py
```

## 📚 기술 스택

### 프론트엔드
- HTML5
- CSS3 (반응형, 다크테마)
- Vanilla JavaScript (ES6+)

### 백엔드
- Flask 2.3.3
- SQLAlchemy 2.0.21
- SQLite
- Python 3.11

### 배포
- GitHub Pages (정적 호스팅)
- GitHub Actions (자동 배포)

## 📝 문제 데이터

### 카테고리별 분류
- **Artist (36개)**: 아티스트 정보, 데뷔 연도, 멤버 등
- **Song (37개)**: 노래 정보, 뮤직비디오, 차트 순위 등
- **General (37개)**: K-pop 일반 지식

### 난이도별 분류
- **Easy**: 기본 정보
- **Medium**: 심화 정보
- **Hard**: 세부 정보

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

## 👨‍💻 저자

**prodg-kr** - [GitHub Profile](https://github.com/prodg-kr)

## 🎯 향후 계획

- [ ] 사용자 로그인 시스템
- [ ] 개인 통계 저장
- [ ] 랭킹 시스템
- [ ] 모바일 앱 (React Native)
- [ ] 다국어 지원
- [ ] 오디오 기능
- [ ] 커뮤니티 기능

## 📞 연락처

- GitHub Issues: [Issues](https://github.com/prodg-kr/KpopQuiz/issues)
- Email: prodg.kr@gmail.com

---

**⭐ 별 🌟을 주시면 감사합니다!**