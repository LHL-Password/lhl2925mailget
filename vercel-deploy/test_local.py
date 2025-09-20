#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地测试脚本
用于在部署前测试验证码获取功能
"""

import sys
import os
from datetime import datetime

# 添加core目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

try:
    from simple_verification import get_verification_code_with_retry
    print("✅ 成功导入验证码获取模块")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)


def test_verification_code(email_input):
    """测试验证码获取功能"""
    print(f"\n🧪 开始测试验证码获取功能")
    print(f"📧 测试邮箱: {email_input}")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    try:
        # 调用验证码获取函数
        result = get_verification_code_with_retry(
            email_input=email_input,
            sent_time=datetime.now(),
            time_window_minutes=10,
            max_retries=2,  # 减少重试次数以便快速测试
            retry_interval=10  # 减少重试间隔
        )
        
        if result:
            print(f"\n🎉 测试成功！")
            print(f"🔑 获取到验证码: {result}")
            return True
        else:
            print(f"\n⚠️  测试完成，但未找到验证码")
            print(f"💡 这可能是正常的，如果最近没有发送验证码邮件")
            return False
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        return False


def main():
    """主函数"""
    print("🚀 2925邮件验证码服务 - 本地测试")
    print("=" * 50)
    
    # 测试用例
    test_cases = [
        "test123",  # 邮箱前缀
        "example@2925.com",  # 完整邮箱
    ]
    
    print("📋 可用的测试用例:")
    for i, case in enumerate(test_cases, 1):
        print(f"  {i}. {case}")
    
    print("\n💡 你也可以输入自定义的邮箱地址或前缀")
    
    # 获取用户输入
    while True:
        user_input = input("\n请输入邮箱地址或前缀 (或输入数字选择测试用例，q退出): ").strip()
        
        if user_input.lower() == 'q':
            print("👋 退出测试")
            break
        
        # 检查是否是数字选择
        if user_input.isdigit():
            choice = int(user_input)
            if 1 <= choice <= len(test_cases):
                email_input = test_cases[choice - 1]
            else:
                print("❌ 无效的选择，请重新输入")
                continue
        else:
            email_input = user_input
        
        if not email_input:
            print("❌ 邮箱地址不能为空，请重新输入")
            continue
        
        # 执行测试
        success = test_verification_code(email_input)
        
        # 询问是否继续测试
        continue_test = input("\n是否继续测试其他邮箱? (y/n): ").strip().lower()
        if continue_test != 'y':
            break
    
    print("\n✅ 测试完成")
    print("💡 如果本地测试正常，可以继续部署到Vercel")


if __name__ == "__main__":
    main()
