# OmniAgent TUI

基于 [Textual](https://textual.textualize.io/) 构建的终端 AI Agent 交互界面。

![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue)
![Textual](https://img.shields.io/badge/textual-%3E%3D0.30.0-orange)

## 功能特性

- **聊天界面** — 基于 RichLog 的消息展示，用户/助手分色显示
- **模型选择** — 自定义覆盖下拉框切换 AI 模型
- **Plan / Build 模式** — Plan 模式隐藏审批选项，Build 模式显示
- **思考等级** — 低 / 中 / 高 / 最高
- **审批级别** — 请求审批 / 替我审批 / 完全访问
- **项目管理** — 侧边栏项目树、项目内对话历史与未分类对话
- **项目选择器** — 底栏下拉框，支持搜索过滤
- **新建对话** — 随时重置回欢迎页
- **设置弹窗** — 预留后续配置入口
- **深色主题** — 通过 `theme.py` 集中管理 CSS 变量

## 安装

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/agent-tui.git
cd agent-tui

# 创建虚拟环境（推荐）
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 安装
pip install .
```

## 使用

```bash
agent-tui
```

或直接运行：

```bash
python -m agent_tui
```

### 快捷键

| 按键 | 功能 |
|------|------|
| `Esc` | 关闭侧边栏 / 关闭弹窗 |
| `☰`（左上角） | 切换侧边栏 |
| `Enter` | 发送消息 |

## 项目结构

```
agent_tui/
├── __init__.py
├── __main__.py          # 入口
├── app.py               # 主布局与应用编排
├── data.py              # 静态数据（模型、项目、对话）
├── theme.py             # 集中式 CSS 变量
└── widgets/
    ├── __init__.py
    ├── chat_input.py    # 输入栏（下拉框 + HalfRowSpacer）
    ├── chat_view.py     # 消息展示（RichLog）
    ├── file_modal.py    # 文件路径输入弹窗
    ├── project_picker.py# 项目选择下拉框
    ├── settings.py      # 设置弹窗（占位）
    └── sidebar.py       # 左侧面板（项目/对话树）
```

## 开发

```bash
# 可编辑模式安装
pip install -e .

# 依赖
# textual>=0.30.0, rich>=13.0.0
```

## 许可证

[GNU General Public License v3.0](LICENSE)
