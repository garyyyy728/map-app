#!/usr/bin/env python3
"""
快速诊断和解决工具
自动检测问题并提供解决方案
"""

import socket
import os
import sys
from pathlib import Path

def print_section(title):
    """打印章节标题"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def check_port(port):
    """检查端口是否在监听"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    except:
        return False

def find_available_proxy():
    """查找可用的代理端口"""
    common_ports = [
        (7890, "Clash 默认端口"),
        (7891, "Clash 备用端口"),
        (10809, "V2rayN HTTP 端口"),
        (10808, "V2rayN Socks 端口"),
        (1080, "Shadowsocks 默认端口"),
        (1087, "Shadowsocks 备用端口"),
    ]
    
    print_section("🔍 步骤 1：检测代理端口")
    
    available_ports = []
    
    for port, name in common_ports:
        if check_port(port):
            print(f"✅ 找到代理：端口 {port} ({name})")
            available_ports.append((port, name))
        else:
            print(f"❌ 端口 {port} ({name}) - 未运行")
    
    return available_ports

def check_env_file():
    """检查 .env 文件"""
    print_section("🔍 步骤 2：检查 .env 配置")
    
    env_path = Path('.env')
    if not env_path.exists():
        print("❌ .env 文件不存在")
        return None
    
    content = env_path.read_text(encoding='utf-8')
    
    # 提取当前代理配置
    http_proxy = None
    for line in content.split('\n'):
        if line.startswith('HTTP_PROXY'):
            http_proxy = line.split('=')[1].strip()
            break
    
    if http_proxy:
        print(f"✅ .env 文件存在")
        print(f"📝 当前配置: {http_proxy}")
        
        # 提取端口
        try:
            port = int(http_proxy.split(':')[-1])
            return port
        except:
            return None
    else:
        print("⚠️  .env 文件存在但未配置代理")
        return None

def provide_solution(available_ports, configured_port):
    """提供解决方案"""
    print_section("💡 诊断结果与解决方案")
    
    if not available_ports:
        # 没有找到运行中的代理
        print("❌ 问题：没有检测到运行中的代理服务器")
        print("\n🔧 解决方案：")
        print("\n1️⃣  安装并启动代理工具（选择其中一个）：")
        print("   • Clash for Windows (推荐)")
        print("   • V2rayN")
        print("   • Shadowsocks")
        print("\n2️⃣  启动代理后，重新运行本脚本")
        print("\n📖 详细说明请查看：解决方案.md")
        return False
    
    # 找到了代理
    print(f"✅ 检测到 {len(available_ports)} 个可用的代理端口")
    
    recommended_port, recommended_name = available_ports[0]
    
    if configured_port == recommended_port:
        print(f"\n✅ 配置正确！代理端口 {recommended_port} 正在运行")
        print("\n🚀 下一步：启动后端服务")
        print("\n   python main.py")
        return True
    else:
        print(f"\n⚠️  配置不匹配！")
        print(f"   .env 中配置的端口: {configured_port}")
        print(f"   实际运行的代理端口: {recommended_port}")
        print(f"\n🔧 解决方案：")
        
        # 询问是否自动修复
        print(f"\n建议更新 .env 为：")
        print(f"   HTTP_PROXY=http://127.0.0.1:{recommended_port}")
        print(f"   HTTPS_PROXY=http://127.0.0.1:{recommended_port}")
        
        print(f"\n是否自动更新？(y/n): ", end='')
        try:
            choice = input().lower()
            if choice == 'y':
                update_env_proxy(recommended_port)
                print("\n✅ .env 已更新！")
                print("\n🚀 现在可以启动服务了：python main.py")
                return True
            else:
                print("\n请手动修改 .env 文件后再启动服务")
                return False
        except:
            print("\n请手动修改 .env 文件后再启动服务")
            return False

def update_env_proxy(port):
    """更新 .env 中的代理配置"""
    env_path = Path('.env')
    
    if env_path.exists():
        content = env_path.read_text(encoding='utf-8')
        
        # 删除旧的代理配置
        lines = []
        for line in content.split('\n'):
            if not line.startswith('HTTP_PROXY') and not line.startswith('HTTPS_PROXY'):
                lines.append(line)
        
        # 删除末尾的空行
        while lines and not lines[-1].strip():
            lines.pop()
        
        # 添加新的代理配置
        lines.append('')
        lines.append('# 代理配置（自动更新）')
        lines.append(f'HTTP_PROXY=http://127.0.0.1:{port}')
        lines.append(f'HTTPS_PROXY=http://127.0.0.1:{port}')
        
        env_path.write_text('\n'.join(lines), encoding='utf-8')

def show_startup_guide():
    """显示启动指南"""
    print_section("📋 快速启动指南")
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║                    后端服务启动步骤                              ║
╚════════════════════════════════════════════════════════════════╝

1️⃣  启动后端服务：
   python main.py

2️⃣  测试 API（新开终端）：
   python test_image_api.py

3️⃣  或打开网页测试：
   打开 web_image_upload.html

╔════════════════════════════════════════════════════════════════╗
║                         重要提示                                ║
╚════════════════════════════════════════════════════════════════╝

⚠️  在使用期间，代理工具必须保持运行
⚠️  如果关闭代理，服务将无法连接到 Gemini API
⚠️  建议选择延迟低的节点（美国/日本/新加坡）

📖 详细文档：
   • 解决方案.md - 完整的问题解决指南
   • PROXY_SETUP.md - 代理配置详解
   • QUICKSTART.md - 快速开始指南
    """)

def main():
    """主函数"""
    print("\n🚀 Gemini API 快速诊断工具")
    print("="*70)
    print("此工具将自动检测问题并提供解决方案\n")
    
    # 1. 检测可用的代理端口
    available_ports = find_available_proxy()
    
    # 2. 检查 .env 配置
    configured_port = check_env_file()
    
    # 3. 提供解决方案
    is_ready = provide_solution(available_ports, configured_port)
    
    # 4. 显示启动指南
    if is_ready:
        show_startup_guide()
    
    print("\n" + "="*70)
    print("诊断完成！")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消")
        sys.exit(0)

