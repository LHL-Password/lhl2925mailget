#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版验证码获取模块
专门为Vercel部署优化，减少依赖
"""

import requests
import json
import uuid
import re
import time
from datetime import datetime, timedelta, timezone

# 中国时区
CHINA_TZ = timezone(timedelta(hours=8))

def get_china_time():
    """获取中国时区的当前时间"""
    return datetime.now(CHINA_TZ)

# 配置信息（直接内嵌，避免复杂的导入）
CURRENT_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiMCIsImdyYW50X3R5cGUiOiJXZWJDbGllbnQiLCJuYW1lIjoibGkxMjE0NjUyOTgxQDI5MjUuY29tIiwibmlja25hbWUiOiJsaTEyMTQ2NTI5ODEiLCJpZCI6IjcxNTQ2YmZiLTJkMTctM2E2Ni04YjQxLTFjYTM1OGFlZThmNiIsImRldmljZUlkIjoiZGV2aWNlSWQiLCJ0b2tlbkZsYWciOiIwIiwiY2xpZW50X2lkIjoiQjkyNTdGN0Y5QjFFRjE1Q0UiLCJyZXFJZCI6Ijk2ZjkxZDYwLWJiZTktNDIxOC05MThiLTA5NDI3N2VhYmViYyIsImF1ZCI6IkI5MjU3RjdGOUIxRUYxNUNFIiwic3ViIjoiNzE1NDZiZmItMmQxNy0zYTY2LThiNDEtMWNhMzU4YWVlOGY2IiwianRpIjoiNzE1NDZiZmItMmQxNy0zYTY2LThiNDEtMWNhMzU4YWVlOGY2IiwiaWF0IjoxNzU4MzU2ODYyLCJpc3MiOiJodHRwczovL21haWxsb2dpbi4yOTgwLmNvbS9vYXV0aCIsImV4cCI6MTc1ODM2NDA2MiwibmJmIjoxNzU4MzU2ODAyfQ.aMfMHRBcg3_dHlTNgrI_ZpG4fYpv6eLnoYN1uaT_Nrc"

# 登录配置信息
USERNAME = "li1214652981@2925.com"
PASSWORD = "lhl1214652981"
RSA_PASSWORD = "e43e00e9dac20bb7d39e00ed9ddd87fd"

MAILBOX = "li1214652981@2925.com"
DEVICE_UID = "e3cbddaa-e77a-4eb8-b15a-fed018ad137a"
BASE_URL = "https://www.2925.com"
MAIL_LIST_URL = f"{BASE_URL}/mailv2/maildata/MailList/mails"
MAIL_READ_URL = f"{BASE_URL}/mailv2/maildata/MailRead/mails/read"

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
    'deviceuid': DEVICE_UID,
    'Authorization': f'Bearer {CURRENT_TOKEN}'
}


def generate_trace_id():
    """生成traceId"""
    return str(uuid.uuid4()).replace('-', '')[:12]


def is_token_valid():
    """检查token是否有效（简单检查）"""
    import base64
    import json
    try:
        # 简单解码JWT token（不验证签名）
        parts = CURRENT_TOKEN.split('.')
        if len(parts) != 3:
            print("❌ Token格式无效")
            return False

        # 解码payload部分
        payload = parts[1]
        # 添加padding如果需要
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding

        decoded = base64.b64decode(payload)
        token_data = json.loads(decoded)

        # 检查过期时间
        exp = token_data.get('exp', 0)
        current_time = time.time()

        if current_time >= exp:
            print("❌ Token已过期")
            return False

        print("✅ Token有效")
        return True

    except Exception as e:
        print(f"❌ Token验证失败: {e}")
        return False


def get_new_token():
    """获取新的token（使用与login_2925.py相同的逻辑）"""
    try:
        # 使用固定数据登录
        trace_id = "81de9b3ea212"
        device_uid = "5a7cdb83-822d-4e42-8487-7f90febb3311"
        device_id = "394a7110-44d8-11f0-99db-2d8fcb53f12a"

        # 创建session（关键差异1）
        session = requests.Session()

        # 设置完整的请求头（关键差异2）
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Accept-Encoding': 'gzip, deflate, br, zstd',  # 关键差异3
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.2925.com',
            'Referer': 'https://www.2925.com/login/',
            'Sec-Ch-Ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest',
            'deviceuid': device_uid,  # 关键差异4：设置在headers中
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        })

        # 请求URL
        url = f"https://www.2925.com/mailv2/auth/weblogin?traceId={trace_id}"

        # 请求数据
        from urllib.parse import urlencode
        data = {
            'uname': USERNAME,
            'rsapwd': RSA_PASSWORD,
            'deviceIds[]': device_id,
            'pass': '',
            'rememberLogin': 'false'
        }

        # 发送请求（使用session）
        response = session.post(
            url,
            data=urlencode(data, doseq=True),
            timeout=30
        )

        response.raise_for_status()
        result = response.json()

        # 检查登录结果
        print(f"🔍 登录响应: code={result.get('code')}, success={result.get('result', {}).get('success')}")

        # 添加详细的调试信息
        result_data = result.get('result', {})
        print(f"🔍 result字段内容: {list(result_data.keys()) if result_data else 'None'}")

        # 处理cookies（关键差异5）
        cookies = {}
        if hasattr(response, 'cookies'):
            for cookie in response.cookies:
                cookies[cookie.name] = cookie.value
            print(f"🍪 获取到cookies: {list(cookies.keys())}")

        if result.get('code') == 200 and result.get('result', {}).get('success'):
            # 获取token和refresh_token
            token = result_data.get('token', '').strip()
            refresh_token = result_data.get('refreashToken', '').strip()  # 注意拼写

            print(f"🔍 Token: '{token[:50]}...' (长度: {len(token)})" if token else "🔍 Token: 空")
            print(f"🔍 RefreshToken: '{refresh_token[:50]}...' (长度: {len(refresh_token)})" if refresh_token else "🔍 RefreshToken: 空")

            # 检查token有效性
            if token and len(token) > 50:  # JWT token通常很长
                print(f"✅ 成功获取有效token")
                return token
            else:
                print(f"❌ Token无效或为空")
                print(f"🔍 完整result内容: {result_data}")

                # 如果有回调URL，记录但不处理（服务器环境可能不支持）
                callback_url = result_data.get('url')
                if callback_url:
                    print(f"🔗 发现回调URL: {callback_url}")
                    print(f"⚠️  服务器环境暂不支持回调URL处理")

                return None
        else:
            print(f"❌ 登录失败: {result.get('message', '未知错误')}")
            print(f"🔍 完整响应: {result}")
            return None

    except Exception as e:
        print(f"❌ 获取新token失败: {e}")
        return None


def auto_refresh_token_if_needed():
    """
    自动检测token是否过期，如果过期则更新token

    Returns:
        bool: True表示token有效或更新成功，False表示更新失败
    """
    global CURRENT_TOKEN, DEFAULT_HEADERS

    try:
        # 检查当前token是否有效
        if is_token_valid():
            print("🔑 Token有效，无需更新")
            return True

        print("⚠️  检测到Token已过期，正在自动更新...")

        # 获取新token
        new_token = get_new_token()

        print(f"🔍 调试信息: new_token = {new_token[:50] if new_token else 'None'}...")

        if new_token:
            # 更新全局token
            global CURRENT_TOKEN, DEFAULT_HEADERS
            CURRENT_TOKEN = new_token
            DEFAULT_HEADERS['Authorization'] = f'Bearer {new_token}'

            # 验证更新是否成功
            print(f"🔍 更新后的token: {CURRENT_TOKEN[:50]}...")
            print("✅ Token自动更新成功！")
            return True
        else:
            print("❌ Token自动更新失败 - 未获取到有效token")
            return False

    except Exception as e:
        print(f"❌ Token自动更新过程出错: {e}")
        return False


def extract_email_prefix(email_input):
    """
    从邮箱地址或前缀中提取前6位作为匹配前缀

    Args:
        email_input (str): 邮箱前缀或完整邮箱地址

    Returns:
        str: 提取的前6位前缀
    """
    if '@' in email_input:
        # 如果输入的是完整邮箱地址，提取@前面的部分，然后取前6位
        prefix = email_input.split('@')[0][:6]
        print(f"📧 从完整邮箱地址提取前缀: '{email_input}' -> '{prefix}'")
        return prefix
    else:
        # 如果输入的是前缀，直接使用（取前6位）
        prefix = email_input[:6]
        print(f"📧 使用输入的前缀: '{prefix}'")
        return prefix


def extract_verification_code(text):
    """从文本中提取验证码"""
    patterns = [
        r'Your verification code is:\s*<b>(\d{6})</b>',
        r'Your verification code is:\s*(\d{6})',
        r'verification code is:\s*<b>(\d{6})</b>',
        r'verification code is:\s*(\d{6})',
        r'验证码[：:]\s*(\d{6})',
        r'验证码为[：:]\s*(\d{6})',
        r'code[：:]\s*(\d{6})',
        r'security code[：:]\s*(\d{6})',
        r'OTP[：:]\s*(\d{6})',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            code = match.group(1)
            if len(code) == 6 and not code.startswith('20'):
                return code

    if 'verification' in text.lower() or 'verify' in text.lower() or '验证' in text:
        matches = re.findall(r'\b(\d{6})\b', text)
        for code in matches:
            if not code.startswith('20') and code != '000000' and code != '123456':
                return code

    return None


def is_verification_email(subject, sender, body_text, body_html):
    """判断是否为验证码邮件"""
    verification_keywords = [
        'verification code', 'verify', 'code', '验证码', '验证',
        'confirm', 'authentication', 'otp', 'one-time', 'security code'
    ]
    
    exclude_keywords = [
        'exhibition', 'expo', 'conference', 'meeting', 'event',
        '博览会', '展会', '会议', '活动', 'invitation', '邀请'
    ]
    
    all_text = f"{subject} {sender} {body_text} {body_html}".lower()
    
    for exclude_word in exclude_keywords:
        if exclude_word.lower() in all_text:
            return False
    
    for keyword in verification_keywords:
        if keyword.lower() in all_text:
            return True
    
    return False


def get_mail_list(page_count=50):
    """获取邮件列表（支持自动token更新）"""
    # 首先尝试获取邮件列表
    result = _get_mail_list_internal(page_count)

    # 如果失败且可能是token问题，尝试更新token后重试
    if not result or result.get('code') in [401, 403, 10001]:  # 常见的认证失败错误码
        print("🔄 检测到可能的认证问题，尝试更新token...")
        if auto_refresh_token_if_needed():
            print("🔄 Token更新成功，重新尝试获取邮件列表...")
            result = _get_mail_list_internal(page_count)
        else:
            print("❌ Token更新失败，无法获取邮件列表")
            return None

    return result


def _get_mail_list_internal(page_count=50):
    """内部函数：获取邮件列表"""
    try:
        params = {
            'Folder': 'Inbox',
            'MailBox': MAILBOX,
            'FilterType': '0',
            'PageIndex': '1',
            'PageCount': str(page_count),
            'traceId': generate_trace_id()
        }

        response = requests.get(MAIL_LIST_URL, params=params, headers=DEFAULT_HEADERS, timeout=30)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"获取邮件列表失败: {e}")
        return None


def read_mail_content(message_id, folder_name="Inbox"):
    """读取指定邮件的详细内容（支持自动token更新）"""
    # 首先尝试读取邮件内容
    result = _read_mail_content_internal(message_id, folder_name)

    # 如果失败且可能是token问题，尝试更新token后重试
    if not result or result.get('code') in [401, 403, 10001]:
        print("🔄 检测到可能的认证问题，尝试更新token...")
        if auto_refresh_token_if_needed():
            print("🔄 Token更新成功，重新尝试读取邮件内容...")
            result = _read_mail_content_internal(message_id, folder_name)
        else:
            print("❌ Token更新失败，无法读取邮件内容")
            return None

    return result


def _read_mail_content_internal(message_id, folder_name="Inbox"):
    """内部函数：读取指定邮件的详细内容"""
    try:
        params = {
            'MessageID': message_id,
            'FolderName': folder_name,
            'MailBox': MAILBOX,
            'IsPre': 'true',
            'traceId': generate_trace_id()
        }

        # 使用session来设置cookies（重要！）
        session = requests.Session()

        # 设置cookies - 这是关键！
        cookies = {
            'aut': CURRENT_TOKEN,
            'jwt_token': CURRENT_TOKEN,
            'account': MAILBOX.replace('@', '%40'),
            'uid': 'user_id_placeholder'
        }

        for name, value in cookies.items():
            session.cookies.set(name, value)

        response = session.get(MAIL_READ_URL, params=params, headers=DEFAULT_HEADERS, timeout=30)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"读取邮件内容失败: {e}")
        return None


def get_verification_code_with_retry(email_input, sent_time=None, time_window_minutes=10, max_retries=5, retry_interval=30):
    """
    获取验证码（带重试机制）
    
    Args:
        email_input (str): 邮箱前缀或完整邮箱地址
        sent_time (datetime): 发送验证码的时间
        time_window_minutes (int): 时间窗口（分钟）
        max_retries (int): 最大重试次数
        retry_interval (int): 重试间隔（秒）
        
    Returns:
        str: 验证码，如果未找到则返回None
    """
    if sent_time is None:
        sent_time = get_china_time()
    
    email_prefix = extract_email_prefix(email_input)
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
            
            # 转换时间戳为datetime对象（带时区信息）
            try:
                # 创建带时区信息的datetime对象
                mail_time = datetime.fromtimestamp(int(create_time) / 1000, tz=CHINA_TZ)
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

            # 检查是否包含指定的邮箱前缀（按照v2版本的逻辑）
            # 只取前6位进行匹配，并查找特定的alias模式
            email_prefix_6 = email_prefix[:6]

            # 在邮件内容中查找特定的alias模式
            # 匹配模式: "This email was sent to the alias 'xyeqwe"
            alias_pattern = f"This email was sent to the alias '{email_prefix_6}"
            all_content = f"{subject} {body_text} {body_html}"

            if alias_pattern not in all_content:
                print(f"    ⏭️  邮件不包含前缀 '{email_prefix_6}' 的alias模式，跳过")
                continue

            # 判断是否为验证码邮件
            if not is_verification_email(subject, sender, body_text, body_html):
                print(f"    ⏭️  不是验证码邮件，跳过")
                continue

            print(f"    🎯 找到匹配的验证码邮件，正在提取验证码...")

            # 提取验证码
            verification_code = None
            
            if body_text:
                verification_code = extract_verification_code(body_text)

            if not verification_code and body_html:
                verification_code = extract_verification_code(body_html)

            if verification_code:
                print(f"    ✅ 成功提取验证码: {verification_code}")
                return verification_code
            else:
                print(f"    ❌ 未能从邮件中提取到验证码")

        print(f"🔄 第 {attempt + 1} 次尝试未找到验证码")
        if attempt < max_retries - 1:
            print(f"⏳ 等待 {retry_interval} 秒后重试...")
            time.sleep(retry_interval)

    print(f"💔 经过 {max_retries} 次尝试，未找到包含验证码的邮件")
    return None
