# 2925邮件验证码服务 - Vercel部署版

这是一个简化的邮件验证码获取服务，专门为Vercel部署优化。

## 功能特性

- ✅ 输入邮箱前缀获取验证码
- ✅ 支持实时验证码提取
- ✅ **自动Token刷新** - 当Token过期时自动更新
- ✅ 简洁的Web界面
- ✅ 无服务器架构，适合Vercel部署
- ✅ 智能错误处理和重试机制

## 目录结构

```
vercel-deploy/
├── api/                    # Vercel API函数
│   └── get-verification.py # 验证码获取API
├── public/                 # 静态文件
│   └── index.html         # 前端界面
├── core/                   # 核心功能模块
│   ├── mail_api.py        # 邮件API封装
│   └── verification.py    # 验证码提取逻辑
├── config/                 # 配置文件
│   └── settings.py        # 基础配置
├── vercel.json            # Vercel配置
├── requirements.txt       # Python依赖
└── README.md             # 说明文档
```

## 部署步骤

### 1. 准备GitHub仓库
```bash
# 创建新的GitHub仓库或使用现有仓库
# 将vercel-deploy目录上传到仓库根目录
```

### 2. Vercel部署配置
1. 登录 [Vercel](https://vercel.com)
2. 点击 "New Project"
3. 选择你的GitHub仓库
4. 配置项目设置：
   - **Framework Preset**: Other
   - **Root Directory**: `2925/vercel-deploy` (如果你的仓库结构是这样)
   - **Build Command**: 留空
   - **Output Directory**: 留空
   - **Install Command**: `pip install -r requirements.txt`

### 3. 环境变量配置（可选）
在Vercel项目设置中添加环境变量：
- `MAIL_TOKEN`: 邮件服务token（如果需要更新token）

### 4. 部署
点击 "Deploy" 按钮，等待部署完成。

## 使用方法

### Web界面使用
1. 访问部署后的URL（如：https://your-project.vercel.app）
2. 输入邮箱地址或前缀（如：test123 或 test123@2925.com）
3. 点击"获取验证码"按钮
4. 系统会自动搜索并返回最新的验证码

### API直接调用
```bash
# GET请求
curl "https://your-project.vercel.app/api/get-verification?email=test123&time_window=10&max_retries=3"

# POST请求
curl -X POST "https://your-project.vercel.app/api/get-verification" \
  -H "Content-Type: application/json" \
  -d '{"email": "test123", "time_window": 10, "max_retries": 3}'
```

## API接口

### GET /api/get-verification

**参数：**
- `email`: 邮箱地址或前缀（必需）
- `time_window`: 时间窗口（分钟，默认10）
- `max_retries`: 最大重试次数（默认3）
- `retry_interval`: 重试间隔（秒，默认20）

**成功返回：**
```json
{
  "success": true,
  "verification_code": "123456",
  "email": "test123",
  "timestamp": "2025-01-20T10:30:00",
  "message": "验证码获取成功"
}
```

**失败返回：**
```json
{
  "success": false,
  "verification_code": null,
  "email": "test123",
  "timestamp": "2025-01-20T10:30:00",
  "message": "未找到验证码，请确认邮箱地址正确且验证码邮件已发送"
}
```

## 故障排除

### 常见问题

1. **Token过期（已自动处理）**
   - ✅ **自动解决**：系统会自动检测token过期并重新登录获取新token
   - 症状：API返回401错误时会自动重试
   - 手动解决：如果自动刷新失败，可更新`simple_verification.py`中的登录信息

2. **找不到验证码**
   - 症状：返回"未找到验证码"
   - 检查：邮箱地址是否正确，验证码邮件是否已发送
   - 调整：增加`time_window`参数值

3. **自动登录失败**
   - 症状：日志显示"Token自动更新失败"
   - 检查：登录信息（用户名、密码、RSA密码）是否正确
   - 解决：更新`simple_verification.py`中的`USERNAME`、`PASSWORD`、`RSA_PASSWORD`

4. **部署失败**
   - 检查：`requirements.txt`文件是否存在
   - 检查：Python版本是否兼容（推荐3.9+）
   - 检查：文件路径是否正确

### 日志查看

在Vercel控制台的Functions标签页可以查看API调用日志，用于调试问题。

## 技术说明

- **运行环境**: Python 3.9+ (Vercel Serverless)
- **依赖**: requests库
- **架构**: 无服务器函数 + 静态前端
- **数据源**: 2925.com邮件服务API
