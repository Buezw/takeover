import subprocess
import os
import time

# 你的 FastAPI 启动命令（改成你实际文件名和 app 对象名）
fastapi_cmd = ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8079"]

# cloudflared config 路径（根据你实际修改）
cloudflared_config_path = r"C:\Users\buezw\.cloudflared\config.yml"
cloudflared_cmd = ["cloudflared", "tunnel", "--config", cloudflared_config_path, "run"]

print("🚀 正在启动 FastAPI 服务...")
fastapi_process = subprocess.Popen(fastapi_cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)

time.sleep(2)  # 等 2 秒再启动 tunnel，避免端口未准备好

print("🌐 正在启动 Cloudflare Tunnel...")
cloudflared_process = subprocess.Popen(cloudflared_cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)

print("✅ 所有服务已启动！按 Ctrl+C 可手动关闭。")

try:
    fastapi_process.wait()
    cloudflared_process.wait()
except KeyboardInterrupt:
    print("🛑 检测到退出指令，正在关闭服务...")
    fastapi_process.terminate()
    cloudflared_process.terminate()
