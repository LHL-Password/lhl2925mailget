# 📤 上传到 GitHub 仓库指南

## 🎯 目标仓库
```
https://github.com/LHL-Password/lhl2925mailget.git
```

## 📁 需要上传的文件

将 `vercel-deploy` 目录下的所有文件上传到 GitHub 仓库根目录：

```
GitHub仓库根目录/
├── 📄 README.md                    # 项目说明文档
├── 📄 DEPLOYMENT_GUIDE.md          # 部署指南
├── 📄 vercel.json                  # Vercel配置文件
├── 📄 requirements.txt             # Python依赖
├── 📄 test_local.py                # 本地测试脚本
├── 📄 test_token_refresh.py        # Token自动刷新测试脚本
├── 📄 UPLOAD_TO_GITHUB.md          # 本文件
├── 📁 api/                         # Vercel API函数
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

## 🚀 方法1: Web界面上传（推荐）

### 步骤1: 访问仓库
1. 打开浏览器，访问：https://github.com/LHL-Password/lhl2925mailget
2. 确保您已登录GitHub账号

### 步骤2: 上传文件
1. 点击 **"Add file"** 按钮
2. 选择 **"Upload files"**
3. 将 `vercel-deploy` 文件夹中的所有文件拖拽到上传区域
   - 可以选择所有文件一次性上传
   - 或者按文件夹分批上传

### 步骤3: 提交更改
1. 在页面底部添加提交信息：
   ```
   Add Vercel deployment for email verification service with auto token refresh
   ```
2. 可选：添加详细描述：
   ```
   - 支持邮箱验证码自动获取
   - 内置Token自动刷新功能
   - 包含Web界面和API接口
   - 适配Vercel无服务器部署
   ```
3. 点击 **"Commit changes"** 按钮

## 🔧 方法2: Git命令行

如果您熟悉Git命令，可以使用以下步骤：

### 步骤1: 克隆仓库
```bash
git clone https://github.com/LHL-Password/lhl2925mailget.git
cd lhl2925mailget
```

### 步骤2: 复制文件
```bash
# 将vercel-deploy目录下的所有文件复制到仓库根目录
# Windows PowerShell:
Copy-Item "D:\A-MyProject\augmentRegister\2925\vercel-deploy\*" -Destination "." -Recurse

# 或者手动复制文件
```

### 步骤3: 提交并推送
```bash
git add .
git commit -m "Add Vercel deployment for email verification service with auto token refresh"
git push origin main
```

## ✅ 上传完成后的验证

上传完成后，您的GitHub仓库应该包含以下文件：
- [x] README.md
- [x] DEPLOYMENT_GUIDE.md  
- [x] vercel.json
- [x] requirements.txt
- [x] api/get-verification.py
- [x] public/index.html
- [x] core/simple_verification.py
- [x] 其他所有文件...

## 🚀 下一步：Vercel部署

文件上传完成后，就可以在Vercel上部署了：

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 "New Project"
3. 选择您的GitHub仓库：`lhl2925mailget`
4. 配置设置：
   - **Framework Preset**: Other
   - **Root Directory**: `/` (根目录)
   - **Build Command**: 留空
   - **Output Directory**: 留空
   - **Install Command**: `pip install -r requirements.txt`
5. 点击 "Deploy"

## 🎉 部署成功

部署成功后，您将获得一个类似这样的URL：
```
https://lhl2925mailget.vercel.app
```

访问这个URL就可以使用邮件验证码获取服务了！

## 📞 需要帮助？

如果在上传过程中遇到问题，请检查：
- [x] GitHub账号是否有仓库的写入权限
- [x] 文件大小是否超过GitHub限制
- [x] 网络连接是否正常

---

**准备好上传了吗？按照上面的步骤操作即可！** 🚀
