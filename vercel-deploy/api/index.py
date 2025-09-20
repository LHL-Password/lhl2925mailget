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
from urllib.parse import urlparse, parse_qs

# 添加核心模块路径
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'core'))

try:
    from simple_verification import get_verification_code_with_retry
    print("✅ 成功导入验证码获取模块")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    get_verification_code_with_retry = None


def handler(request):
    """Vercel函数入口点"""
    try:
        # 设置CORS头
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        
        # 处理OPTIONS请求（CORS预检）
        if request.method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # 检查函数是否可用
        if get_verification_code_with_retry is None:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({
                    "success": False,
                    "error": "验证码获取功能不可用，请检查服务配置",
                    "timestamp": datetime.now().isoformat()
                }, ensure_ascii=False)
            }
        
        email_input = None
        time_window = 10
        max_retries = 3
        retry_interval = 20
        
        # 处理GET请求
        if request.method == 'GET':
            # 解析URL参数
            parsed_url = urlparse(request.url)
            query_params = parse_qs(parsed_url.query)
            
            email_input = query_params.get('email', [None])[0]
            if query_params.get('time_window'):
                time_window = int(query_params.get('time_window', [10])[0])
            if query_params.get('max_retries'):
                max_retries = int(query_params.get('max_retries', [3])[0])
            if query_params.get('retry_interval'):
                retry_interval = int(query_params.get('retry_interval', [20])[0])
        
        # 处理POST请求
        elif request.method == 'POST':
            try:
                # 读取请求体
                body = request.body
                if isinstance(body, bytes):
                    body = body.decode('utf-8')
                
                data = json.loads(body)
                email_input = data.get('email')
                time_window = data.get('time_window', 10)
                max_retries = data.get('max_retries', 3)
                retry_interval = data.get('retry_interval', 20)
                
            except json.JSONDecodeError:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({
                        "success": False,
                        "error": "无效的JSON数据",
                        "timestamp": datetime.now().isoformat()
                    }, ensure_ascii=False)
                }
        
        else:
            return {
                'statusCode': 405,
                'headers': headers,
                'body': json.dumps({
                    "success": False,
                    "error": "方法不允许",
                    "timestamp": datetime.now().isoformat()
                }, ensure_ascii=False)
            }
        
        # 验证邮箱参数
        if not email_input:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    "success": False,
                    "error": "缺少email参数",
                    "timestamp": datetime.now().isoformat()
                }, ensure_ascii=False)
            }
        
        print(f"收到验证码获取请求: {email_input}")
        
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
        else:
            # 未找到验证码
            response_data = {
                "success": False,
                "verification_code": None,
                "email": email_input,
                "timestamp": datetime.now().isoformat(),
                "message": "未找到验证码，请确认邮箱地址正确且验证码邮件已发送"
            }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response_data, ensure_ascii=False)
        }
        
    except Exception as e:
        print(f"Handler error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json; charset=utf-8',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "success": False,
                "error": f"服务器内部错误: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }, ensure_ascii=False)
        }
