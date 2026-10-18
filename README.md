# iPhone Use · 淘宝双11赚能量

通过 Mac「iPhone 镜像」，引导 AI 完成淘宝「淘金币双11狂享20亿」活动中的赚能量任务。

本项目提供一个 Codex skill：**`taobao-coin11-energy`**。它将实机探索得到的操作流程、到账判断和故障恢复方法整理为可复用指引，供具备原生应用操作能力的 AI 使用。

## 能做什么

- 按当前任务要求和页面结构识别任务，适应名称、顺序、次数上限变化。
- 处理商品浏览、搜索、拍立淘、活动答题，以及淘宝内部和支付宝的浏览跳转任务。
- 按预计收益与完整耗时选择任务，减少重复截图、无效等待和失败重试。
- 核验单次能量及累计任务奖励，区分已到账、待刷新和受阻状态。
- 处理商品详情页的「搜同款」截图弹层，避免关闭与截图反复循环。

这是操作指引型 skill，依赖 AI 所在环境的工具完成操作；仓库不包含独立运行的手机自动化程序，也不会安装控制工具或配置系统权限。

## 使用前提

1. Mac 与 iPhone 支持并已连接「iPhone 镜像」，镜像窗口能够正常显示和操作手机。
2. Codex 环境提供 **`mcp__cua_repl.js`** 原生应用控制工具，并已允许访问「iPhone 镜像」。仅安装 skill 不会自动获得该工具或权限。
3. 根据系统提示完成必要的 macOS 屏幕录制、辅助功能等授权。
4. iPhone 上的淘宝已登录，能够进入对应双11活动；支付宝相关任务还需要可用的支付宝环境。

建议先手动进入「淘金币双11狂享20亿 → 赚能量 → 做任务赚能量」，再让 AI 开始。活动入口可能变化，skill 不依赖固定的首页坐标或深链。

## 安装

### 使用 npx 安装（推荐）

需要已安装 Node.js，并能使用 `npx`。将 skill 安装到 Codex 的个人目录：

```bash
npx skills add DDSRem-Dev/iPhone-Use-Taobao-Coin11-Skill --skill taobao-coin11-energy --agent codex --global
```

如需仅安装到当前项目，在目标项目目录执行并省略 `--global`：

```bash
npx skills add DDSRem-Dev/iPhone-Use-Taobao-Coin11-Skill --skill taobao-coin11-energy --agent codex
```

命令使用 [skills CLI](https://github.com/vercel-labs/skills)，按终端提示确认安装即可。

### 手动安装

克隆仓库：

```bash
git clone https://github.com/DDSRem-Dev/iPhone-Use-Taobao-Coin11-Skill.git
cd iPhone-Use-Taobao-Coin11-Skill
```

将完整 skill 文件夹复制到个人 skill 目录。若已有同名 skill，请先备份旧版本。

```bash
mkdir -p ~/.agents/skills
cp -R taobao-coin11-energy ~/.agents/skills/
cp LICENSE ~/.agents/skills/taobao-coin11-energy/LICENSE
```

安装后的入口应为：

```text
~/.agents/skills/taobao-coin11-energy/SKILL.md
```

也可以将整个 `taobao-coin11-energy` 文件夹放入目标项目的 `.agents/skills/`，用于该项目。请保留其中的 `agents/` 和 `references/`，并将仓库根目录的 `LICENSE` 一并复制到 skill 文件夹。

Codex 会自动发现 skill 变更；若列表没有更新，重启 Codex 后再检查。安装目录与发现方式参考 [OpenAI 官方 Build skills 文档](https://learn.chatgpt.com/docs/build-skills)。

## 使用

在 Codex 中选择「淘宝双11赚能量」skill，或在支持 `$` 提及的输入框中使用：

```text
$taobao-coin11-energy
帮我完成当前可执行的赚能量任务，优先选择耗时短、收益高的任务。
不要购买、抽奖或添加桌面小组件；受阻时跳过并说明原因。
最后汇报能量增量、累计奖励和未完成的任务。
```

也可以给出明确的时间或进度目标，例如：

```text
$taobao-coin11-energy
在接下来的 5 分钟内尽量获取能量，达到时间就停止。
```

运行时尽量避免同时操作手机。需要人工操作时，按 AI 的说明完成后告知它，以便重新识别当前画面。

## 操作中的关键点

### 商品详情页避免反复截图

本次实测中，读取商品详情画面可能触发淘宝截图检测并弹出「搜同款」；状态读取也可能产生同样副作用。

已验证的商品浏览流程是：**打开商品 → 按页面要求停留 → 返回列表 → 核验奖励**。详情停留期间不读取画面。若已出现弹层，连续执行「关闭 X → 商品返回」，中间不截图。

15 秒任务曾以 17 秒停留成功，但实际等待时间始终以当前任务要求为准。其他页面若已在计时或显示完成，无需额外进入商品。

### 完成入口跳转不等于到账

任务列表会重排、改名，奖励和计数也可能延迟更新。skill 使用明确的到账提示及刷新后的数值核验，不复用旧行号，不因数字暂未更新立即重做任务。

### 授权异常需要检查会话

如果出现 `Computer Use was not approved to use iPhone Mirroring`，先检查 Codex 的目标应用访问权限和 macOS 所需权限。本次曾在已授权、已手动连接后仍被拒绝，重启会话后恢复；这是一条实测恢复路径，不保证适用于所有环境。详见 [镜像连接与排障](taobao-coin11-energy/references/iphone-mirroring.md)。

## 已验证范围与限制

实机探索日期为 **2026-10-19**。已验证商品浏览、搜索、拍立淘、一道活动答题、多种淘宝与支付宝跳转任务，以及 5 次、20 次累计奖励。完整流程见 [任务参考](taobao-coin11-energy/references/task-flows.md)，证据和未验证项见 [探索记录](taobao-coin11-energy/references/verification.md)。

- 「惊喜好物」曾成功获得能量，但自动退出失败，需要用户帮助返回。
- 快手、微博曾进入下载引导页且未到账；已安装应用的正常打开路径可在实际环境中另行判断。
- 小组件任务保留手动步骤，未验证添加后的能量奖励。修改主屏布局前需要用户明确授权。
- 尚未逐项验证所有动态推广任务、所有次数上限、不同窗口尺寸，以及后续活动版本。
- 购买、付款、参与抽奖、邀请分享、开通服务和新增权限不会因出现在任务页面上而自动获得授权；浏览任务也不需要消耗能量升级赛车。

任务额度和完成条件以当前活动页面为准。实测记录用于指导操作，不代表固定收益或所有任务均能自动完成。

## 项目结构

```text
.
├── README.md
├── LICENSE
└── taobao-coin11-energy/
    ├── SKILL.md                    # AI 操作入口、分类与效率规则
    ├── agents/
    │   └── openai.yaml             # skill 显示信息
    └── references/
        ├── iphone-mirroring.md     # 连接、权限与工具排障
        ├── task-flows.md           # 各类任务的实测操作流程
        └── verification.md         # 探索证据与适用边界
```

## 许可证

本项目采用 [MIT License](LICENSE)，Copyright (c) 2026 DDSRem。
