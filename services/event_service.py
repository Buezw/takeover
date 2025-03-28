import json
import os
from typing import List, Optional
from models.event import Event

class EventService:
    def __init__(self):
        # 设置数据文件路径
        self.data_file = os.path.join("static", "data", "events.json")
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure the data file exists"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump([], f)
    
    def get_all_events(self) -> List[Event]:
        """获取所有事件"""
        # 从文件读取并返回所有事件
        with open(self.data_file, "r", encoding="utf-8") as f:
            return [Event(**event) for event in json.load(f)]
    
    def get_events_by_date(self, date: str) -> List[Event]:
        """获取某一天的事件"""
        # 返回指定日期的所有事件
        events = self.get_all_events()
        return [event for event in events if event.date == date]
    
    def get_events_by_month(self, year: str, month: str) -> List[Event]:
        """获取指定月份的事件"""
        events = self.get_all_events()
        prefix = f"{year}-{month.zfill(2)}"
        return [event for event in events if event.date.startswith(prefix)]
    
    def create_event(self, event: Event) -> Event:
        """创建新事件"""
        # 添加新事件到文件
        events = self.get_all_events()
        event.id = max([e.id for e in events], default=0) + 1
        events.append(event)
        self._save_events(events)
        return event
    
    def delete_event(self, event_id: int) -> Optional[Event]:
        """删除事件"""
        # 从文件中删除指定事件
        events = self.get_all_events()
        event = next((e for e in events if e.id == event_id), None)
        if event:
            events = [e for e in events if e.id != event_id]
            self._save_events(events)
        return event
    
    def _save_events(self, events: List[Event]):
        """Save events to file"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([event.dict() for event in events], f, indent=4)
