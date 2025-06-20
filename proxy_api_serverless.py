from fastapi import FastAPI, Request, HTTPException
from config import PROXY_SECRET_KEY, BACKEND_API_URL, BACKEND_API_KEY
import httpx

app = FastAPI()


@app.post("/proxy-ask")
async def proxy_ask(request: Request):
    try:
        client_key = request.headers.get("X-PUBLIC-KEY")
        print(f"client_key: {client_key}")
        print(f"PROXY_SECRET_KEY: {PROXY_SECRET_KEY}")
        
        # Flutter → Proxy 호출 시 보내야 할 인증 키 (임의 설정 가능)
        if client_key != PROXY_SECRET_KEY:
            raise HTTPException(status_code=401, detail="❌ 인증 실패: 유효하지 않은 키")

        body = await request.json()
        print(f"Request body: {body}")

        async with httpx.AsyncClient(timeout=60.0) as client:
            print(f"Sending request to: {BACKEND_API_URL}")
            response = await client.post(
                BACKEND_API_URL,
                headers={
                    "Content-Type": "application/json",
                    "X-API-KEY": BACKEND_API_KEY  # 내부 보호용 키
                },
                json=body
            )
            
            print(f"Backend response status: {response.status_code}")
            print(f"Backend response headers: {response.headers}")
            
            # 응답 상태 코드 확인
            if response.status_code != 200:
                try:
                    error_body = response.json()
                    print(f"Backend error response: {error_body}")
                    raise HTTPException(status_code=response.status_code, detail=f"Backend error: {error_body}")
                except:
                    print(f"Backend error text: {response.text}")
                    raise HTTPException(status_code=response.status_code, detail=f"Backend error: {response.text}")
            
            # 성공 응답 처리
            try:
                result = response.json()
                print(f"Backend success response: {result}")
                return result
            except Exception as e:
                print(f"Failed to parse backend response as JSON: {e}")
                print(f"Response text: {response.text}")
                raise HTTPException(status_code=500, detail="백엔드 응답 파싱 실패")
                
    except HTTPException:
        # FastAPI HTTPException은 다시 raise
        raise
    except Exception as e:
        print(f"Unexpected error in proxy_ask: {str(e)}")
        raise HTTPException(status_code=500, detail=f"프록시 서버 오류: {str(e)}")