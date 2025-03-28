import subprocess
import sys
import os
import threading
import time

def stream_logs(process, service_name):
    """实时输出服务日志"""
    for line in iter(process.stdout.readline, ''):  # 改为空字符串
        print(f"[{service_name}] {line.strip()}")  # 移除 decode()

def run_services():
    """启动所有服务"""
    python = sys.executable
    
    print("\n=== 正在启动服务 ===")
    
    # 启动主服务
    main_service = subprocess.Popen(
        [python, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True
    )
    print("✓ 主服务已启动 (端口 8079)")
    
    # 启动AI服务
    ai_service = subprocess.Popen(
        [python, "chat_service.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True
    )
    print("✓ AI服务已启动 (端口 8181)\n")

    # 启动 Claude 服务（例如 Cloudflare Tunnel）
    claude_service = subprocess.Popen(
        ["cloudflared", "tunnel", "--config", r"C:\Users\buezw\.cloudflared\config.yml", "run"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True
    )
    print("✓ Claude 隧道已启动\n")

    
    # 创建日志监控线程
    main_thread = threading.Thread(target=stream_logs, args=(main_service, "主服务"))
    ai_thread = threading.Thread(target=stream_logs, args=(ai_service, "AI服务"))
    claude_thread = threading.Thread(target=stream_logs, args=(claude_service, "Claude隧道"))


    main_thread.daemon = True
    ai_thread.daemon = True
    claude_thread.daemon = True

    main_thread.start()
    ai_thread.start()
    claude_thread.start()

    try:
        while True:
            time.sleep(0.1)
            # 检查服务是否还在运行
            main_status = main_service.poll()
            ai_status = ai_service.poll()
            
            if main_status is not None:
                print(f"\n⚠️ 警告：主服务已停止 (状态码: {main_status})")
                break
            if ai_status is not None:
                print(f"\n⚠️ 警告：AI服务已停止 (状态码: {ai_status})")
                break
    except KeyboardInterrupt:
        print("\n正在关闭所有服务...")
        main_service.terminate()
        ai_service.terminate()
        claude_service.terminate()
        main_service.wait(timeout=5)
        ai_service.wait(timeout=5)
        claude_service.wait(timeout=5)
        print("✓ 服务已关闭")
        sys.exit(0)

if __name__ == "__main__":
    run_services()
