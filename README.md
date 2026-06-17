# OmniAgent TUI

A terminal user interface for AI Agent interaction, built with [Textual](https://textual.textualize.io/).

![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue)
![Textual](https://img.shields.io/badge/textual-%3E%3D0.30.0-orange)

## Features

- **Chat interface** — RichLog-based message display with user/assistant color coding
- **Model selector** — Switch between AI models via custom overlay dropdown
- **Plan / Build mode** — Toggle between Plan (hides approval) and Build (shows approval)
- **Thinking level** — Low / Medium / High / Max
- **Approval level** — Ask for approval / Approve for me / Full access
- **Project management** — Sidebar with project tree, per-project chat history, and orphan chats
- **Project picker** — Bottom bar dropdown with search
- **New Chat** — Reset to welcome screen at any time
- **Settings modal** — Placeholder for future configuration
- **Dark theme** — Centralized via `theme.py` (`string.Template`-based CSS)

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/agent-tui.git
cd agent-tui

# Create virtual environment (recommended)
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# Install
pip install .
```

## Usage

```bash
agent-tui
```

Or run directly:

```bash
python -m agent_tui
```

### Controls

| Key | Action |
|-----|--------|
| `Esc` | Close sidebar / dismiss modal |
| `☰` (top-left) | Toggle sidebar |
| `Enter` | Send message |

## Project Structure

```
agent_tui/
├── __init__.py
├── __main__.py          # Entry point
├── app.py               # Main app layout & orchestration
├── data.py              # Static data (models, projects, chats)
├── theme.py             # Centralized CSS variables via render_css()
└── widgets/
    ├── __init__.py
    ├── chat_input.py    # Input bar with dropdowns and HalfRowSpacer
    ├── chat_view.py     # Message display (RichLog)
    ├── file_modal.py    # File path input modal
    ├── project_picker.py# Project selector dropdown
    ├── settings.py      # Settings modal (placeholder)
    └── sidebar.py       # Left panel with project/chats tree
```

## Development

```bash
# Install in editable mode
pip install -e .

# Dependencies
# textual>=0.30.0, rich>=13.0.0
```

## License

MIT
