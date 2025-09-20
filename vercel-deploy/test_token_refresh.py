#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token自动刷新功能测试脚本
"""

import sys
import os
from datetime import datetime

# 添加core目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

try:
    from simple_verification import (
        is_token_valid, auto_refresh_token_if_needed, 
        get_mail_list, CURRENT_TOKEN
    )
    print("✅ 成功导入验证码获取模块")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)


def test_token_validation():
    """测试token验证功能"""
    print("\n🧪 测试Token验证功能")
    print("-" * 40)
    
    print(f"📄 当前Token: {CURRENT_TOKEN[:50]}...")
    
    # 测试token验证
    is_valid = is_token_valid()
    if is_valid:
        print("✅ Token验证通过")
    else:
        print("❌ Token验证失败")
    
    return is_valid


def test_auto_refresh():
    """测试自动token刷新功能"""
    print("\n🧪 测试自动Token刷新功能")
    print("-" * 40)
    
    # 尝试自动刷新token
    success = auto_refresh_token_if_needed()
    
    if success:
        print("✅ Token刷新测试通过")
    else:
        print("❌ Token刷新测试失败")
    
    return success


def test_mail_list_with_auto_refresh():
    """测试带自动刷新的邮件列表获取"""
    print("\n🧪 测试邮件列表获取（含自动刷新）")
    print("-" * 40)
    
    try:
        # 获取邮件列表（会自动处理token过期）
        result = get_mail_list(page_count=10)
        
        if result and result.get('code') == 200:
            mail_count = len(result.get('result', {}).get('list', []))
            print(f"✅ 成功获取邮件列表，共 {mail_count} 封邮件")
            return True
        else:
            print(f"❌ 获取邮件列表失败: {result.get('message', '未知错误') if result else '无响应'}")
            return False
            
    except Exception as e:
        print(f"❌ 邮件列表获取异常: {e}")
        return False


def test_expired_token_scenario():
    """模拟token过期场景测试"""
    print("\n🧪 模拟Token过期场景测试")
    print("-" * 40)
    
    # 备份原始token
    import simple_verification
    original_token = simple_verification.CURRENT_TOKEN
    
    try:
        # 设置一个过期的token进行测试
        expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDAwMDAwMDB9.invalid"
        simple_verification.CURRENT_TOKEN = expired_token
        simple_verification.DEFAULT_HEADERS['Authorization'] = f'Bearer {expired_token}'
        
        print("🔄 设置过期Token，测试自动刷新...")
        
        # 尝试获取邮件列表，应该会触发自动刷新
        result = get_mail_list(page_count=5)
        
        if result and result.get('code') == 200:
            print("✅ 过期Token自动刷新测试成功")
            return True
        else:
            print("❌ 过期Token自动刷新测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 过期Token测试异常: {e}")
        return False
    finally:
        # 恢复原始token
        simple_verification.CURRENT_TOKEN = original_token
        simple_verification.DEFAULT_HEADERS['Authorization'] = f'Bearer {original_token}'


def main():
    """主函数"""
    print("🚀 Token自动刷新功能测试")
    print("=" * 50)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_results = []
    
    # 测试1: Token验证
    test_results.append(("Token验证", test_token_validation()))
    
    # 测试2: 自动刷新
    test_results.append(("自动Token刷新", test_auto_refresh()))
    
    # 测试3: 邮件列表获取
    test_results.append(("邮件列表获取", test_mail_list_with_auto_refresh()))
    
    # 测试4: 过期Token场景
    test_results.append(("过期Token自动刷新", test_expired_token_scenario()))
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    print("-" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print("-" * 50)
    print(f"总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！Token自动刷新功能正常工作")
    else:
        print("⚠️  部分测试失败，请检查配置和网络连接")
    
    print("\n💡 提示：如果测试失败，请检查：")
    print("   1. 网络连接是否正常")
    print("   2. 登录信息是否正确")
    print("   3. 2925.com服务是否可用")


if __name__ == "__main__":
    main()
