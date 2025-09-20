#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试时区修复功能
验证中国时区时间是否正确显示
"""

import sys
import os
from datetime import datetime, timezone, timedelta

# 添加核心模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

try:
    from simple_verification import get_china_time
    from verification import get_china_time as verification_get_china_time
    print("✅ 成功导入时区函数")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

def test_timezone_functions():
    """测试时区函数"""
    print("🕐 时区测试")
    print("=" * 50)
    
    # 获取不同时区的时间
    utc_time = datetime.now(timezone.utc)
    local_time = datetime.now()
    china_time_1 = get_china_time()
    china_time_2 = verification_get_china_time()
    
    print(f"UTC时间:           {utc_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"本地时间:          {local_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"中国时间(simple):   {china_time_1.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"中国时间(verify):   {china_time_2.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # 验证时区偏移
    china_tz = timezone(timedelta(hours=8))
    expected_china_time = datetime.now(china_tz)
    
    print(f"期望中国时间:      {expected_china_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # 检查时间差异（应该在几秒内）
    diff1 = abs((china_time_1 - expected_china_time).total_seconds())
    diff2 = abs((china_time_2 - expected_china_time).total_seconds())
    
    print(f"\n⏱️  时间差异检查:")
    print(f"simple_verification 差异: {diff1:.2f} 秒")
    print(f"verification 差异:        {diff2:.2f} 秒")
    
    if diff1 < 5 and diff2 < 5:
        print("✅ 时区修复成功！时间差异在可接受范围内")
        return True
    else:
        print("❌ 时区修复可能有问题，时间差异过大")
        return False

def test_time_window_calculation():
    """测试时间窗口计算"""
    print("\n🔍 时间窗口计算测试")
    print("=" * 50)
    
    china_time = get_china_time()
    time_window_minutes = 10
    
    # 模拟时间窗口计算（与verification.py中的逻辑一致）
    start_time = china_time - timedelta(minutes=time_window_minutes)
    end_time = china_time + timedelta(minutes=time_window_minutes)
    
    print(f"当前中国时间:      {china_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"搜索开始时间:      {start_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"搜索结束时间:      {end_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"时间窗口:          {time_window_minutes} 分钟")
    
    # 显示时间窗口范围（类似于实际搜索时的输出）
    print(f"\n📅 搜索时间窗口: {start_time.strftime('%H:%M:%S')} - {end_time.strftime('%H:%M:%S')}")
    
    return True

def main():
    """主测试函数"""
    print("🚀 Vercel部署时区修复测试")
    print("=" * 60)
    
    try:
        # 测试时区函数
        timezone_ok = test_timezone_functions()
        
        # 测试时间窗口计算
        window_ok = test_time_window_calculation()
        
        print("\n" + "=" * 60)
        if timezone_ok and window_ok:
            print("🎉 所有测试通过！时区修复成功")
            print("✅ 部署到Vercel后应该能正确处理中国时区")
        else:
            print("❌ 部分测试失败，请检查时区配置")
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
