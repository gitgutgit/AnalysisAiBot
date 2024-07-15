python3 -m venv '.aivenv'   ->create venv
source .aivenv/bin/activate  

pip freeze > requirements.txt   요구상황 추출해내기
pip install -r requirements.txt 요구상황파일있을때 가져오기

ps aux | grep python


streamlit run AnalysisAiBot.py

uvicorn main:app --reload --port 8000 -> fastapi 가동 (8000은 포트번호)