#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件API封装模块
简化版的邮件服务API调用
"""

import requests
import json
import uuid
from datetime import datetime
import sys
import os

# 添加config目录到路径
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config'))
from settings import (
    CURRENT_TOKEN, get_auth_headers, MAIL_LIST_URL, MAIL_READ_URL, MAILBOX
)


def generate_trace_id():
    """生成traceId"""
    return str(uuid.uuid4()).replace('-', '')[:12]


def get_mail_list(page_count=50):
    """
    获取邮件列表
    
    Args:
        page_count (int): 每页邮件数量
        
    Returns:
        dict: 邮件列表数据
    """
    try:
        params = {
            'Folder': 'Inbox',
            'MailBox': MAILBOX,
            'FilterType': '0',
            'PageIndex': '1',
            'PageCount': str(page_count),
            'traceId': generate_trace_id()
        }
        
        headers = get_auth_headers()
        
        response = requests.get(MAIL_LIST_URL, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result
        
    except Exception as e:
        print(f"获取邮件列表失败: {e}")
        return None


def read_mail_content(message_id, folder_name="Inbox"):
    """
    读取指定邮件的详细内容
    
    Args:
        message_id (str): 邮件ID
        folder_name (str): 文件夹名称
        
    Returns:
        dict: 邮件内容数据
    """
    try:
        params = {
            'MessageID': message_id,
            'FolderName': folder_name,
            'MailBox': MAILBOX,
            'IsPre': 'true',
            'traceId': generate_trace_id()
        }
        
        headers = get_auth_headers()
        
        response = requests.get(MAIL_READ_URL, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result
        
    except Exception as e:
        print(f"读取邮件内容失败: {e}")
        return None


def extract_email_prefix(email_input):
    """
    从邮箱地址中提取前缀
    
    Args:
        email_input (str): 邮箱前缀或完整邮箱地址
        
    Returns:
        str: 邮箱前缀
    """
    if '@' in email_input:
        return email_input.split('@')[0]
    return email_input


def is_verification_email(subject, sender, body_text, body_html):
    """
    判断是否为验证码邮件
    
    Args:
        subject (str): 邮件主题
        sender (str): 发件人
        body_text (str): 邮件文本内容
        body_html (str): 邮件HTML内容
        
    Returns:
        bool: 是否为验证码邮件
    """
    # 验证码关键词
    verification_keywords = [
        'verification code', 'verify', 'code', '验证码', '验证',
        'confirm', 'authentication', 'otp', 'one-time', 'security code'
    ]
    
    # 排除关键词
    exclude_keywords = [
        'exhibition', 'expo', 'conference', 'meeting', 'event',
        '博览会', '展会', '会议', '活动', 'invitation', '邀请'
    ]
    
    # 合并所有文本内容进行检查
    all_text = f"{subject} {sender} {body_text} {body_html}".lower()
    
    # 检查是否包含排除关键词
    for exclude_word in exclude_keywords:
        if exclude_word.lower() in all_text:
            return False
    
    # 检查是否包含验证码关键词
    for keyword in verification_keywords:
        if keyword.lower() in all_text:
            return True
    
    return False
