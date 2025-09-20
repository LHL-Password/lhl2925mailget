#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel API函数：获取验证码
接收邮箱输入，返回对应的验证码
"""

import json
import sys
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# 添加核心模块路径
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'core'))

try:
    from simple_verification import get_verification_code_with_retry
except ImportError as e:
    print(f"Import error: {e}")
    # 如果导入失败，尝试直接导入
    try:
        import simple_verification
        get_verification_code_with_retry = simple_verification.get_verification_code_with_retry
    except ImportError as e2:
        print(f"Fallback import error: {e2}")
        get_verification_code_with_retry = None


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理GET请求"""
        try:
            # 解析URL和参数
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # 获取邮箱参数
            email_input = query_params.get('email', [None])[0]
            
            if not email_input:
                self.send_error_response(400, "缺少email参数")
                return
            
            # 获取可选参数
            time_window = int(query_params.get('time_window', [10])[0])
            max_retries = int(query_params.get('max_retries', [3])[0])
            retry_interval = int(query_params.get('retry_interval', [20])[0])
            
            print(f"收到验证码获取请求: {email_input}")

            # 检查函数是否可用
            if get_verification_code_with_retry is None:
                self.send_error_response(500, "验证码获取功能不可用，请检查服务配置")
                return

            # 调用验证码获取函数
            result = get_verification_code_with_retry(
                email_input=email_input,
                sent_time=datetime.now(),
                time_window_minutes=time_window,
                max_retries=max_retries,
                retry_interval=retry_interval
            )
            
            if result:
                # 成功获取验证码
                response_data = {
                    "success": True,
                    "verification_code": result,
                    "email": email_input,
                    "timestamp": datetime.now().isoformat(),
                    "message": "验证码获取成功"
                }
                self.send_success_response(response_data)
            else:
                # 未找到验证码
                response_data = {
                    "success": False,
                    "verification_code": None,
                    "email": email_input,
                    "timestamp": datetime.now().isoformat(),
                    "message": "未找到验证码，请确认邮箱地址正确且验证码邮件已发送"
                }
                self.send_success_response(response_data)
                
        except Exception as e:
            print(f"处理请求时出错: {e}")
            self.send_error_response(500, f"服务器内部错误: {str(e)}")
    
    def do_POST(self):
        """处理POST请求"""
        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # 解析JSON数据
            try:
                data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                self.send_error_response(400, "无效的JSON数据")
                return
            
            # 获取邮箱参数
            email_input = data.get('email')
            
            if not email_input:
                self.send_error_response(400, "缺少email参数")
                return
            
            # 获取可选参数
            time_window = data.get('time_window', 10)
            max_retries = data.get('max_retries', 3)
            retry_interval = data.get('retry_interval', 20)
            
            print(f"收到验证码获取请求: {email_input}")

            # 检查函数是否可用
            if get_verification_code_with_retry is None:
                self.send_error_response(500, "验证码获取功能不可用，请检查服务配置")
                return

            # 调用验证码获取函数
            result = get_verification_code_with_retry(
                email_input=email_input,
                sent_time=datetime.now(),
                time_window_minutes=time_window,
                max_retries=max_retries,
                retry_interval=retry_interval
            )
            
            if result:
                # 成功获取验证码
                response_data = {
                    "success": True,
                    "verification_code": result,
                    "email": email_input,
                    "timestamp": datetime.now().isoformat(),
                    "message": "验证码获取成功"
                }
                self.send_success_response(response_data)
            else:
                # 未找到验证码
                response_data = {
                    "success": False,
                    "verification_code": None,
                    "email": email_input,
                    "timestamp": datetime.now().isoformat(),
                    "message": "未找到验证码，请确认邮箱地址正确且验证码邮件已发送"
                }
                self.send_success_response(response_data)
                
        except Exception as e:
            print(f"处理POST请求时出错: {e}")
            self.send_error_response(500, f"服务器内部错误: {str(e)}")
    
    def send_success_response(self, data):
        """发送成功响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response_json = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(response_json.encode('utf-8'))
    
    def send_error_response(self, status_code, message):
        """发送错误响应"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        error_data = {
            "success": False,
            "error": message,
            "timestamp": datetime.now().isoformat()
        }
        
        response_json = json.dumps(error_data, ensure_ascii=False, indent=2)
        self.wfile.write(response_json.encode('utf-8'))
    
    def do_OPTIONS(self):
        """处理OPTIONS请求（CORS预检）"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


# Vercel函数入口点
def handler_function(request):
    """Vercel函数入口点"""
    return handler(request)
