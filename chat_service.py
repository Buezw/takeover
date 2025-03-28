from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import re
from datetime import datetime, timedelta
import httpx
import json
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, EVENT_PROMPT, ERROR_MESSAGES
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

# 更新 CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ 先用通配测试
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("⚠️ 请求验证失败:")
    print(exc)
    return await request_validation_exception_handler(request, exc)


async def create_event_via_api(event_data: dict) -> dict:
    """通过主服务API创建事件"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8079/api/events",
                json=event_data
            )
            return response.json()
        except Exception as e:
            print(f"创建事件API错误: {e}")
            return event_data  # 出错时返回原始数据

async def call_deepseek_api(prompt: str) -> dict:
    """调用 DeepSeek API"""
    async with httpx.AsyncClient() as client:
        try:
            # 准备当前日期信息，用于相对日期的解析
            current_date = datetime.now().strftime("%Y-%m-%d")
            formatted_prompt = EVENT_PROMPT.format(
                current_date=current_date,
                user_input=prompt
            )
            
            # 调试信息
            print(f"发送到DeepSeek的提示: {formatted_prompt}")
            print(f"API URL: {DEEPSEEK_API_URL}")
            print(f"API Key: {DEEPSEEK_API_KEY[:5]}...")
            
            request_data = {
                "messages": [
                    {"role": "system", "content": "你是一个日历助手，专门帮助用户创建日程事件。请始终返回JSON格式的数据。"},
                    {"role": "user", "content": formatted_prompt}
                ],
                "model": "deepseek-chat",
                "temperature": 0.2,
                "max_tokens": 800
            }
            
            print(f"请求数据: {json.dumps(request_data, ensure_ascii=False)[:100]}...")
            
            response = await client.post(
                DEEPSEEK_API_URL,
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=request_data,
                timeout=30.0
            )
            
            # 检查响应状态
            print(f"响应状态码: {response.status_code}")
            response.raise_for_status()
            
            result = response.json()
            
            # 提取AI响应文本
            ai_response = result['choices'][0]['message']['content']
            print(f"AI Response: {ai_response}")
            
            # 清理和解析JSON
            json_str = ai_response.strip()
            if not json_str.startswith('{'): 
                json_match = re.search(r'({[\s\S]*?})', json_str)
                if json_match:
                    json_str = json_match.group(1)
            
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                print(f"原始响应: {json_str}")
                return {}
                
        except httpx.TimeoutException:
            print("DeepSeek API 超时")
            return {}
        except Exception as e:
            print(f"DeepSeek API 错误: {str(e)}")
            return {}

@app.post("/chat")
async def chat_with_ai(message: ChatMessage):
    try:
        print(f"收到消息: {message}")

        user_message = message.message

        # 检测是否是添加事件的请求
        if any(keyword in user_message.lower() for keyword in ["添加", "创建", "安排", "预定"]):
            # 使用 DeepSeek 解析事件信息
            event_data = await call_deepseek_api(user_message)
            
            # 调试输出
            print(f"解析后的事件数据: {event_data}")
            
            # 验证返回的数据
            if not event_data or not event_data.get("date") or not event_data.get("title"):
                return {
                    "response": ERROR_MESSAGES["parse_error"]
                }
            # ✅ 自动保存事件到主服务
            await create_event_via_api(event_data)


            # 构建友好的响应
            time_info = event_data.get('time_start', '全天')
            if event_data.get('time_end'):
                time_info += f" - {event_data['time_end']}"
            
            return {
                "response": f"✅ 已理解您的需求，将添加以下事件:\n"
                          f"{event_data['title']}\n"
                          f"{event_data['date']}\n"
                          f"{time_info}\n"
                          f"{event_data.get('description', '无描述')}",
                "event": event_data
            }
        
        # 其他一般对话
        return {
            "response": "我是您的日历助手，您可以这样安排事件：\n"
                      "- 添加明天下午3点的团队会议\n"
                      "- 创建下周一上午10点的项目评审\n"
                      "- 安排2024年1月20日全天的年会"
        }
    except Exception as e:
        print(f"处理聊天消息错误: {e}")
        return {"response": ERROR_MESSAGES["api_error"]}

if __name__ == "__main__":
    uvicorn.run("chat_service:app", host="127.0.0.1", port=8181, reload=True)
