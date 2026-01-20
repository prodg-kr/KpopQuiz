#!/usr/bin/env python3
"""Flask 앱 실행"""
import sys
import os

# backend 폴더를 sys.path에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import app

if __name__ == '__main__':
    print("\nFlask server starting...\n")
    print("=" * 50)
    print("  KpopQuiz API Server")
    print("  http://localhost:5000")
    print("=" * 50)
    print("\nPress CTRL+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
