---
name: taobao-coin11-help
description: 从淘金币双11助力 API 获取待处理链接，借助局域网 Safari 页面把完整 raw_text 复制到 iPhone 剪贴板，在淘宝完成助力并回写完成状态。用于 iPhone 镜像下的淘金币互助自动化。
---

# 淘金币双11自动助力

使用 Mac「iPhone 镜像」和 `mcp__cua_repl.js`，循环处理当天 API 返回的待助力链接。流程的关键是不改写 `raw_text`：Safari 页面负责把原文放进 **iPhone 自己的剪贴板**，淘宝再读取它。

## API 与服务

先读取 [API 与网页服务参考](references/api-workflow.md)。API 默认与 NoneBot 共用端口：

- `GET /api/tb_coin11_help/links`：只返回当天未完成记录。
- `POST /api/tb_coin11_help/links/complete`：用 `{"id": <id>}` 或 `{"url": "..."}` 标记完成。

令牌存在时，对两个请求都加 `Authorization: Bearer $ONEBOT_ACCESS_TOKEN`。不要把令牌放进 Safari URL、页面内容或日志。

在 Mac 上启动随 skill 提供的网页服务：

```bash
ONEBOT_ACCESS_TOKEN="$ONEBOT_ACCESS_TOKEN" \
TB_HELP_API="http://127.0.0.1:7689" \
TB_HELP_PORT=8765 \
python3 taobao-coin11-help/scripts/tb_help_server.py
```

服务绑定 `0.0.0.0`，让 iPhone 使用 Mac 的局域网 IP 访问 `http://<mac-ip>:8765/`。若端口被防火墙或策略阻断，先确认 Mac 与 iPhone 在同一局域网、服务确实监听该地址，再请用户在 Safari 手动打开页面；不要把 API 端口暴露给手机来代替网页服务。

## 每条链接的操作

1. GET 待处理列表，保存 `id`、`url` 和完整 `raw_text`。不要 trim、规范化空格、替换 emoji、拆分淘口令或只复制 URL。
2. 在 Safari 打开网页，点击对应记录的“复制完整 raw_text”。只有页面出现“已复制完整文本”后才继续。页面中的 `<textarea>` 用于人工核对，复制按钮使用 `execCommand('copy')`，并以 `navigator.clipboard` 作回退。
3. 从 Safari 切到淘宝并保持在淘宝首页。首次出现“淘宝想从 Safari 浏览器粘贴”时选择“允许粘贴”，这是让淘宝读取刚才的 iPhone 剪贴板；不要用 Mac 端 `paste()` 把 raw_text 直接注入淘宝。
4. 等待淘宝识别淘口令弹窗。确认弹窗中的链接或分享者与当前记录相符，再点击“查看详情”，随后点击“帮ta助力”。若按钮点击后仍停留在详情页，重新观察一次并只重试这一个点击，不要重复复制或提交完成状态。
5. 以可见成功证据为准：助力页回到活动／商品页并出现“奖励已发放”“已得600”等明确提示，或出现助力完成状态。仅看到页面跳转、弹窗消失或加载结束不能算成功。
6. 成功后立即 POST 当前记录的 `id`。POST 返回成功后再 GET；只有记录从待处理列表消失才把它计入完成数。
7. 回到 Safari 处理下一条。每轮都重新 GET，直到 `count: 0`；列表为空时停止，不重复处理历史记录。

## 镜像操作要点

- 首次使用先读取 `mcp__cua_repl` 返回的文档，并用 `cua.getApp('com.apple.ScreenContinuity')` 获取镜像窗口。每次坐标操作前用最新截图定位。
- `phone.typeText()` 通过 Mac 键盘事件发送内容，实测会丢失中文、emoji、`₴` 及长 URL 中的标点。它只适合输入短 ASCII 辅助内容，不能用来输入 `raw_text`。
- Safari 网页复制是稳定路径：复制发生在 iPhone 上，淘宝读取的是 iPhone 剪贴板，能保留中文、emoji、特殊符号和原始空格。
- 如果必须由 AI 输入服务地址，先尝试输入纯 IP，让 Safari 的历史／自动完成补上带端口的地址；复杂 URL 输入失败时请用户手动打开页面。不要在淘宝搜索框里拼接被破坏的文本。
- 淘宝可能先显示首页，再延迟弹出助力卡片。观察到首页后再等一次；出现卡片后按当前页面按钮操作。
- 任何助力失败、链接不匹配、API POST 失败或成功证据不明确，都不要 POST 完成；记录原因并继续 GET 检查其余链接。

## 停止与报告

报告处理总数、成功数、跳过数及每条失败原因。若 API 不可达、服务无法被 iPhone 访问、镜像控制失效或淘宝要求验证码／登录／额外权限，停止相关分支并请求用户处理，不循环重试。

