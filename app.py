from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models.event import Event
from services.event_service import EventService
import os
import shutil
import uvicorn
from fastapi import Request
from fastapi.responses import Response
import httpx


app = FastAPI()
event_service = EventService()

# Setup static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("calender.html", {"request": request})

@app.get("/api/events")
async def get_events(date: str = None, year: str = None, month: str = None):
    if date:
        return event_service.get_events_by_date(date)
    if year and month:
        return event_service.get_events_by_month(year, month)
    return event_service.get_all_events()

@app.post("/api/events", status_code=201)
async def create_event(event: Event):
    return event_service.create_event(event)

@app.delete("/api/events/{event_id}")
async def delete_event(event_id: int):
    return event_service.delete_event(event_id)

@app.api_route("/chat", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@app.api_route("/chat/", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def proxy_chat(request: Request):
    method = request.method
    headers = dict(request.headers)
    body = await request.body()

    url = "http://127.0.0.1:8181/chat"
    timeout = httpx.Timeout(
        timeout=120.0,
        connect=10.0,
        read=50.0,
        write=20.0
    )

    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.request(method, url, headers=headers, content=body)
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=resp.headers
        )


def setup_app():
    """Setup necessary directories and files"""
    for dir_path in ["templates", "static", "static/data"]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    
    # 总是复制最新的 calender.html 到 templates 目录，无论文件是否已存在
    source_path = "calender.html"
    target_path = os.path.join("templates", "calender.html")
    if os.path.exists(source_path):
        print(f"正在更新模板文件: {target_path}")
        shutil.copy2(source_path, target_path)
    else:
        print(f"警告: 源文件 {source_path} 不存在")

if __name__ == "__main__":
    setup_app()
    uvicorn.run("app:app", host="127.0.0.1", port=8079, reload=True)
