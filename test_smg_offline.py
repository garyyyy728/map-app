"""
離線測試 SMG 街道圖片下載器 + HuggingFace 水浸檢測
使用模擬數據測試所有核心功能，無需外部 API 連接
"""
import sys
import os
import io
from datetime import datetime
from PIL import Image

# 添加父目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from smg_image_downloader import (
    ensure_directories,
    analyze_flood_with_model,
    load_model,
    save_analysis_result,
    LOCATION_NAMES,
    CAMERA_GROUPS,
    SAVE_DIR,
    ANALYSIS_SAVE_DIR
)


def create_test_image(width=640, height=480, color='blue'):
    """創建測試用圖片"""
    img = Image.new('RGB', (width, height), color=color)
    # 添加一些變化使圖片更真實
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.rectangle([100, 100, 300, 300], fill='gray')
    draw.ellipse([350, 200, 500, 350], fill='darkblue')
    return img


def test_directories():
    """測試 1: 目錄創建"""
    print("\n=== 測試 1: 目錄創建 ===")
    try:
        ensure_directories()
        
        # 驗證目錄存在
        assert os.path.exists(SAVE_DIR), f"圖片目錄不存在: {SAVE_DIR}"
        assert os.path.exists(ANALYSIS_SAVE_DIR), f"分析結果目錄不存在: {ANALYSIS_SAVE_DIR}"
        
        print(f"✓ 圖片目錄已創建: {SAVE_DIR}")
        print(f"✓ 分析結果目錄已創建: {ANALYSIS_SAVE_DIR}")
        print("✓ 目錄創建測試通過")
        return True
    except Exception as e:
        print(f"✗ 目錄創建測試失敗: {str(e)}")
        return False


