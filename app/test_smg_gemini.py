"""
测试 SMG API 和 Gemini API 连接
"""
import requests
import base64
import os

print("=" * 60)
print("测试 1: SMG API 连接")
print("=" * 60)

# 测试获取一个地点的图片 URL
test_group = "LMF"
api_url = f"https://cms.smg.gov.mo/zh_TW/api/imageseries/ftgmsCamera{test_group}"

try:
    print(f"\n正在请求: {api_url}")
    response = requests.get(api_url, timeout=10)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"返回数据类型: {type(data)}")
        
        if isinstance(data, list) and len(data) > 0:
            print(f"图片数量: {len(data)}")
            latest = data[0]
            print(f"最新图片信息: {latest}")
            
            if "path" in latest:
                image_path = latest["path"]
                full_url = f"https://cms.smg.gov.mo{image_path}"
                print(f"\n✅ SMG API 测试成功!")
                print(f"图片 URL: {full_url}")
                
                # 测试下载图片
                print(f"\n正在下载测试图片...")
                img_response = requests.get(full_url, timeout=15)
                if img_response.status_code == 200:
                    test_image_path = "/tmp/test_smg_image.jpg"
                    with open(test_image_path, "wb") as f:
                        f.write(img_response.content)
                    print(f"✅ 图片下载成功: {test_image_path}")
                    print(f"图片大小: {len(img_response.content) / 1024:.1f} KB")
                    
                    # 测试 Gemini API
                    print("\n" + "=" * 60)
                    print("测试 2: Gemini API 连接")
                    print("=" * 60)
                    
                    api_key = "AIzaSyBUU2MYPMqc9NHanRp68tRCJsUb5wWA1wU"
                    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
                    
                    # 读取图片并转换为 base64
                    with open(test_image_path, "rb") as f:
                        image_data = base64.b64encode(f.read()).decode('utf-8')
                    
                    payload = {
                        "contents": [{
                            "parts": [
                                {"text": "分析這張圖片裡面的水浸情況如何"},
                                {
                                    "inline_data": {
                                        "mime_type": "image/jpeg",
                                        "data": image_data
                                    }
                                }
                            ]
                        }]
                    }
                    
                    print(f"\n正在调用 Gemini API...")
                    gemini_response = requests.post(
                        gemini_url,
                        json=payload,
                        headers={"Content-Type": "application/json"},
                        timeout=60
                    )
                    
                    print(f"状态码: {gemini_response.status_code}")
                    
                    if gemini_response.status_code == 200:
                        result = gemini_response.json()
                        
                        if "candidates" in result:
                            text = result["candidates"][0]["content"]["parts"][0]["text"]
                            print(f"\n✅ Gemini API 测试成功!")
                            print(f"\n分析结果:")
                            print("-" * 60)
                            print(text)
                            print("-" * 60)
                        else:
                            print(f"❌ 响应格式异常: {result}")
                    else:
                        print(f"❌ Gemini API 请求失败")
                        print(f"错误: {gemini_response.text}")
                    
                    # 清理测试文件
                    if os.path.exists(test_image_path):
                        os.remove(test_image_path)
                        print(f"\n已清理测试文件")
                        
                else:
                    print(f"❌ 图片下载失败: {img_response.status_code}")
            else:
                print(f"❌ 数据中没有 'path' 字段")
        else:
            print(f"❌ 返回数据格式异常")
    else:
        print(f"❌ 请求失败")
        
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
