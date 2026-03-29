#!/usr/bin/env python
"""
Google Calendar + Tasks MCP server (momokiako プロジェクト用)

ツール一覧:
  list_events(days=1)          - 今日から N 日分のカレンダー予定
  list_tasks(tasklist, max)    - Google Tasks の未完了タスク
  list_task_lists()            - タスクリスト名と ID の一覧

トークン保存先: ~/.claude/secrets/google_cal_tasks_token.json (リポジトリ外)
credentials:    環境変数 GOOGLE_CREDENTIALS_PATH (省略時: このファイルの2階層上の credentials.json)
"""

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from mcp.server.fastmcp import FastMCP

# ── スコープ ──────────────────────────────────────────────────────────────
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/tasks.readonly",
]

# ── パス解決 ──────────────────────────────────────────────────────────────
_here = Path(__file__).resolve()

CREDENTIALS_PATH = os.environ.get(
    "GOOGLE_CREDENTIALS_PATH",
    str(_here.parent.parent / "credentials.json"),
)
TOKEN_PATH = os.environ.get(
    "GOOGLE_TOKEN_PATH",
    str(Path.home() / ".claude" / "secrets" / "google_cal_tasks_token.json"),
)

# ── MCP サーバー初期化 ────────────────────────────────────────────────────
mcp = FastMCP("google-cal-tasks")


# ── 認証ヘルパー ──────────────────────────────────────────────────────────
def _get_credentials() -> Credentials:
    """トークンを読み込み、必要なら再認証する。"""
    creds = None
    token_path = Path(TOKEN_PATH)

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            # ブラウザを開いてローカルサーバーで受け取る
            creds = flow.run_local_server(port=0)
        # トークンを保存（ディレクトリがなければ作る）
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json(), encoding="utf-8")

    return creds


# ── ツール: カレンダー ────────────────────────────────────────────────────
@mcp.tool()
def list_events(days: int = 1) -> str:
    """
    今日から N 日分の Google カレンダー予定を取得する。

    Args:
        days: 取得する日数（1 = 今日のみ、7 = 今週分など）
    Returns:
        「・HH:MM タイトル」の形式で1件1行。予定がなければ「予定なし」。
    """
    creds = _get_credentials()
    service = build("calendar", "v3", credentials=creds)

    # タイムゾーン付きの今日0時
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    time_max = today_start + timedelta(days=days)

    result = service.events().list(
        calendarId="primary",
        timeMin=today_start.isoformat(),
        timeMax=time_max.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = result.get("items", [])
    if not events:
        return "予定なし"

    lines = []
    for ev in events:
        start_raw = ev["start"].get("dateTime", ev["start"].get("date", ""))
        title = ev.get("summary", "(タイトルなし)")
        if "T" in start_raw:
            dt = datetime.fromisoformat(start_raw)
            start_str = dt.strftime("%m/%d %H:%M")
        else:
            start_str = f"{start_raw}（終日）"
        lines.append(f"・{start_str}　{title}")

    return "\n".join(lines)


# ── ツール: タスク ────────────────────────────────────────────────────────
@mcp.tool()
def list_tasks(tasklist: str = "@default", max_results: int = 30) -> str:
    """
    Google Tasks の未完了タスクを取得する。

    Args:
        tasklist: タスクリスト ID（省略時は既定リスト @default）
        max_results: 最大取得件数（既定 30）
    Returns:
        「□ タイトル （期限: MM/DD）」の形式で1件1行。なければ「タスクなし」。
    """
    creds = _get_credentials()
    service = build("tasks", "v1", credentials=creds)

    result = service.tasks().list(
        tasklist=tasklist,
        showCompleted=False,
        maxResults=max_results,
    ).execute()

    items = result.get("items", [])
    if not items:
        return "タスクなし"

    lines = []
    for task in items:
        title = task.get("title", "(タイトルなし)")
        due = task.get("due", "")
        due_str = ""
        if due:
            dt = datetime.fromisoformat(due.replace("Z", "+00:00"))
            due_str = f"　（期限: {dt.strftime('%m/%d')}）"
        lines.append(f"□ {title}{due_str}")

    return "\n".join(lines)


@mcp.tool()
def list_task_lists() -> str:
    """
    Google Tasks のタスクリスト一覧を取得する。
    list_tasks の tasklist 引数に渡す ID を確認するために使う。
    """
    creds = _get_credentials()
    service = build("tasks", "v1", credentials=creds)

    result = service.tasklists().list(maxResults=20).execute()
    lists = result.get("items", [])
    if not lists:
        return "タスクリストなし"

    lines = [f"・{lst['title']}　（id: {lst['id']}）" for lst in lists]
    return "\n".join(lines)


# ── エントリーポイント ────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run()
