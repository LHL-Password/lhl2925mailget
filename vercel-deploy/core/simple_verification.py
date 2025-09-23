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
CURRENT_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiMCIsImdyYW50X3R5cGUiOiJXZWJDbGllbnQiLCJuYW1lIjoibGkxMjE0NjUyOTgxQDI5MjUuY29tIiwibmlja25hbWUiOiJsaTEyMTQ2NTI5ODEiLCJpZCI6IjcxNTQ2YmZiLTJkMTctM2E2Ni04YjQxLTFjYTM1OGFlZThmNiIsImRldmljZUlkIjoiZGV2aWNlSWQiLCJ0b2tlbkZsYWciOiIwIiwiY2xpZW50X2lkIjoiQjkyNTdGN0Y5QjFFRjE1Q0UiLCJyZXFJZCI6ImE2YzNmNDY4LTg3OWQtNGFjMi05NTE2LWQ5ZWNkZDE3ZjExMCIsImF1ZCI6IkI5MjU3RjdGOUIxRUYxNUNFIiwic3ViIjoiNzE1NDZiZmItMmQxNy0zYTY2LThiNDEtMWNhMzU4YWVlOGY2IiwianRpIjoiNzE1NDZiZmItMmQxNy0zYTY2LThiNDEtMWNhMzU4YWVlOGY2IiwiaWF0IjoxNzU4NjM4MjY5LCJpc3MiOiJodHRwczovL21haWxsb2dpbi4yOTgwLmNvbS9vYXV0aCIsImV4cCI6MTc1ODY0NTQ2OSwibmJmIjoxNzU4NjM4MjA5fQ.Rn-r-2zjb-BXZ4A8NKOUMUxCBUWuAU6U2upDK9Am520"

# AUC token (从登录cookies中获取，用于邮件API请求)
AUC_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyZWZyZXNoX2FnZW50IjoiOWdKekZBWG5GOGlkSUVvRXVXZTdKVUhhUWhJTXVoYVFPUDFnbEJiT1M3dz0iLCJncmFudF90eXBlIjoiV2ViQ2xpZW50IiwiY2xpZW50X2lkIjoiQjkyNTdGN0Y5QjFFRjE1Q0UiLCJyZXFJZCI6ImE2YzNmNDY4LTg3OWQtNGFjMi05NTE2LWQ5ZWNkZDE3ZjExMCIsImF1ZCI6IkI5MjU3RjdGOUIxRUYxNUNFIiwic3ViIjoiNzE1NDZiZmItMmQxNy0zYTY2LThiNDEtMWNhMzU4YWVlOGY2IiwianRpIjoiNzE1NDZiZmItMmQxNy0zYTY2LThiNDEtMWNhMzU4YWVlOGY2IiwiaWF0IjoxNzU4NjM4MjY5LCJpc3MiOiJodHRwczovL21haWxsb2dpbi4yOTgwLmNvbS9vYXV0aCIsImV4cCI6MTc1ODY4MTQ2OSwibmJmIjoxNzU4NjM4MjY5fQ.QacN1em8Jx1LP_AFOcjv-MYg7AD8tY64s_lWW_cUnBU"

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


