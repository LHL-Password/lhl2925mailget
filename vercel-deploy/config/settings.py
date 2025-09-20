#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel部署版配置文件
简化版的邮件服务配置
"""

import os

# 从环境变量获取敏感信息，如果没有则使用默认值
CURRENT_TOKEN = os.getenv('MAIL_TOKEN', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiMCIsImdyYW50X3R5cGUiOiJXZWJDbGllbnQiLCJuYW1lIjoibGkxMjE0NjUyOTgxQDI5MjUuY29tIiwibmlja25hbWUiOiJsaTEyMTQ2NTI5ODEiLCJpZCI6IjcxNTQ2YmZiLTJkMTctM2E2Ni04YjQxLTFjYTM1OGFlZThmNiIsImRldmljZUlkIjoiZGV2aWNlSWQiLCJ0b2tlbkZsYWciOiIwIiwiY2xpZW50X2lkIjoiQjkyNTdGN0Y5QjFFRjE1Q0UiLCJyZXFJZCI6ImQ1NWU3YjE1LTg5NWYtNDdhMi04MGFkLTlkNzEzZDExMzgzYSIsImF1ZCI6IkI5MjU3RjdGOUIxRUYxNUNFIiwic3ViIjoiNzE1NDZiZmItMmQxNy0zYTY2LThiNDEtMWNhMzU4YWVlOGY2IiwianRpIjoiNzE1NDZiZmItMmQxNy0zYTY2LThiNDEtMWNhMzU4YWVlOGY2IiwiaWF0IjoxNzU4MzAyMTg0LCJpc3MiOiJodHRwczovL21haWxsb2dpbi4yOTgwLmNvbS9vYXV0aCIsImV4cCI6MTc1ODMwOTM4NCwibmJmIjoxNzU4MzAyMTI0fQ.P7WbR_g5LAYX75u8MQ_mDTYNb0cLOq4jYBTJ-mXotOI')

# 用户信息
USERNAME = "li1214652981@2925.com"
MAILBOX = "li1214652981@2925.com"
DEVICE_UID = "e3cbddaa-e77a-4eb8-b15a-fed018ad137a"

# API配置
BASE_URL = "https://www.2925.com"
MAIL_LIST_URL = f"{BASE_URL}/mailv2/maildata/MailList/mails"
MAIL_READ_URL = f"{BASE_URL}/mailv2/maildata/MailRead/mails/read"

# 默认请求头
DEFAULT_HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Priority': 'u=1, i',
    'Referer': 'https://www.2925.com/',
    'Sec-Ch-Ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0',
    'X-Requested-With': 'XMLHttpRequest',
    'deviceuid': DEVICE_UID
}

def get_auth_headers():
    """获取带认证的请求头"""
    headers = DEFAULT_HEADERS.copy()
    headers['Authorization'] = f'Bearer {CURRENT_TOKEN}'
    return headers

# 验证码配置
VERIFICATION_CONFIG = {
    'default_time_window_minutes': 10,
    'default_max_retries': 5,
    'default_retry_interval': 30,
    'verification_keywords': [
        'verification code', 'verify', 'code', '验证码', '验证',
        'confirm', 'authentication', 'otp', 'one-time', 'security code'
    ],
    'exclude_keywords': [
        'exhibition', 'expo', 'conference', 'meeting', 'event',
        '博览会', '展会', '会议', '活动', 'invitation', '邀请'
    ]
}