def test_model_loading():
    """測試 2: HuggingFace 模型載入"""
    print("\n=== 測試 2: HuggingFace 模型載入 ===")
    try:
        print("正在嘗試載入 HuggingFace 水浸檢測模型...")
        model, processor = load_model()
        
        if model is None or processor is None:
            print("✗ 模型載入失敗")
            print("注意: 模型載入失敗可能是由於:")
            print("  1. 網絡連接問題（首次需要下載模型）")
            print("  2. 磁盤空間不足")
            print("  3. 依賴庫版本不兼容")
            return False
        
        print(f"✓ 模型載入成功")
        print(f"✓ 模型類型: {type(model).__name__}")
        print(f"✓ 處理器類型: {type(processor).__name__}")
        
        # 驗證模型配置
        if hasattr(model, 'config') and hasattr(model.config, 'id2label'):
            labels = model.config.id2label
            print(f"✓ 模型支持 {len(labels)} 個分類標籤:")
            for label_id, label_name in labels.items():
                print(f"    - {label_id}: {label_name}")
        
        print("✓ 模型載入測試通過")
        return True
        
    except Exception as e:
        print(f"✗ 模型載入測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_image_creation():
    """測試 3: 測試圖片創建"""
    print("\n=== 測試 3: 測試圖片創建 ===")
    try:
        # 創建測試圖片
        test_img = create_test_image()
        
        # 保存測試圖片
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_filename = f"TEST_{timestamp}.jpg"
        test_filepath = os.path.join(SAVE_DIR, test_filename)
        
        test_img.save(test_filepath)
        
        # 驗證圖片已保存
        assert os.path.exists(test_filepath), "測試圖片未成功保存"
        file_size = os.path.getsize(test_filepath)
        
        print(f"✓ 測試圖片已創建: {test_filepath}")
        print(f"✓ 圖片大小: {file_size / 1024:.2f} KB")
        print(f"✓ 圖片尺寸: {test_img.size}")
        print("✓ 圖片創建測試通過")
        
        return test_filepath
        
    except Exception as e:
        print(f"✗ 圖片創建測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def test_flood_analysis(image_path):
    """測試 4: 水浸檢測分析"""
    print("\n=== 測試 4: HuggingFace 水浸檢測分析 ===")
    
    if not image_path or not os.path.exists(image_path):
        print("✗ 跳過分析測試（無有效測試圖片）")
        return None
    
    try:
        print(f"正在分析測試圖片: {image_path}")
        
        # 執行水浸檢測
        result = analyze_flood_with_model(image_path)
        
        if not result:
            print("✗ 分析結果為空")
            return None
        
        if not result.get('success'):
            print(f"✗ 分析失敗: {result.get('error', 'Unknown error')}")
            return result
        
        # 驗證結果包含必要的字段
        required_fields = ['predicted_label', 'confidence', 'is_flooded', 'flood_status', 'analysis']
        for field in required_fields:
            assert field in result, f"分析結果缺少必要字段: {field}"
        
        print("✓ 分析成功完成")
        print(f"✓ 水浸狀態: {result['flood_status']}")
        print(f"✓ 檢測類別: {result['predicted_label']}")
        print(f"✓ 置信度: {result['confidence']:.2%}")
        print(f"✓ 是否有水浸: {'是' if result['is_flooded'] else '否'}")
        
        # 顯示完整分析文本的一部分
        analysis_text = result.get('analysis', '')
        if analysis_text:
            print("\n分析結果摘要:")
            print("-" * 60)
            lines = analysis_text.split('\n')[:10]  # 只顯示前10行
            for line in lines:
                print(line)
            if len(analysis_text.split('\n')) > 10:
                print("... (更多內容)")
            print("-" * 60)
        
        print("✓ 水浸檢測測試通過")
        return result
        
    except Exception as e:
        print(f"✗ 水浸檢測測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def test_save_analysis(result):
    """測試 5: 保存分析結果"""
    print("\n=== 測試 5: 保存分析結果 ===")
    
    if not result:
        print("✗ 跳過保存測試（無分析結果）")
        return False
    
    try:
        # 使用測試地點代號
        test_location = "TEST"
        
        # 保存分析結果
        save_analysis_result(test_location, result)
        
        # 驗證文件已保存
        # 列出分析結果目錄中的文件
        files = os.listdir(ANALYSIS_SAVE_DIR)
        test_files = [f for f in files if f.startswith("TEST_")]
        
        assert len(test_files) > 0, "未找到保存的分析結果文件"
        
        # 讀取並驗證最新的測試文件
        latest_file = sorted(test_files)[-1]
        filepath = os.path.join(ANALYSIS_SAVE_DIR, latest_file)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 驗證內容包含關鍵信息
        assert "地點:" in content, "分析結果缺少地點信息"
        assert "時間:" in content, "分析結果缺少時間信息"
        assert "分析狀態:" in content, "分析結果缺少狀態信息"
        
        if result.get('success'):
            assert "水浸狀態" in content, "分析結果缺少水浸狀態"
        
        print(f"✓ 分析結果已保存: {filepath}")
        print(f"✓ 文件大小: {len(content)} 字節")
        print("\n文件內容預覽:")
        print("-" * 60)
        print(content[:500] + "..." if len(content) > 500 else content)
        print("-" * 60)
        print("✓ 保存分析結果測試通過")
        
        return True
        
    except Exception as e:
        print(f"✗ 保存分析結果測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_location_mapping():
    """測試 6: 地點名稱映射"""
    print("\n=== 測試 6: 地點名稱映射 ===")
    try:
        print(f"✓ 總共配置了 {len(CAMERA_GROUPS)} 個監控地點")
        print(f"✓ 總共配置了 {len(LOCATION_NAMES)} 個地點名稱")
        
        # 驗證所有地點代號都有對應的中文名稱
        missing_names = []
        for group in CAMERA_GROUPS:
            if group not in LOCATION_NAMES:
                missing_names.append(group)
        
        if missing_names:
            print(f"⚠️  以下地點代號缺少中文名稱: {', '.join(missing_names)}")
        else:
            print("✓ 所有地點代號都有對應的中文名稱")
        
        # 顯示所有地點
        print("\n配置的監控地點:")
        for i, group in enumerate(CAMERA_GROUPS, 1):
            name = LOCATION_NAMES.get(group, "未命名")
            print(f"  {i:2d}. {group} - {name}")
        
        print("✓ 地點名稱映射測試通過")
        return True
        
    except Exception as e:
        print(f"✗ 地點名稱映射測試失敗: {str(e)}")
        return False


def run_all_tests():
    """運行所有測試"""
    print("=" * 80)
    print("SMG 街道圖片下載器 + HuggingFace 水浸檢測 - 離線功能測試")
    print("=" * 80)
    print("\n本測試套件將驗證以下功能：")
    print("1. 目錄創建和管理")
    print("2. HuggingFace 模型載入")
    print("3. 圖片創建和處理")
    print("4. 水浸檢測分析")
    print("5. 分析結果保存")
    print("6. 地點配置驗證")
    print("\n注意: 此為離線測試，使用模擬數據替代實際 API")
    print("=" * 80)
    
    results = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'skipped': 0
    }
    
    # 測試 1: 目錄創建
    results['total'] += 1
    if test_directories():
        results['passed'] += 1
    else:
        results['failed'] += 1
        print("\n⚠️  目錄創建失敗，無法繼續後續測試")
        return results
    
    # 測試 2: 模型載入
    results['total'] += 1
    model_loaded = test_model_loading()
    if model_loaded:
        results['passed'] += 1
    else:
        results['failed'] += 1
        print("\n⚠️  模型載入失敗，將跳過依賴模型的測試")
    
    # 測試 3: 圖片創建
    results['total'] += 1
    test_image_path = test_image_creation()
    if test_image_path:
        results['passed'] += 1
    else:
        results['failed'] += 1
        print("\n⚠️  圖片創建失敗，將跳過後續測試")
        model_loaded = False
    
    # 測試 4: 水浸檢測（僅在模型載入成功時執行）
    results['total'] += 1
    if model_loaded and test_image_path:
        analysis_result = test_flood_analysis(test_image_path)
        if analysis_result and analysis_result.get('success'):
            results['passed'] += 1
        else:
            results['failed'] += 1
    else:
        print("\n=== 測試 4: HuggingFace 水浸檢測分析 ===")
        print("✗ 跳過此測試（模型未載入或圖片創建失敗）")
        results['skipped'] += 1
        analysis_result = None
    
    # 測試 5: 保存結果
    results['total'] += 1
    if analysis_result and analysis_result.get('success'):
        if test_save_analysis(analysis_result):
            results['passed'] += 1
        else:
            results['failed'] += 1
    else:
        print("\n=== 測試 5: 保存分析結果 ===")
        print("✗ 跳過此測試（無有效分析結果）")
        results['skipped'] += 1
    
    # 測試 6: 地點映射（不依賴其他測試）
    results['total'] += 1
    if test_location_mapping():
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # 總結
    print("\n" + "=" * 80)
    print("測試總結")
    print("=" * 80)
    print(f"總測試數: {results['total']}")
    print(f"✓ 通過: {results['passed']}")
    print(f"✗ 失敗: {results['failed']}")
    print(f"- 跳過: {results['skipped']}")
    print(f"成功率: {results['passed'] / results['total'] * 100:.1f}%")
    print("=" * 80)
    
    # 給出建議
    print("\n建議:")
    if results['failed'] > 0:
        print("⚠️  有測試失敗，請檢查:")
        print("  1. 依賴庫是否正確安裝 (pip install -r requirements.txt)")
        print("  2. 是否有足夠的磁盤空間（模型需要約 2GB）")
        print("  3. 網絡連接是否正常（首次運行需要下載模型）")
    else:
        print("✓ 所有測試通過！")
        print("  您可以運行主程序進行實際監控:")
        print("    python smg_image_downloader.py")
    
    print("\n查看測試產生的文件:")
    print(f"  - 測試圖片: {SAVE_DIR}/")
    print(f"  - 分析結果: {ANALYSIS_SAVE_DIR}/")
    print("=" * 80)
    
    return results


if __name__ == "__main__":
    try:
        results = run_all_tests()
        # 如果有失敗的測試，返回非零退出碼
        exit_code = 0 if results['failed'] == 0 else 1
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n測試被用戶中斷")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n測試運行時發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
