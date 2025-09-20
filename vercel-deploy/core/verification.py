#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证码提取模块
从邮件内容中提取验证码
"""

import re
import time
from datetime import datetime, timedelta, timezone

# 中国时区
CHINA_TZ = timezone(timedelta(hours=8))

def get_china_time():
    """获取中国时区的当前时间"""
    return datetime.now(CHINA_TZ)

# 尝试相对导入，如果失败则使用绝对导入
try:
    from .mail_api import (
        get_mail_list, read_mail_content, extract_email_prefix, is_verification_email
    )
except ImportError:
    from mail_api import (
        get_mail_list, read_mail_content, extract_email_prefix, is_verification_email
    )


def extract_verification_code(text):
    """
    从文本中提取验证码
    
    Args:
        text (str): 邮件文本内容
        
    Returns:
        str: 验证码，如果未找到则返回None
    """
    # 多种验证码模式匹配（按优先级排序）
    patterns = [
        r'Your verification code is:\s*<b>(\d{6})</b>',  # Your verification code is: <b>123456</b>
        r'Your verification code is:\s*(\d{6})',  # Your verification code is: 123456
        r'verification code is:\s*<b>(\d{6})</b>',  # verification code is: <b>123456</b>
        r'verification code is:\s*(\d{6})',  # verification code is: 123456
        r'验证码[：:]\s*(\d{6})',  # 验证码：123456
        r'验证码为[：:]\s*(\d{6})',  # 验证码为：123456
        r'code[：:]\s*(\d{6})',  # code: 123456
        r'security code[：:]\s*(\d{6})',  # security code: 123456
        r'OTP[：:]\s*(\d{6})',  # OTP: 123456
    ]

    # 首先尝试精确匹配
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            code = match.group(1)
            # 验证码通常是6位数字，且不应该是年份等
            if len(code) == 6 and not code.startswith('20'):  # 排除年份
                return code

    # 如果没有找到精确匹配，且确认是验证码邮件，再尝试宽松匹配
    if 'verification' in text.lower() or 'verify' in text.lower() or '验证' in text:
        # 查找6位数字，但要更严格
        matches = re.findall(r'\b(\d{6})\b', text)
        for code in matches:
            # 排除明显不是验证码的数字
            if not code.startswith('20') and code != '000000' and code != '123456':
                return code

    return None


def find_verification_mail_by_alias(email_prefix, sent_time=None, time_window_minutes=10, max_retries=5, retry_interval=30):
    """
    根据邮箱前缀查找验证码邮件
    
    Args:
        email_prefix (str): 邮箱前缀
        sent_time (datetime): 发送验证码的时间
        time_window_minutes (int): 时间窗口（分钟）
        max_retries (int): 最大重试次数
        retry_interval (int): 重试间隔（秒）
        
    Returns:
        dict: 包含验证码和邮件信息的字典，如果未找到则返回None
    """
    if sent_time is None:
        sent_time = get_china_time()
    
    # 计算时间窗口
    start_time = sent_time - timedelta(minutes=time_window_minutes)
    end_time = sent_time + timedelta(minutes=time_window_minutes)
    
    print(f"🔍 正在搜索邮箱前缀 '{email_prefix}' 的验证码邮件...")
    print(f"⏰ 时间窗口: {start_time.strftime('%H:%M:%S')} - {end_time.strftime('%H:%M:%S')}")
    
    for attempt in range(max_retries):
        print(f"\n📡 第 {attempt + 1}/{max_retries} 次尝试...")
        
        # 获取邮件列表
        mail_list_data = get_mail_list()
        if not mail_list_data or mail_list_data.get('code') != 200:
            print("❌ 无法获取邮件列表")
            if attempt < max_retries - 1:
                print(f"⏳ 等待 {retry_interval} 秒后重试...")
                time.sleep(retry_interval)
            continue

        mail_list = mail_list_data.get('result', {}).get('list', [])
        print(f"📧 获取到 {len(mail_list)} 封邮件")

        # 按时间排序（最新的在前）
        mail_list.sort(key=lambda x: int(x.get('createTime', '0')), reverse=True)
        
        for i, mail in enumerate(mail_list, 1):
            message_id = mail.get('messageId')
            subject = mail.get('subject', '无主题')
            sender = mail.get('sender', {}).get('senderDisplay', '未知发件人')
            create_time = mail.get('createTime', '0')
            
            # 转换时间戳为datetime对象
            try:
                mail_time = datetime.fromtimestamp(int(create_time) / 1000)
                readable_time = mail_time.strftime('%Y-%m-%d %H:%M:%S')
            except:
                continue
            
            # 检查时间窗口
            if not (start_time <= mail_time <= end_time):
                continue
            
            print(f"📨 [{i:2d}] 检查邮件: {subject} | {sender} | {readable_time}")

            # 读取邮件详细内容
            mail_content = read_mail_content(message_id)
            if not mail_content or mail_content.get('code') != 200:
                print(f"    ⚠️  无法读取邮件内容")
                continue

            result = mail_content.get('result', {})
            body_text = result.get('bodyText', '')
            body_html = result.get('bodyHtmlText', '')

            # 检查是否包含指定的邮箱前缀
            all_content = f"{subject} {body_text} {body_html}"
            if email_prefix not in all_content:
                print(f"    ⏭️  邮件不包含前缀 '{email_prefix}'，跳过")
                continue

            # 判断是否为验证码邮件
            if not is_verification_email(subject, sender, body_text, body_html):
                print(f"    ⏭️  不是验证码邮件，跳过")
                continue

            print(f"    🎯 找到匹配的验证码邮件，正在提取验证码...")

            # 提取验证码
            verification_code = None
            
            # 先在纯文本中搜索
            if body_text:
                verification_code = extract_verification_code(body_text)

            # 如果纯文本中没找到，再在HTML中搜索
            if not verification_code and body_html:
                verification_code = extract_verification_code(body_html)

            if verification_code:
                print(f"    ✅ 成功提取验证码: {verification_code}")
                return {
                    'verification_code': verification_code,
                    'mail_info': {
                        'subject': subject,
                        'sender': sender,
                        'create_time': readable_time,
                        'body_text': body_text[:200] + '...' if len(body_text) > 200 else body_text
                    }
                }
            else:
                print(f"    ❌ 未能从邮件中提取到验证码")

        print(f"🔄 第 {attempt + 1} 次尝试未找到验证码")
        if attempt < max_retries - 1:
            print(f"⏳ 等待 {retry_interval} 秒后重试...")
            time.sleep(retry_interval)

    print(f"💔 经过 {max_retries} 次尝试，未找到包含验证码的邮件")
    return None


def get_verification_code_with_retry(email_input, sent_time=None, time_window_minutes=10, max_retries=5, retry_interval=30):
    """
    便捷函数：获取验证码（带重试机制）
    支持邮箱前缀或完整邮箱地址输入
    
    Args:
        email_input (str): 邮箱前缀或完整邮箱地址
        sent_time (datetime): 发送验证码的时间
        time_window_minutes (int): 时间窗口（分钟）
        max_retries (int): 最大重试次数
        retry_interval (int): 重试间隔（秒）
        
    Returns:
        str: 验证码，如果未找到则返回None
    """
    # 自动提取前缀
    email_prefix = extract_email_prefix(email_input)
    
    result = find_verification_mail_by_alias(
        email_prefix=email_prefix,
        sent_time=sent_time,
        time_window_minutes=time_window_minutes,
        max_retries=max_retries,
        retry_interval=retry_interval
    )
    
    return result['verification_code'] if result else None
