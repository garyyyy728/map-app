"""
SMG 水浸監控系統 - 使用範例
展示如何使用監控系統的各種功能
"""

# ============================================================
# 範例 1: 基本使用 - 簡化版
# ============================================================
def example_1_basic_usage():
    """最簡單的使用方式 - 運行一次完整監控"""
    print("\n" + "=" * 60)
    print("範例 1: 基本使用")
    print("=" * 60)
    
    from smg_flood_monitor_simple import process_all_cameras, ensure_directories
    
    # 確保目錄存在
    ensure_directories()
    
    # 處理所有攝像頭
    success_count = process_all_cameras()
    
    print(f"\n✅ 完成！成功處理 {success_count} 個地點")


# ============================================================
# 範例 2: 自定義監控特定地點
# ============================================================
def example_2_specific_locations():
    """只監控特定的幾個地點"""
    print("\n" + "=" * 60)
    print("範例 2: 監控特定地點")
    print("=" * 60)
    
    from smg_flood_monitor_simple import (
        get_image_url, download_image, analyze_flood_with_gemini,
        save_analysis_result, LOCATION_NAMES
    )
    
    # 只監控這三個地點
    target_locations = ["LMF", "LPI", "LHK"]
    
    for group_code in target_locations:
        location_name = LOCATION_NAMES.get(group_code, group_code)
        print(f"\n處理: {location_name} ({group_code})")
        
        # 獲取並下載圖片
        url = get_image_url(group_code)
        if url:
            image_path = download_image(group_code, url)
            if image_path:
                # 分析水浸情況
                analysis = analyze_flood_with_gemini(image_path)
                if analysis:
                    save_analysis_result(group_code, image_path, analysis)
                    print(f"✅ {location_name} 處理完成")


# ============================================================
# 範例 3: 單次下載和分析
# ============================================================
def example_3_single_location():
    """下載並分析單個地點的圖片"""
    print("\n" + "=" * 60)
    print("範例 3: 單個地點分析")
    print("=" * 60)
    
    from smg_flood_monitor_simple import (
        get_image_url, download_image, analyze_flood_with_gemini
    )
    
    # 分析花地瑪的實時圖片
    group_code = "LMF"
    
    print(f"\n正在分析 {group_code} 的實時圖片...")
    
    # 1. 獲取圖片 URL
    url = get_image_url(group_code)
    if not url:
        print("❌ 無法獲取圖片 URL")
        return
    
    # 2. 下載圖片
    image_path = download_image(group_code, url)
    if not image_path:
        print("❌ 圖片下載失敗")
        return
    
    # 3. 分析水浸情況
    analysis = analyze_flood_with_gemini(image_path)
    if analysis:
        print("\n分析結果:")
        print("-" * 60)
        print(analysis)
        print("-" * 60)
    else:
        print("❌ 分析失敗")


