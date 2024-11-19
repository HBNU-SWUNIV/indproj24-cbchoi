import json
import urllib.parse

from fastapi.responses import HTMLResponse, Response
from pathlib import Path
from fastapi import APIRouter, Depends, Request, status, FastAPI

from ..models.database import db_manager
from ..instance.config import MONGODB_URL, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(include_in_schema=False)
db_manager.init_manager(MONGODB_URL, "simulverse")

data = {}

@router.get("/signaling")
def ok():
    return Response(content='{"status":"ok"}', status_code=200, media_type='application/json')

@router.post("/signaling/offer")
async def offer(request: Request) -> Response:
    """ Offer post

    Args:
        request (Request): request from offer

    Returns:
        Response: status_code
    """
  
    form = await request.form()
    if form.get("type") == "offer":
        data["offer"] = {"id": form.get("id"), "type": form.get("type"), "sdp": form.get("sdp")}
        print(data["offer"])
        return Response(content='{"status":"ok"}',status_code = 200)
    else:
        return Response(status_code=400)
    
@router.post("/signaling/answer")
async def answer(request: Request) -> Response:
    """_summary_

    Args:
        request (Request): request from answer

    Returns:
        Response: status_code
    """
    
    req = await request.body()
    
    decoded_data = urllib.parse.unquote(req)
    
    req_result = json.loads(decoded_data)
    
    if req_result["type"] == "Answer":
        data["answer"] = {"id" : req_result['id'], "type" : req_result['type'], "sdp":req_result['sdp']}
        return Response(status_code=200)
    else: 
        return Response(status_code= 400)       
    
    

@router.get("/signaling/get_offer")
def get_offer() -> Response:
    # 카메라 데이터 확인
    if "offer" in data:
        # 카메라 데이터 json객체로 저장
        j = json.dumps(data["offer"])
        # json객체로 저장한 데이터 삭제
        del data["offer"]
        # 상태 코드 및 json파일 반환
        return Response(j, status_code =200, media_type='application/json')
    else: 
        return Response(status_code =503)    
    
@router.get("/signaling/get_answer")
def get_answer() -> Response:
    if "answer" in data:
        j = json.dumps(data["answer"])
        del data["answer"]
        return Response(j, status_code = 200, media_type='application/json')
    else:
        return Response(status_code = 503)    