# 内嵌Login2925类的简化版本（与原版完全一致的逻辑）
class Login2925:
    def __init__(self):
        self.base_url = "https://www.2925.com"
        self.login_url = f"{self.base_url}/mailv2/auth/weblogin"
        self.session = requests.Session()

        # 设置默认请求头（与debug_login.py完全一致）
        self.session.headers.update({
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.base_url,
            'Pragma': 'no-cache',
            'Priority': 'u=1, i',
            'Referer': f'{self.base_url}/login/',
            'Sec-Ch-Ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0',
            'X-Requested-With': 'XMLHttpRequest'
        })

    def generate_trace_id(self):
        """生成traceId"""
        return str(uuid.uuid4()).replace('-', '')[:12]

    def generate_device_id(self):
        """生成设备ID"""
        return str(uuid.uuid4())

    def login(self, username, password, rsa_password=None, use_fixed_data=False):
        """
        登录获取token（与原版Login2925完全一致的逻辑）

        Args:
            username (str): 用户名/邮箱
            password (str): 密码
            rsa_password (str): RSA加密后的密码，如果提供则使用此参数
            use_fixed_data (bool): 是否使用固定的设备ID和traceID

        Returns:
            dict: 登录结果，包含token等信息
        """
        try:
            if use_fixed_data:
                # 使用提供的固定数据
                trace_id = "81de9b3ea212"
                device_uid = "5a7cdb83-822d-4e42-8487-7f90febb3311"
                device_id = "394a7110-44d8-11f0-99db-2d8fcb53f12a"
            else:
                # 生成随机参数
                trace_id = self.generate_trace_id()
                device_uid = self.generate_device_id()
                device_id = self.generate_device_id()

            # 设置设备ID头
            self.session.headers['deviceuid'] = device_uid

            # 构建登录URL
            login_url_with_trace = f"{self.login_url}?traceId={trace_id}"

            # 构建请求数据
            login_data = {
                'uname': username,
                'rsapwd': rsa_password if rsa_password else password,
                'deviceIds[]': device_id,
                'pass': '',
                'rememberLogin': 'false'
            }

            # 发送登录请求
            print(f"正在登录用户: {username}")
            print(f"请求URL: {login_url_with_trace}")
            print(f"🔍 登录数据: {login_data}")

            from urllib.parse import urlencode
            response = self.session.post(
                login_url_with_trace,
                data=urlencode(login_data, doseq=True),
                timeout=30
            )

            # 检查响应状态
            response.raise_for_status()

            # 打印响应头信息以便调试
            print(f"🔍 响应状态码: {response.status_code}")
            print(f"🔍 响应头: {dict(response.headers)}")
            print(f"🔍 响应cookies: {dict(response.cookies)}")

            # 检查响应内容类型
            content_type = response.headers.get('content-type', '').lower()
            print(f"🔍 响应内容类型: {content_type}")

            # 如果返回的是HTML而不是JSON，说明请求有问题
            if 'text/html' in content_type:
                print("❌ 服务器返回HTML页面而不是JSON，可能是请求参数或URL有误")
                print(f"📄 响应内容预览: {response.text[:200]}...")
                return {
                    'success': False,
                    'error': '服务器返回HTML页面而不是JSON响应',
                    'response_preview': response.text[:500]
                }

            # 解析JSON响应
            try:
                result = response.json()
                print(f"🔍 完整result内容: {result}")
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                print(f"📄 响应内容: {response.text[:500]}...")
                return {
                    'success': False,
                    'error': f'JSON解析失败: {e}',
                    'response_text': response.text[:500]
                }

            # 检查登录是否成功 - 支持两种响应格式
            success = False
            token = None
            refresh_token = None
            app_info = {}

            # 格式1: 新版API响应格式 {"success": true, "resCode": 200, "token": "..."}
            if result.get('success') and result.get('resCode') == 200:
                success = True
                token = result.get('token')
                refresh_token = result.get('refreashToken')
                app_info = result.get('appInfo', {})
                print("✅ 检测到新版API响应格式")

            # 格式2: 旧版API响应格式 {"code": 200, "result": {"success": true, "token": "..."}}
            elif result.get('code') == 200 and result.get('result', {}).get('success'):
                success = True
                result_data = result.get('result', {})
                token = result_data.get('token')
                refresh_token = result_data.get('refreashToken')
                app_info = result_data.get('appInfo', {})
                print("✅ 检测到旧版API响应格式")

            if success:
                print("登录成功!")

                print(f"Token: {token}")
                print(f"Refresh Token: {refresh_token}")
                print(f"用户信息: {app_info.get('name', '未知')}")

                # 检查token是否为空
                if not token:
                    print("❌ 登录成功但未找到token字段")
                    print(f"🔍 完整result内容: {result}")

                    # 尝试从其他可能的字段获取token
                    possible_token_fields = ['accessToken', 'access_token', 'authToken', 'auth_token', 'jwt', 'bearerToken', 'key', 'secKey']

                    # 首先检查result_data（旧版API格式）
                    if 'result_data' in locals():
                        for field in possible_token_fields:
                            if result_data.get(field):
                                token = result_data.get(field)
                                print(f"✅ 从result_data字段 '{field}' 找到token: {token[:50]}...")
                                break

                        # 如果还没找到，尝试从appInfo中获取
                        if not token and result_data.get('appInfo'):
                            app_info_data = result_data.get('appInfo', {})
                            for field in possible_token_fields:
                                if app_info_data.get(field):
                                    token = app_info_data.get(field)
                                    print(f"✅ 从appInfo字段 '{field}' 找到token: {token[:50]}...")
                                    break

                    # 如果还没找到，从顶级result中查找
                    if not token:
                        for field in possible_token_fields:
                            if result.get(field):
                                token = result.get(field)
                                print(f"✅ 从顶级字段 '{field}' 找到token: {token[:50]}...")
                                break

                    # 如果还是没有找到token，尝试访问回调URL获取真正的token
                    if not token:
                        callback_url = result.get('result', {}).get('url') if result.get('result') else result.get('url')
                        if callback_url:
                            print(f"🔗 尝试访问回调URL获取token: {callback_url}")
                            try:
                                # 为服务器环境添加更多的请求头
                                callback_headers = self.session.headers.copy()
                                callback_headers.update({
                                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                                    'Connection': 'keep-alive',
                                    'Upgrade-Insecure-Requests': '1',
                                })

                                callback_response = self.session.get(
                                    callback_url,
                                    headers=callback_headers,
                                    timeout=30,
                                    allow_redirects=True
                                )
                                print(f"🔍 回调响应状态码: {callback_response.status_code}")
                                print(f"🔍 回调响应cookies: {dict(callback_response.cookies)}")

                                # 检查回调响应的cookies中是否有token
                                for cookie_name, cookie_value in callback_response.cookies.items():
                                    if ('token' in cookie_name.lower() or 'auth' in cookie_name.lower() or
                                        'auc' in cookie_name.lower() or 'jwt' in cookie_name.lower()):
                                        print(f"🍪 从回调URL获取到token cookie: {cookie_name} = {cookie_value[:50]}...")
                                        token = cookie_value
                                        break

                                # 如果回调响应是JSON，也尝试解析
                                if not token and 'application/json' in callback_response.headers.get('content-type', ''):
                                    try:
                                        callback_data = callback_response.json()
                                        for field in possible_token_fields:
                                            if callback_data.get(field):
                                                token = callback_data.get(field)
                                                print(f"✅ 从回调响应字段 '{field}' 找到token: {token[:50]}...")
                                                break
                                    except:
                                        pass

                            except Exception as e:
                                print(f"❌ 访问回调URL失败: {e}")

                    # 如果还是没有token，尝试使用key字段作为临时方案（仅用于服务器环境）
                    if not token:
                        key_value = result.get('result', {}).get('key') if result.get('result') else result.get('key')
                        if key_value:
                            print(f"⚠️  作为备用方案，尝试使用key字段: {key_value}")
                            # 这里我们可以尝试用key值进行后续的API调用测试
                            token = key_value
                            print("🔧 使用key作为临时token，将在后续API调用中验证其有效性")

                    if not token:
                        print("❌ 在所有可能的字段中都未找到token")
                        # 如果仍然没有token，但登录成功，可能需要从cookies或其他地方获取
                        print("🔍 尝试从响应cookies中查找token...")
                        for cookie_name, cookie_value in response.cookies.items():
                            if 'token' in cookie_name.lower() or 'auth' in cookie_name.lower() or 'auc' in cookie_name.lower():
                                print(f"🍪 发现可能的token cookie: {cookie_name} = {cookie_value[:50]}...")
                                if not token:  # 如果还没有token，使用第一个找到的
                                    token = cookie_value
                                    print(f"✅ 使用cookie作为token: {cookie_name}")
                                    break

                # 从响应头中获取cookies
                cookies = {}
                if hasattr(response, 'cookies'):
                    for cookie in response.cookies:
                        cookies[cookie.name] = cookie.value

                return {
                    'success': True,
                    'token': token,
                    'refresh_token': refresh_token,
                    'user_info': app_info,
                    'cookies': cookies,
                    'full_response': result
                }
            else:
                print(f"登录失败: {result.get('message', '未知错误')}")
                return {
                    'success': False,
                    'message': result.get('message', '未知错误'),
                    'full_response': result
                }

        except requests.exceptions.RequestException as e:
            print(f"网络请求错误: {e}")
            return {
                'success': False,
                'error': f"网络请求错误: {e}"
            }
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return {
                'success': False,
                'error': f"JSON解析错误: {e}"
            }
        except Exception as e:
            print(f"未知错误: {e}")
            return {
                'success': False,
                'error': f"未知错误: {e}"
            }








