# API 与网页服务参考

## API

API 与 NoneBot 共用端口，默认地址为 `http://<api-host>:7689`：

```text
GET  /api/tb_coin11_help/links
POST /api/tb_coin11_help/links/complete
```

配置 `ONEBOT_ACCESS_TOKEN` 后，请求头必须包含：

```text
Authorization: Bearer <ONEBOT_ACCESS_TOKEN>
```

GET 返回当天尚未完成的链接：

```json
{
  "day": "2026-10-19",
  "count": 1,
  "items": [
    {
      "id": 1,
      "day": "2026-10-19",
      "url": "https://m.tb.cn/h.j2hZCc4",
      "raw_text": "...",
      "completed_at": null
    }
  ]
}
```

完成确认支持记录 ID 或 URL：

```json
{"id": 1}
```

```json
{"url": "https://m.tb.cn/h.j2hZCc4"}
```

未配置令牌时 API 不校验 Authorization，适合本机或受控内网调试。服务端仍应绑定局域网可达地址，并避免把令牌写入 HTML。

## Safari 页面

`taobao-coin11-help/scripts/tb_help_server.py` 每次请求页面时重新 GET API，并为每条记录显示：

- 记录 ID 与链接地址；
- 原始 `raw_text` 的只读文本框；
- “复制完整 raw_text”按钮与复制结果状态。

按钮在 iPhone Safari 中运行 `document.execCommand('copy')`，失败时再尝试 `navigator.clipboard.writeText`。按钮传入 JSON 编码的原文，因此不会由 HTML 转义改变内容。复制后必须看到页面状态“已复制完整文本”，再切换淘宝。

## 经过验证的闭环

2026-10-19 在同一局域网实测：

1. Mac 服务监听 `0.0.0.0:8765`，iPhone 用 `http://192.168.100.7:8765/` 打开页面。
2. Safari 点击第二条记录的复制按钮，显示“已复制完整文本”。
3. 切换淘宝，允许“从 Safari 浏览器粘贴”，等待助力卡片出现。
4. 点击“查看详情”→“帮ta助力”，页面显示“奖励已发放／已得600”。
5. 对两条记录分别 POST 完成，GET 最终返回 `count: 0`。

`phone.typeText(raw_text)` 会丢失中文、emoji 和特殊符号；不要把它作为复制方案。Safari 页面复制是本流程的必要环节。
