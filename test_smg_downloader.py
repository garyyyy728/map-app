"""
SMG 圖片下載器測試腳本
測試核心功能而不進行完整循環
"""
import sys
import os

# 添加父目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from smg_image_downloader import (
    ensure_directories,
    get_image_url,
    download_image,
    analyze_flood_with_model,
    load_model,
    save_analysis_result,
    LOCATION_NAMES,
    CAMERA_GROUPS
)

def test_directories():
    """測試目錄創建"""
    print("\n=== 測試 1: 目錄創建 ===")
    ensure_directories()
    print("✓ 目錄創建成功")


def test_get_image_url():
    """測試獲取圖片 URL"""
    print("\n=== 測試 2: 獲取圖片 URL ===")
    # 測試第一個地點
    test_group = CAMERA_GROUPS[0]
    print(f"測試地點: {test_group} ({LOCATION_NAMES.get(test_group, test_group)})")
    
    url = get_image_url(test_group)
    if url:
        print(f"✓ 成功獲取 URL: {url[:80]}...")
        return url
    else:
        print("✗ 獲取 URL 失敗")
        return None


def test_download(url):
    """測試圖片下載"""
    print("\n=== 測試 3: 下載圖片 ===")
    if not url:
        print("跳過下載測試（無有效 URL）")
        return None
    
    test_group = CAMERA_GROUPS[0]
    filepath = download_image(test_group, url)
    
    if filepath and os.path.exists(filepath):
        file_size = os.path.getsize(filepath)
        print(f"✓ 下載成功: {filepath}")
        print(f"  文件大小: {file_size / 1024:.2f} KB")
        return filepath
    else:
        print("✗ 下載失敗")
        return None


def test_analyze(image_path):
    """測試 HuggingFace 模型分析"""
    print("\n=== 測試 4: HuggingFace 水浸檢測 ===")
    if not image_path or not os.path.exists(image_path):
        print("跳過分析測試（無有效圖片）")
        return None
    
    # 先載入模型
    print("正在載入模型...")
    model, processor = load_model()
    if model is None or processor is None:
        print("✗ 模型載入失敗")
        return None
    
    result = analyze_flood_with_model(image_path)
    
    if result and result.get('success'):
        print(f"✓ 分析成功")
        print(f"  檢測結果: {result.get('predicted_label', 'N/A')}")
        print(f"  置信度: {result.get('confidence', 0):.2%}")
        return result
    else:
        print(f"✗ 分析失敗: {result.get('error', 'Unknown error') if result else 'No result'}")
        return result


def test_save_result(result):
    """測試保存分析結果"""
    print("\n=== 測試 5: 保存分析結果 ===")
    if not result:
        print("跳過保存測試（無分析結果）")
        return
    
    test_group = CAMERA_GROUPS[0]
    save_analysis_result(test_group, result)
    print("✓ 結果保存完成")


def main():
    """運行所有測試"""
    print("=" * 80)
    print("SMG 圖片下載器 - 功能測試")
    print("=" * 80)
    print("\n此測試將執行以下步驟：")
    print("1. 創建必要的目錄")
    print("2. 獲取一個測試地點的圖片 URL")
    print("3. 下載測試圖片")
    print("4. 使用 HuggingFace 模型分析水浸情況")
    print("5. 保存分析結果")
    print("\n注意: 此測試會下載圖片並載入 AI 模型")
    print("=" * 80)
    
    try:
        # 測試 1: 目錄創建
        test_directories()
        
        # 測試 2: 獲取 URL
        url = test_get_image_url()
        
        # 測試 3: 下載圖片
        image_path = test_download(url)
        
        # 測試 4: Gemini 分析
        result = test_analyze(image_path)
        
        # 測試 5: 保存結果
        test_save_result(result)
        
        # 總結
        print("\n" + "=" * 80)
        print("測試完成！")
        print("=" * 80)
        print("\n檢查結果：")
        print(f"- 圖片保存目錄: smg_images/")
        print(f"- 分析結果目錄: smg_analysis_results/")
        
        if image_path and os.path.exists(image_path):
            print(f"\n已下載圖片: {image_path}")
        
        if result:
            print(f"分析狀態: {'成功' if result.get('success') else '失敗'}")
            if result.get('success'):
                print(f"\n完整分析結果:")
                print("-" * 80)
                print(result.get('analysis', 'N/A'))
                print("-" * 80)
        
        print("\n如果所有測試通過，您可以運行主程序：")
        print("  python smg_image_downloader.py")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\n測試被用戶中斷")
    except Exception as e:
        print(f"\n\n測試過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
