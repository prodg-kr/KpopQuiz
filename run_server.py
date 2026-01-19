#!/usr/bin/env python3
"""Flask 앱 실행"""
import sys
import os

# backend 폴더를 sys.path에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import app

if __name__ == '__main__':
    print("\n🚀 Flask 서버 시작 중...\n")
    print("📍 http://localhost:5000")
    print("✅ DB에 110개 문제가 동기화되어 있습니다.\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
