# 镜像连接与工具注意事项

## 前提与授权

- Mac 已打开「iPhone 镜像」，手机已连接且能显示当前画面；淘宝已登录。支付宝跳转任务另依赖可用的支付宝环境。
- Codex 的应用访问授权与 macOS「屏幕录制／辅助功能」权限是不同层。遇到 `Computer Use was not approved to use iPhone Mirroring`，请用户在 Codex 应用访问设置中检查是否允许「iPhone 镜像」，并检查系统所需权限；只需处理目标应用的访问，不要求开放所有应用。不同版本的设置入口可能不同，不编造菜单路径。
- 本次曾出现：用户已允许 Any App、手动打开镜像，仍被拒绝且没有授权弹窗；**用户重启会话后才恢复**。这是实测恢复方式，不证明唯一原因，也不保证每次有效。授权看似已开启却仍失败时，向用户说明原始错误，建议重新开启会话再试一次。
- 用户操作镜像后，要刷新状态再继续。不要把所有异常归因于用户同时操作；本次截图循环发生时用户明确没有操作。

相关资料（排障时再查，不必每轮联网）：

- [OpenAI Computer Use 文档](https://learn.chatgpt.com/docs/computer-use)
- [应用可枚举但控制被拒绝的同类报告 #18896](https://github.com/openai/codex/issues/18896)
- [旧会话与新会话授权差异报告 #18522](https://github.com/openai/codex/issues/18522)

这些 issue 是相似故障报告，不是已确认的修复说明。

## 绑定与观察

首次工具调用遵守 `mcp__cua_repl` 的初始化规则。例如只执行：

```javascript
var phone = await cua.getApp('com.apple.ScreenContinuity');
```

读取工具返回的 API 文档再调用其他方法。上下文压缩后若工具要求恢复文档，先调用 `await cua.rewriteDocumentation()`。所有原生 UI 操作使用此工具，不用 AppleScript、其他输入库或 shell 模拟鼠标。

- `phone.getAXStateAndScreenshot()`：在任务列表、加载后的列表及跨应用目标页识别内容；一次调用已同时读取状态与画面，通常不再紧接着单独读取AX或截图。
- `phone.click([x,y])`：坐标按最新截图和当前窗口定位；不是手机原生分辨率坐标。
- `phone.scroll([x,y], 'down', distance)`：用于滚动。Mac 接口的 distance 为页数，不把 600 当作 600 像素。需要像素时先确认当前平台文档支持。一次滚动无效就检查目标区域，不连续盲增距离。
- `phone.pressKey('super+1')`：镜像 Home；`super+2`：应用切换器。仅在确有导航需要时使用。
- 本次 AX 只暴露 Mac 外壳、菜单和窗口，不暴露 iOS 任务按钮。`There has been no change...` 不能说明手机画面没有变化；需要时以截图判断。
- 本次截图为 **638×1404**，无需把坐标除以二。移动窗口、缩放或分辨率变化后重新定位，禁止将此尺寸当作固定前提。
- 工具观察自带等待。对加载中/过渡动画可再次观察，勿用固定长睡眠等待所有页面。真正的任务停留按页面规定计时；有可见倒计时则使用剩余时间，已完成则不补等。无倒计时的已验证商品流程，从进入详情起按要求时长加约1～2秒余量等待一次，不把工具开销预估为已完成时间；详情停留期间尤其不能截图。等待工具不存在时使用当前环境允许的等效计时方式，不能用反复截图充当计时器。

## 有限恢复

| 错误 | 处理 |
| --- | --- |
| `Computer Use is not active ... first call get_app_state` | 刷新 `phone.getAXState()` 后重试一次；若在详情页，意识到这可能触发搜同款，按连续关闭流程退出 |
| `The user changed ... Re-query latest state` | 重新读取最新状态，再定位；详情同样考虑截图副作用 |
| 截图失败 `-10005` / `SCStreamErrorDomain -3812` | 本次重新 `cua.getApp('com.apple.ScreenContinuity')` 后恢复，可尝试一次 |
| 同一错误持续出现 | 停止该分支，报告错误与已做恢复，请用户检查连接或重开会话 |

不要通过不断截图证明商品弹层已关闭；详情页观察的副作用优先按主文件处理。
