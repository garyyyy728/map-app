# 代理配置指南

## 📍 为什么需要配置代理？

由于 Google Gemini API 在某些地区（包括中国大陆）存在访问限制，您可能会遇到以下错误：

```
400 FAILED_PRECONDITION
User location is not supported for the API use.
```

**解决方案：使用代理或 VPN 服务。**

---

## 🔧 配置步骤

### 方法 1: 使用系统代理工具

#### Windows 用户

1. **安装代理工具**（选择其中一个）：
   - Clash for Windows
   - V2rayN
   - Shadowsocks
   - 其他代理工具

2. **启动代理服务**
   
   确保代理工具正在运行，并记下 HTTP 端口号（通常显示在工具界面）

3. **在 `.env` 文件中添加代理配置**

   ```env
   # 常见配置示例
   
   # Clash (默认端口 7890)
   HTTP_PROXY=http://127.0.0.1:7890
   HTTPS_PROXY=http://127.0.0.1:7890
   
   # V2rayN (默认端口 10809)
   # HTTP_PROXY=http://127.0.0.1:10809
   # HTTPS_PROXY=http://127.0.0.1:10809
   
   # Shadowsocks (默认端口 1080)
   # HTTP_PROXY=http://127.0.0.1:1080
   # HTTPS_PROXY=http://127.0.0.1:1080
   ```

#### macOS/Linux 用户

1. **安装代理工具**（选择其中一个）：
   - ClashX / Clash for Linux
   - V2rayU / V2ray
   - Shadowsocks

2. **在 `.env` 文件中添加代理配置**

   ```env
   HTTP_PROXY=http://127.0.0.1:7890
   HTTPS_PROXY=http://127.0.0.1:7890
   ```

### 方法 2: 使用 VPN

如果您使用 VPN 服务（如 ExpressVPN、NordVPN 等）：

1. 连接 VPN 到支持的地区（美国、日本、新加坡等）
2. **不需要**在 `.env` 中配置代理
3. 直接启动服务即可

---

## 📝 完整的 .env 配置示例

```env
# Gemini API Configuration
GEMINI_API_KEY=AIzaSyAebsKqvJPLrt8FXZrYnRw28oLviH0jEtw

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Application Settings
DEBUG=True

# Proxy Configuration (根据您的实际代理工具配置)
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
```

---

## 🧪 测试代理配置

### 1. 验证代理是否工作

```bash
# Windows PowerShell
$env:HTTP_PROXY="http://127.0.0.1:7890"
$env:HTTPS_PROXY="http://127.0.0.1:7890"
curl https://www.google.com

# macOS/Linux
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
curl https://www.google.com
```

如果能访问 Google，说明代理配置正确。

### 2. 测试 Gemini API

启动服务后，运行测试：

```bash
python test_api.py
```

如果看到成功的响应，说明配置正确！

---

## 🔍 常见问题

### ❌ 问题 1: 仍然提示 "User location is not supported"

**原因：**
- 代理未正确配置
- 代理工具未启动
- 代理端口错误

**解决：**
1. 检查代理工具是否正在运行
2. 确认 `.env` 中的端口号与代理工具一致
3. 查看服务器日志，确认是否使用了代理

### ❌ 问题 2: 连接超时

**原因：**
- 代理服务器响应慢
- 网络不稳定

**解决：**
1. 切换代理节点（选择延迟更低的）
2. 增加超时时间
3. 检查代理工具的连接状态

### ❌ 问题 3: 代理认证失败

**原因：**
- 代理需要用户名和密码

**解决：**
在 `.env` 中使用完整的代理 URL：

```env
HTTP_PROXY=http://username:password@127.0.0.1:7890
HTTPS_PROXY=http://username:password@127.0.0.1:7890
```

---

## 🎯 推荐配置

### 开发环境（本地）

使用本地代理工具（Clash、V2ray 等）

**优点：**
- 简单易配置
- 响应速度快
- 免费

**推荐配置：**
```env
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
```

### 生产环境（服务器）

部署到国外云服务器（AWS、GCP、Azure 等）

**优点：**
- 无需代理
- 稳定可靠
- 延迟低

**推荐地区：**
- 美国（us-east-1, us-west-1）
- 日本（ap-northeast-1）
- 新加坡（ap-southeast-1）
- 欧洲（eu-west-1）

---

## 📊 代理工具对比

| 工具 | 平台 | 默认端口 | 难度 | 推荐度 |
|------|------|----------|------|--------|
| Clash for Windows | Windows | 7890 | ⭐ | ⭐⭐⭐⭐⭐ |
| ClashX | macOS | 7890 | ⭐ | ⭐⭐⭐⭐⭐ |
| V2rayN | Windows | 10809 | ⭐⭐ | ⭐⭐⭐⭐ |
| V2rayU | macOS | 1080 | ⭐⭐ | ⭐⭐⭐⭐ |
| Shadowsocks | All | 1080 | ⭐ | ⭐⭐⭐ |

---

## ✅ 检查清单

配置完成后，请确认：

- [ ] 代理工具已安装并运行
- [ ] `.env` 文件包含正确的代理配置
- [ ] 代理端口号与工具配置一致
- [ ] 可以访问 Google 等外网站点
- [ ] 测试脚本运行成功
- [ ] API 返回正常响应

---

## 🌐 支持的地区

以下地区可以**直接访问** Gemini API（无需代理）：

✅ 美国、加拿大
✅ 日本、韩国、新加坡
✅ 欧洲大部分国家
✅ 澳大利亚、新西兰

❌ 以下地区**需要代理**：

❌ 中国大陆
❌ 部分中东国家
❌ 部分非洲国家

---

## 💡 提示

1. **选择合适的代理节点**
   - 优先选择延迟低的节点
   - 美国、日本、新加坡节点通常效果较好

2. **保持代理稳定**
   - 确保代理工具持续运行
   - 定期检查连接状态

3. **安全提示**
   - 不要在代码中硬编码代理信息
   - 定期更换代理节点
   - 使用可信的代理服务

---

**配置代理后，您就可以正常使用 Gemini API 了！** 🎉

如有问题，请参考 `TROUBLESHOOTING.md` 获取更多帮助。