def auto_refresh_token_if_needed():
    """
    自动检测token是否过期，如果过期则调用Login2925更新token
    （与get_verification_by_alias_v2.py完全一致的逻辑）

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

        # 创建登录实例（与get_verification_by_alias_v2.py完全一致）
        login_client = Login2925()

        # 使用配置文件中的登录信息（与get_verification_by_alias_v2.py完全一致）
        username = USERNAME  # 从配置获取
        password = "lhl1214652981"  # 这个应该从安全的地方获取，比如环境变量
        rsa_password = "e43e00e9dac20bb7d39e00ed9ddd87fd"  # 这个也应该从安全的地方获取

        print(f"� 正在使用账户 {username} 重新登录...")

        # 执行登录（与get_verification_by_alias_v2.py完全一致的参数）
        result = login_client.login(username, password, rsa_password, use_fixed_data=True)

        if result['success']:
            # 获取新token并更新全局变量
            new_token = result.get('token')
            if new_token:
                print("✅ Token自动更新成功！")
                CURRENT_TOKEN = new_token
                DEFAULT_HEADERS['Authorization'] = f'Bearer {new_token}'

                # 同时更新AUC token（从cookies中获取）
                cookies = result.get('cookies', {})
                global AUC_TOKEN
                if 'auc' in cookies:
                    AUC_TOKEN = cookies['auc']
                    print(f"✅ 同时获取到AUC token")

                return True
            else:
                print("❌ 登录成功但未获取到有效token")
                print(f"🔍 登录响应: {result.get('full_response', {})}")
                return False
        else:
            print(f"❌ Token自动更新失败: {result.get('message', result.get('error'))}")
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
    """内部函数：获取邮件列表（修复：添加cookies支持和多种token格式支持）"""
    global CURRENT_TOKEN
    try:
        params = {
            'Folder': 'Inbox',
            'MailBox': MAILBOX,
            'FilterType': '0',
            'PageIndex': '1',
            'PageCount': str(page_count),
            'traceId': generate_trace_id()
        }

        # 使用session来设置cookies（关键修复！）
        session = requests.Session()

        # 设置cookies - 这是关键！
        cookies = {
            'aut': CURRENT_TOKEN,
            'jwt_token': CURRENT_TOKEN,
            'account': MAILBOX.replace('@', '%40'),
            'uid': '71546bfb-2d17-3a66-8b41-1ca358aee8f6'  # 用户ID
        }

        # 如果有AUC token，也添加到cookies中
        if AUC_TOKEN:
            cookies['auc'] = AUC_TOKEN
            print(f"🍪 使用AUC token: {AUC_TOKEN[:50]}...")

        # 如果CURRENT_TOKEN看起来像UUID格式（可能是key字段），尝试多种cookie设置
        if len(CURRENT_TOKEN) == 36 and CURRENT_TOKEN.count('-') == 4:
            print(f"🔧 检测到UUID格式的token，尝试多种cookie设置方式")
            cookies.update({
                'key': CURRENT_TOKEN,
                'secKey': CURRENT_TOKEN,
                'sessionKey': CURRENT_TOKEN,
                'authKey': CURRENT_TOKEN
            })

        for name, value in cookies.items():
            session.cookies.set(name, value)

        # 同时在请求头中也尝试多种认证方式
        headers = DEFAULT_HEADERS.copy()
        headers.update({
            'X-Auth-Token': CURRENT_TOKEN,
            'X-Session-Key': CURRENT_TOKEN,
            'X-API-Key': CURRENT_TOKEN
        })

        print(f"🔍 使用的cookies: {list(cookies.keys())}")
        print(f"🔍 请求URL: {MAIL_LIST_URL}")
        print(f"🔍 请求参数: {params}")

        response = session.get(MAIL_LIST_URL, params=params, headers=headers, timeout=30)

        print(f"🔍 邮件列表响应状态码: {response.status_code}")
        print(f"🔍 邮件列表响应头: {dict(response.headers)}")

        # 检查响应内容类型
        content_type = response.headers.get('content-type', '').lower()
        print(f"🔍 响应内容类型: {content_type}")

        if 'text/html' in content_type:
            print("❌ 服务器返回HTML页面，可能是认证失败被重定向到登录页")
            print(f"📄 响应内容预览: {response.text[:200]}...")

            # 尝试重新登录获取新的token
            print("🔄 尝试重新登录获取有效token...")
            login_client = Login2925()
            login_result = login_client.login(USERNAME, PASSWORD, RSA_PASSWORD, use_fixed_data=True)

            if login_result.get('success') and login_result.get('token'):
                print("✅ 重新登录成功，使用新token重试...")
                CURRENT_TOKEN = login_result['token']

                # 更新cookies和headers
                cookies['aut'] = CURRENT_TOKEN
                cookies['jwt_token'] = CURRENT_TOKEN
                headers['Authorization'] = f'Bearer {CURRENT_TOKEN}'

                # 重新设置cookies
                for name, value in cookies.items():
                    session.cookies.set(name, value)

                # 重新发送请求
                response = session.get(MAIL_LIST_URL, params=params, headers=headers, timeout=30)
                print(f"🔍 重试后响应状态码: {response.status_code}")

                if 'text/html' in response.headers.get('content-type', '').lower():
                    print("❌ 重新登录后仍然返回HTML，可能是API端点或参数问题")
                    return None
            else:
                print("❌ 重新登录失败")
                return None

        if response.status_code != 200:
            print(f"🔍 邮件列表响应内容: {response.text[:500]}")

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
