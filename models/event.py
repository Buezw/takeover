from pydantic import BaseModel
from typing import Optional

class Event(BaseModel):
    id: Optional[int] = None       # 事件ID，可选
    title: str                     # 事件标题，必填
    description: Optional[str] = "" # 事件描述，可选
    date: str                      # 事件日期，必填，格式: "YYYY-MM-DD"
    time_start: Optional[str] = "" # 开始时间，可选，格式: "HH:MM"
    time_end: Optional[str] = ""   # 结束时间，可选，格式: "HH:MM"
