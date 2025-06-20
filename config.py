import base64
import os

PROXY_SECRET_KEY = os.getenv("PROXY_SECRET_KEY")  # Flutter → Proxy 호출 시 보내야 할 인증 키 (임의 설정 가능)
BACKEND_API_URL = os.getenv("BACKEND_API_URL")    # 실제 GPT+Notion 처리 API의 주소
BACKEND_API_KEY = os.getenv("BACKEND_API_KEY")    # Proxy -> Lambda 호출 시 보내는 인증 키 (Base64 인코딩된 상태로 전송)