from __future__ import annotations

MODELS: list[tuple[str, str]] = [
    ("Claude 3.5 Sonnet", "claude-3.5-sonnet"),
    ("GPT-4o", "gpt-4o"),
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
PROJECT_LOGO = """
[#fab283 bold]
█▀▀█ █▄▄█ █▀▀█ ▀▜▛▀ █▀▀█ █▀▀▀ █▀▀▀ █▀▀█ ▀▜▛▀
█  █ █  █ █  █  ▐▌  █▀▀█ █  █ █▀▀▀ █  █  ▐▌
▀▀▀▀ ▀  ▀ ▀  ▀ ▀▀▀▀ ▀  ▀ ▀▀▀▀ ▀▀▀▀ ▀  ▀  ▝▘
[/]
"""
