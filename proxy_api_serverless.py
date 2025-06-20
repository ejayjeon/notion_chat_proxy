from fastapi import FastAPI, Request, HTTPException
from config import PROXY_SECRET_KEY, BACKEND_API_URL, BACKEND_API_KEY
import httpx

app = FastAPI()


@app.post("/proxy-ask")
async def proxy_ask(request: Request):
    client_key = request.headers.get("X-PUBLIC-KEY")
    print(f"client_key: {client_key}")
    # Flutter → Proxy 호출 시 보내야 할 인증 키 (임의 설정 가능)
    if client_key != PROXY_SECRET_KEY:
        raise HTTPException(status_code=401, detail="❌ 인증 실패: 유효하지 않은 키")

    body = await request.json()

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(
            BACKEND_API_URL,
            headers={
                "Content-Type": "application/json",
                "X-API-KEY": BACKEND_API_KEY  # 내부 보호용 키
            },
            json=body
        )
    return response.json()