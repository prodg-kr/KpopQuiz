# Python 3.11 설치 방법 (Windows)

## 옵션 1: python.org에서 직접 설치 (권장)
1. https://www.python.org/downloads/ 방문
2. "Download Python 3.11.x" 클릭
3. 설치 마법사에서:
   - ✅ "Add Python 3.11 to PATH" 체크 (중요!)
   - "Install Now" 클릭
4. 설치 완료 후 PowerShell 재시작

## 옵션 2: Microsoft Store에서 설치
1. Windows 시작 → "Microsoft Store" 열기
2. "Python 3.11" 검색
3. 설치 클릭

## 옵션 3: Windows Package Manager (winget)
```powershell
winget install Python.Python.3.11
```

## 검증 (설치 후)
```powershell
python --version
# Python 3.11.x 출력되어야 함
```

## 그 후 실행
```powershell
cd c:\_github\KpopQuiz
python init_db.py
# 110개 문제가 DB에 추가됩니다
```

## 문제 해결
만약 설치 후에도 "python: 명령을 찾을 수 없습니다" 오류가 나면:
1. Python 설치 시 PATH에 체크했는지 확인
2. PowerShell을 재시작
3. 안 되면 경로로 직접 실행:
   python3 init_db.py
