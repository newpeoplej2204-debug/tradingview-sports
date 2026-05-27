
# Result Candle Sports Trading Terminal

## 변경 사항
- 득점/실점 기반 OHLC 제거
- 경기 결과 기반 캔들 구조 적용
- 승리 = 빨간 캔들
- 무승부 = 초록 캔들
- 패배 = 파란 캔들
- TradingView 스타일 UI
- 스크롤/확대/축소 지원
- 화면 분할 지원
- 홈/원정 독립 캔들 개수 선택 가능

## 실행
pip install -r requirements.txt
streamlit run app.py
