# 2925邮件验证码服务 - Vercel部署完整指南

## 📁 项目结构

```
vercel-deploy/
├── 📄 README.md                    # 项目说明文档
├── 📄 DEPLOYMENT_GUIDE.md          # 部署指南（本文件）
├── 📄 vercel.json                  # Vercel配置文件
├── 📄 requirements.txt             # Python依赖
├── 📄 test_local.py                # 本地测试脚本
├── � test_token_refresh.py        # Token自动刷新测试脚本
├── �📁 api/                         # Vercel API函数
│   └── 📄 get-verification.py      # 验证码获取API
├── 📁 public/                      # 静态前端文件
│   └── 📄 index.html              # Web界面
├── 📁 core/                        # 核心功能模块
│   ├── 📄 simple_verification.py   # 简化版验证码获取（推荐）
│   ├── 📄 verification.py          # 完整版验证码获取
│   └── 📄 mail_api.py              # 邮件API封装
└── 📁 config/                      # 配置文件
    └── 📄 settings.py              # 基础配置
```

## 🚀 快速部署步骤

### 1. 准备工作
- [x] 确保有GitHub账号
- [x] 确保有Vercel账号
- [x] 准备好2925.com的有效token

### 2. 上传到GitHub
```bash
# 方法1: 直接上传vercel-deploy文件夹到GitHub仓库

# 方法2: 使用Git命令
git add 2925/vercel-deploy/
git commit -m "Add Vercel deployment for email verification service"
git push origin main
```

### 3. Vercel部署配置
1. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 "New Project"
3. 选择你的GitHub仓库
4. 配置项目设置：
   - **Project Name**: `email-verification-service` (或自定义)
   - **Framework Preset**: `Other`
   - **Root Directory**: `2925/vercel-deploy`
   - **Build Command**: 留空
   - **Output Directory**: 留空
   - **Install Command**: `pip install -r requirements.txt`

### 4. 部署
点击 "Deploy" 按钮，等待部署完成（通常1-3分钟）。

## 🔧 配置说明

### Token配置

**🔄 自动Token刷新（推荐）**
系统已内置自动token刷新功能：
- 当检测到token过期（401错误）时，自动重新登录获取新token
- 无需手动维护token，大大降低维护成本
- 登录信息已预配置，开箱即用

**手动Token配置（可选）**
如需更新登录信息：

1. **修改登录信息**
   编辑 `core/simple_verification.py` 中的：
   - `USERNAME`: 用户名
   - `PASSWORD`: 密码
   - `RSA_PASSWORD`: RSA加密密码

2. **环境变量方式**
   在Vercel项目设置中添加环境变量：
   - `MAIL_TOKEN`: 手动指定token（会跳过自动刷新）

### 参数调优
可以在API调用时调整以下参数：
- `time_window`: 搜索时间窗口（分钟，默认10）
- `max_retries`: 最大重试次数（默认3）
- `retry_interval`: 重试间隔（秒，默认20）

## 🧪 测试验证

### 本地测试
```bash
cd 2925/vercel-deploy

# 基础功能测试
python test_local.py

# Token自动刷新功能测试
python test_token_refresh.py
```

### 部署后测试
1. **Web界面测试**
   - 访问: `https://your-project.vercel.app`
   - 输入邮箱地址或前缀
   - 点击"获取验证码"

2. **API测试**
   ```bash
   # GET请求测试
   curl "https://your-project.vercel.app/api/get-verification?email=test123"
   
   # POST请求测试
   curl -X POST "https://your-project.vercel.app/api/get-verification" \
     -H "Content-Type: application/json" \
     -d '{"email": "test123"}'
   ```

## 📊 使用统计

### API响应格式
```json
{
  "success": true,
  "verification_code": "123456",
  "email": "test123",
  "timestamp": "2025-01-20T10:30:00",
  "message": "验证码获取成功"
}
```

### 性能指标
- **冷启动时间**: ~2-5秒
- **热启动时间**: ~500ms
- **超时设置**: 30秒
- **并发支持**: Vercel默认限制

## 🔍 故障排除

### 常见错误及解决方案

1. **"Import error"**
   - 检查文件路径是否正确
   - 确认所有必需文件都已上传

2. **"Token无效"**
   - 更新 `simple_verification.py` 中的token
   - 或设置环境变量 `MAIL_TOKEN`

3. **"未找到验证码"**
   - 确认邮箱地址正确
   - 确认验证码邮件已发送
   - 增加 `time_window` 参数

4. **"部署失败"**
   - 检查 `requirements.txt` 文件
   - 确认Python版本兼容性
   - 查看Vercel部署日志

### 日志查看
- Vercel Dashboard → 项目 → Functions 标签页
- 实时查看API调用日志和错误信息

## 🔄 维护更新

### Token更新
当2925.com的token过期时：
1. 使用2925目录中的 `login_2925.py` 获取新token
2. 更新 `simple_verification.py` 中的 `CURRENT_TOKEN`
3. 重新部署或设置环境变量

### 功能扩展
- 添加更多邮件服务支持
- 增加验证码格式识别
- 添加缓存机制
- 增加用户认证

## 📞 技术支持

如遇到问题，请检查：
1. Vercel部署日志
2. API响应错误信息
3. 本地测试结果
4. Token有效性

---

**部署完成后，你将拥有一个完全可用的邮件验证码获取服务！** 🎉
