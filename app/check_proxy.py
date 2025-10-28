#!/usr/bin/env python3
"""
代理配置检查和诊断工具
快速检查代理设置是否正确
"""

import os
import sys
import requests
from pathlib import Path

def print_header(text):
    """打印标题"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def check_env_file():
    """检查 .env 文件"""
    print_header("1. 检查 .env 文件")
    
    env_path = Path('.env')
    if not env_path.exists():
        print("❌ .env 文件不存在")
        print("\n请创建 .env 文件并添加以下内容：")
        print("""
GEMINI_API_KEY=your_api_key_here
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
        """)
        return False
    
    # 读取 .env 文件
    env_content = env_path.read_text(encoding='utf-8')
    
    has_http_proxy = 'HTTP_PROXY' in env_content
    has_https_proxy = 'HTTPS_PROXY' in env_content
    has_api_key = 'GEMINI_API_KEY' in env_content
    
    print(f"{'✅' if env_path.exists() else '❌'} .env 文件存在")
    print(f"{'✅' if has_api_key else '❌'} GEMINI_API_KEY 已配置")
    print(f"{'✅' if has_http_proxy else '❌'} HTTP_PROXY 已配置")
    print(f"{'✅' if has_https_proxy else '❌'} HTTPS_PROXY 已配置")
    
    if has_http_proxy:
        # 提取代理地址
        for line in env_content.split('\n'):
            if line.startswith('HTTP_PROXY'):
                proxy = line.split('=')[1].strip()
                print(f"\n当前代理配置: {proxy}")
                
                # 提取端口
                if ':' in proxy:
                    port = proxy.split(':')[-1]
                    print(f"代理端口: {port}")
    
    return has_http_proxy and has_https_proxy and has_api_key

def check_proxy_ports():
    """检查常见代理端口"""
    print_header("2. 检查代理端口")
    
    common_ports = [
        (7890, "Clash 默认端口"),
        (7891, "Clash 备用端口"),
        (10809, "V2rayN HTTP 端口"),
        (1080, "Shadowsocks 默认端口"),
        (1087, "Shadowsocks 备用端口"),
    ]
    
    working_ports = []
    
    for port, name in common_ports:
        try:
            # 尝试连接到代理端口
            proxies = {
                'http': f'http://127.0.0.1:{port}',
                'https': f'http://127.0.0.1:{port}'
            }
            
            # 测试连接（超时 2 秒）
            response = requests.get(
                'http://www.google.com',
                proxies=proxies,
                timeout=2
            )
            
            if response.ok:
                print(f"✅ 端口 {port} ({name}) - 工作正常")
                working_ports.append(port)
            else:
                print(f"⚠️  端口 {port} ({name}) - 响应异常")
                
        except requests.exceptions.ProxyError:
            print(f"❌ 端口 {port} ({name}) - 代理未运行")
        except requests.exceptions.Timeout:
            print(f"⏱️  端口 {port} ({name}) - 超时")
        except Exception as e:
            print(f"❌ 端口 {port} ({name}) - {type(e).__name__}")
    
    if working_ports:
        print(f"\n✅ 找到 {len(working_ports)} 个可用的代理端口: {working_ports}")
        print(f"\n建议在 .env 中使用:")
        print(f"HTTP_PROXY=http://127.0.0.1:{working_ports[0]}")
        print(f"HTTPS_PROXY=http://127.0.0.1:{working_ports[0]}")
        return working_ports[0]
    else:
        print("\n❌ 未找到可用的代理端口")
        print("\n请确保：")
        print("1. 代理工具（Clash/V2rayN/Shadowsocks）正在运行")
        print("2. 代理配置正确")
        return None

def test_api_with_proxy():
    """测试 Gemini API 连接"""
    print_header("3. 测试 Gemini API 连接（通过代理）")
    
    # 从环境变量读取代理配置
    from dotenv import load_dotenv
    load_dotenv()
    
    http_proxy = os.getenv('HTTP_PROXY')
    https_proxy = os.getenv('HTTPS_PROXY')
    
    if not http_proxy or not https_proxy:
        print("❌ .env 中未配置代理")
        return False
    
    print(f"使用代理: {http_proxy}")
    
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ 未配置 GEMINI_API_KEY")
            return False
        
        # 配置 Gemini
        genai.configure(api_key=api_key)
        
        # 测试列出模型
        print("正在测试 API 连接...")
        models = genai.list_models()
        model_names = [m.name for m in models]
        
        print(f"✅ API 连接成功！")
        print(f"可用模型数量: {len(model_names)}")
        
        return True
        
    except Exception as e:
        print(f"❌ API 连接失败: {e}")
        
        if 'User location is not supported' in str(e):
            print("\n💡 这是地理位置限制错误")
            print("可能的原因：")
            print("1. 代理未正确配置或未运行")
            print("2. 需要重启服务以应用新的代理配置")
        
        return False

def auto_fix_env():
    """自动修复 .env 配置"""
    print_header("自动修复建议")
    
    # 检查可用端口
    print("正在扫描可用的代理端口...\n")
    
    # 不使用代理测试端口
    common_ports = [7890, 7891, 10809, 1080, 1087]
    
    for port in common_ports:
        try:
            # 简单的 socket 测试
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                print(f"✅ 检测到端口 {port} 正在监听")
                
                print(f"\n建议的 .env 配置：")
                print(f"""
HTTP_PROXY=http://127.0.0.1:{port}
HTTPS_PROXY=http://127.0.0.1:{port}
                """)
                
                # 询问是否自动添加
                print(f"\n是否自动更新 .env 文件？(y/n): ", end='')
                choice = input().lower()
                
                if choice == 'y':
                    update_env_proxy(port)
                    print("\n✅ .env 文件已更新")
                    print("⚠️  请重启后端服务: python main.py")
                
                return
        except:
            pass
    
    print("❌ 未检测到运行中的代理")
    print("\n请先启动代理工具：")
    print("- Clash")
    print("- V2rayN")
    print("- Shadowsocks")

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
        
        # 添加新的代理配置
        lines.append('')
        lines.append('# 代理配置（自动添加）')
        lines.append(f'HTTP_PROXY=http://127.0.0.1:{port}')
        lines.append(f'HTTPS_PROXY=http://127.0.0.1:{port}')
        
        env_path.write_text('\n'.join(lines), encoding='utf-8')

def main():
    """主函数"""
    print("\n🔍 代理配置诊断工具")
    print("="*70)
    
    # 1. 检查 .env 文件
    env_ok = check_env_file()
    
    # 2. 检查代理端口（如果 .env 不完整）
    if not env_ok:
        auto_fix_env()
    
    # 3. 测试 API 连接
    print_header("测试总结")
    
    try:
        # 尝试导入必要的库
        import google.generativeai
        from dotenv import load_dotenv
        
        if env_ok:
            print("✅ .env 配置完整")
            print("\n下一步：")
            print("1. 确保代理工具正在运行")
            print("2. 重启后端服务: python main.py")
            print("3. 运行测试: python test_image_api.py")
        else:
            print("❌ .env 配置不完整")
            print("\n请按照上面的建议配置 .env 文件")
            
    except ImportError as e:
        print(f"⚠️  缺少依赖: {e}")
        print("\n请安装依赖: pip install -r requirements.txt")

if __name__ == "__main__":
    main()