# ============================================================
# 範例 4: 自定義分析提示詞
# ============================================================
def example_4_custom_prompt():
    """使用自定義提示詞分析圖片"""
    print("\n" + "=" * 60)
    print("範例 4: 自定義分析提示詞")
    print("=" * 60)
    
    import requests
    import base64
    from smg_flood_monitor_simple import get_image_url, download_image
    
    # 自定義提示詞
    custom_prompts = [
        "這個地點現在的交通狀況如何？",
        "圖片中是否有積水或水浸跡象？",
        "描述當前的天氣狀況",
        "這個區域看起來安全嗎？"
    ]
    
    group_code = "LTA"  # 永樂戲院
    
    # 下載圖片
    url = get_image_url(group_code)
    if not url:
        print("❌ 無法獲取圖片 URL")
        return
    
    image_path = download_image(group_code, url)
    if not image_path:
        print("❌ 圖片下載失敗")
        return
    
    # 對同一張圖片使用不同提示詞分析
    api_key = "AIzaSyBUU2MYPMqc9NHanRp68tRCJsUb5wWA1wU"
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
    
    # 讀取圖片
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    for i, prompt in enumerate(custom_prompts, 1):
        print(f"\n[{i}] 提示詞: {prompt}")
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_data
                        }
                    }
                ]
            }]
        }
        
        try:
            response = requests.post(
                gemini_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                print(f"回答: {text}")
            else:
                print(f"❌ 請求失敗: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 錯誤: {e}")
        
        # 避免請求過快
        import time
        time.sleep(2)


# ============================================================
# 範例 5: 批量下載圖片（不分析）
# ============================================================
def example_5_download_only():
    """只下載圖片，不進行 AI 分析"""
    print("\n" + "=" * 60)
    print("範例 5: 批量下載圖片")
    print("=" * 60)
    
    from smg_flood_monitor_simple import (
        CAMERA_GROUPS, get_image_url, download_image, LOCATION_NAMES
    )
    
    downloaded = []
    
    for group_code in CAMERA_GROUPS:
        location_name = LOCATION_NAMES.get(group_code, group_code)
        
        url = get_image_url(group_code)
        if url:
            image_path = download_image(group_code, url)
            if image_path:
                downloaded.append((group_code, location_name, image_path))
        
        # 短暫延迟
        import time
        time.sleep(1)
    
    print(f"\n✅ 下載完成: {len(downloaded)}/{len(CAMERA_GROUPS)} 張圖片")
    
    for code, name, path in downloaded:
        print(f"  - {name} ({code}): {path}")


# ============================================================
# 範例 6: 定時監控（自定義間隔）
# ============================================================
def example_6_scheduled_monitoring():
    """每隔指定時間運行一次監控"""
    print("\n" + "=" * 60)
    print("範例 6: 定時監控")
    print("=" * 60)
    
    from smg_flood_monitor_simple import process_all_cameras
    from datetime import datetime
    import time
    
    interval_minutes = 5  # 5 分鐘間隔
    max_runs = 3  # 最多運行 3 次（示例）
    
    print(f"監控間隔: {interval_minutes} 分鐘")
    print(f"最多運行: {max_runs} 次")
    print("\n按 Ctrl+C 提前停止\n")
    
    for run in range(max_runs):
        print(f"\n第 {run + 1}/{max_runs} 次監控")
        print("-" * 60)
        
        process_all_cameras()
        
        if run < max_runs - 1:  # 不是最後一次
            next_run = datetime.now().timestamp() + (interval_minutes * 60)
            next_time = datetime.fromtimestamp(next_run).strftime('%H:%M:%S')
            print(f"\n⏰ 等待下一次監控... (下次運行: {next_time})")
            time.sleep(interval_minutes * 60)
    
    print("\n✅ 監控任務完成")


# ============================================================
# 範例 7: 使用 FastAPI 服務
# ============================================================
def example_7_use_fastapi_service():
    """通過 FastAPI 端點分析圖片"""
    print("\n" + "=" * 60)
    print("範例 7: 使用 FastAPI 服務")
    print("=" * 60)
    
    import requests
    from smg_flood_monitor_simple import get_image_url, download_image
    
    # 注意: 需要先啟動 FastAPI 服務
    # python main.py
    
    api_url = "http://localhost:8000/api/gemini/analyze-image"
    
    # 下載一張圖片
    group_code = "LMF"
    url = get_image_url(group_code)
    if not url:
        print("❌ 無法獲取圖片 URL")
        return
    
    image_path = download_image(group_code, url)
    if not image_path:
        print("❌ 圖片下載失敗")
        return
    
    # 使用 FastAPI 端點分析
    print("\n正在通過 API 分析圖片...")
    
    try:
        with open(image_path, "rb") as f:
            files = {"image": f}
            data = {"prompt": "分析這張圖片裡面的水浸情況如何"}
            
            response = requests.post(api_url, files=files, data=data, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print("\n分析結果:")
                    print("-" * 60)
                    print(result["analysis"])
                    print("-" * 60)
                else:
                    print(f"❌ 分析失敗: {result.get('message')}")
            else:
                print(f"❌ API 請求失敗: {response.status_code}")
                
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到 API 服務")
        print("請確保 FastAPI 服務已啟動: python main.py")
    except Exception as e:
        print(f"❌ 錯誤: {e}")


# ============================================================
# 主函數 - 運行所有範例
# ============================================================
def main():
    """運行示例菜單"""
    print("\n" + "=" * 60)
    print("  SMG 水浸監控系統 - 使用範例")
    print("=" * 60)
    
    examples = [
        ("基本使用 - 運行一次完整監控", example_1_basic_usage),
        ("監控特定地點", example_2_specific_locations),
        ("單個地點分析", example_3_single_location),
        ("自定義分析提示詞", example_4_custom_prompt),
        ("批量下載圖片（不分析）", example_5_download_only),
        ("定時監控", example_6_scheduled_monitoring),
        ("使用 FastAPI 服務", example_7_use_fastapi_service),
    ]
    
    print("\n請選擇要運行的範例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print("  0. 退出")
    
    try:
        choice = int(input("\n請輸入選項 (0-7): "))
        
        if choice == 0:
            print("再見！")
            return
        
        if 1 <= choice <= len(examples):
            _, func = examples[choice - 1]
            func()
        else:
            print("無效的選項")
            
    except ValueError:
        print("請輸入有效的數字")
    except KeyboardInterrupt:
        print("\n\n中斷運行")
    except Exception as e:
        print(f"\n錯誤: {e}")


if __name__ == "__main__":
    main()
