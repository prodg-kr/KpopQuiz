# 🐍 Python 설치 및 설정 가이드

## 📋 요구사항

- **Windows 10/11** 또는 **macOS/Linux**
- Python 3.11 이상

## 💻 Windows 설치 (권장)

### 방법 1: python.org에서 직접 설치 (가장 확실)

1. **Python 다운로드**
   - https://www.python.org/downloads/ 방문
   - "Download Python 3.11" 클릭 (또는 최신 버전)

2. **설치 마법사 실행**
   - 설치 파일(.exe) 실행
   - ⚠️ **중요**: "Add Python to PATH" 체크 ✅
   - "Install Now" 클릭
   - 설치 완료 대기 (약 1분)

3. **설치 확인**
   ```powershell
   python --version
   # 출력: Python 3.11.x
   ```

### 방법 2: Windows Package Manager (winget)

```powershell
winget install Python.Python.3.11
```

### 방법 3: Microsoft Store

1. **Microsoft Store** 열기
2. **"Python 3.11"** 검색
3. **설치** 클릭

---

## 🍎 macOS 설치

### Homebrew 사용 (권장)

```bash
# Homebrew 설치 (미설치 시)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 설치
brew install python@3.11
```

---

## 🐧 Linux 설치

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

### Fedora/CentOS

```bash
sudo dnf install python3.11 python3-pip
```

---

## 🚀 Flask 백엔드 실행

### 1단계: 저장소 클론

```bash
git clone https://github.com/prodg-kr/KpopQuiz.git
cd KpopQuiz
```

### 2단계: 가상 환경 생성 (선택사항이지만 권장)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3단계: 의존성 설치

```bash
pip install -r requirements.txt
```

설치 확인:
```bash
pip list
# Flask, Flask-SQLAlchemy, Flask-CORS 등이 표시되어야 함
```

### 4단계: 서버 실행

```bash
python run_server.py
```

출력:
```
🚀 Flask 서버 시작 중...
📍 http://localhost:5000
✅ DB에 110개 문제가 동기화되어 있습니다.

WARNING: This is a development server...
* Running on http://0.0.0.0:5000
* Press CTRL+C to quit
```

### 5단계: 브라우저에서 열기

- http://localhost:5000 을 브라우저에서 열기

---

## 🔧 문제 해결

### "python: 명령을 찾을 수 없습니다"

**원인**: Python이 PATH에 없음

**해결**:
1. Python 재설치 시 "Add Python to PATH" 반드시 체크
2. 또는 PowerShell 재시작

```powershell
# Python 위치 확인
where python

# 없으면 전체 경로로 실행
C:\Users\YIM\AppData\Local\Programs\Python\Python311\python.exe run_server.py
```

### "ModuleNotFoundError: No module named 'flask'"

**원인**: 의존성이 설치되지 않음

**해결**:
```bash
pip install -r requirements.txt
```

### "Port 5000 is already in use"

**원인**: 다른 프로그램이 포트 5000을 사용 중

**해결**:
```bash
# 포트를 사용 중인 프로세스 확인 (Windows)
netstat -ano | findstr :5000

# 프로세스 종료
taskkill /PID <PID> /F
```

### 데이터베이스 오류

**원인**: DB 스키마 불일치

**해결**:
```bash
# DB 재동기화
python sync_questions.py

# 또는 서버 재시작
python run_server.py
```

---

## ✅ 설치 확인 체크리스트

- [ ] Python 3.11+ 설치됨
- [ ] `pip --version` 작동함
- [ ] 가상환경 활성화됨 (선택사항)
- [ ] `pip install -r requirements.txt` 완료
- [ ] `python run_server.py` 실행됨
- [ ] http://localhost:5000 접속 가능

---

## 📞 추가 도움

- Python 공식 문서: https://docs.python.org/3/
- Flask 문서: https://flask.palletsprojects.com/
- GitHub Issues: https://github.com/prodg-kr/KpopQuiz/issues


