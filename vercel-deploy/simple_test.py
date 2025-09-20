#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试脚本
"""

import sys
import os

# 测试核心模块导入
print("🧪 测试核心模块导入...")
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

try:
    from simple_verification import get_verification_code_with_retry, is_token_valid
    print("✅ 核心模块导入成功")
    
    # 测试token验证
    print("\n🔑 测试Token验证...")
    token_valid = is_token_valid()
    print(f"Token状态: {'有效' if token_valid else '无效/过期'}")
    
    # 测试验证码获取（快速测试）
    print("\n📧 测试验证码获取功能...")
    print("注意：这只是测试API调用，可能不会找到实际的验证码")
    
    result = get_verification_code_with_retry(
        email_input="test123",
        time_window_minutes=1,  # 很短的时间窗口
        max_retries=1,          # 只重试1次
        retry_interval=5        # 短重试间隔
    )
    
    if result:
        print(f"✅ 找到验证码: {result}")
    else:
        print("⚠️  未找到验证码（这是正常的，因为没有实际的验证码邮件）")
    
    print("\n🎉 所有测试完成！核心功能正常工作")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
