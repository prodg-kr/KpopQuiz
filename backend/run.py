#!/usr/bin/env python3
"""Flask 앱 직접 실행 - DB 자동 동기화"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app import app

if __name__ == '__main__':
    print("\n🚀 Flask 서버 시작 중...\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
