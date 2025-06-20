import base64
import os

PROXY_SECRET_KEY = os.getenv("PROXY_SECRET_KEY")  # Flutter → Proxy 호출 시 보내야 할 인증 키 (임의 설정 가능)
BACKEND_API_URL = os.getenv("BACKEND_API_URL")    # 실제 GPT+Notion 처리 API의 주소
# BACKEND_API_KEY = os.getenv("BACKEND_API_KEY")    # Proxy -> GPT API 서버의 문을 여는 열쇠?
encoded_key = os.getenv("BACKEND_API_KEY")
BACKEND_API_KEY = base64.b64decode(encoded_key).decode('utf-8') # Proxy -> GPT API 서버의 문을 여는 열쇠?