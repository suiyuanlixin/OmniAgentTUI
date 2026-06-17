from __future__ import annotations

from agent_tui.theme import TEXT_MUTED, TEXT_PRIMARY

MODELS: list[tuple[str, str]] = [
    ("GPT 5.5 Instant", "gpt-5-5-instant"),
    ("Claude Fable 5", "claude-fable-5"),
    ("Gemini 3.5 Pro", "gemini-3-5-pro"),
    ("Grok V9 Medium", "grok-v9-medium"),
    ("DeepSeek V4 Pro", "deepseek-v4-pro"),
    ("Qwen 3.7 Max", "qwen-3-7-max"),
    ("GLM 5.2", "glm-5-2"),
    ("Kimi K2.7 Code", "kimi-k2-7-code"),
    ("MiniMax M3", "minimax-m3"),
    ("Step 3.7 Flash", "step-3-7-flash"),
]

THINKING_LEVELS: list[tuple[str, str]] = [
    ("Low", "low"),
    ("Medium", "medium"),
    ("High", "high"),
    ("Max", "max"),
]

APPROVAL_LEVELS: list[tuple[str, str]] = [
    ("Ask for approval", "ask"),
    ("Approve for me", "approve"),
    ("Full access", "full"),
]

PROJECTS: list[str] = [
    "my-agent-project",
    "web-scraper",
    "data-analyzer",
    "api-server",
    "ml-pipeline",
    "chatbot-service",
    "devops-tools",
]

SAMPLE_CHATS: dict[str, list[str]] = {
    "my-agent-project": ["Debug token limit", "Add streaming support", "Initial setup"],
    "web-scraper": ["Fix pagination bug", "Add proxy rotation"],
    "data-analyzer": ["Optimize queries", "Add chart export"],
    "api-server": ["Rate limiting", "Auth middleware", "Health check endpoint"],
    "ml-pipeline": ["Model evaluation", "Data preprocessing", "Pipeline config"],
}

ORPHAN_CHATS: list[str] = [
    "Quick Python question",
    "Bash script help",
    "Code review notes",
]

PROJECT_NAME = "OmniAgent"
PROJECT_LOGO = (
    f"[{TEXT_MUTED} bold]█▀▀█ █▄▄█ █▀▀█ ▀▜▛▀[/][{TEXT_PRIMARY} bold] █▀▀█ █▀▀▀ █▀▀▀ █▀▀█ ▀▜▛▀[/]\n"
    f"[{TEXT_MUTED} bold]█  █ █  █ █  █  ▐▌ [/][{TEXT_PRIMARY} bold] █▀▀█ █  █ █▀▀▀ █  █  ▐▌ [/]\n"
    f"[{TEXT_MUTED} bold]▀▀▀▀ ▀  ▀ ▀  ▀ ▀▀▀▀[/][{TEXT_PRIMARY} bold] ▀  ▀ ▀▀▀▀ ▀▀▀▀ ▀  ▀  ▝▘ [/]"
)
