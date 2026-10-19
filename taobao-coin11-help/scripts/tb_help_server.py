#!/usr/bin/env python3
"""Serve a LAN page for copying Taobao help raw_text on the iPhone."""

from __future__ import annotations

import html
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, urlopen

API_BASE = os.environ.get("TB_HELP_API", "http://127.0.0.1:7689").rstrip("/")
TOKEN = os.environ.get("ONEBOT_ACCESS_TOKEN", "")
PORT = int(os.environ.get("TB_HELP_PORT", "8765"))
HOST = os.environ.get("TB_HELP_HOST", "0.0.0.0")


def load_items() -> list[dict]:
    headers = {"Accept": "application/json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    request = Request(f"{API_BASE}/api/tb_coin11_help/links", headers=headers)
    with urlopen(request, timeout=10) as response:
        payload = json.load(response)
    return payload.get("items", [])


def page() -> bytes:
    items = load_items()
    cards: list[str] = []
    for item in items:
        raw = item.get("raw_text", "")
        raw_json = html.escape(json.dumps(raw, ensure_ascii=False), quote=True)
        cards.append(
            f"""<section class='card'>
<div class='meta'>ID {html.escape(str(item.get('id')))} · {html.escape(item.get('url', ''))}</div>
<textarea id='raw-{item.get('id')}' readonly>{html.escape(raw)}</textarea>
<button onclick='copyRaw({raw_json}, this)'>复制完整 raw_text</button>
<span class='status'></span>
</section>"""
        )
    body = "".join(cards) or "<p>当前没有待助力链接。</p>"
    document = f"""<!doctype html>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>淘金币双11助力</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,sans-serif;margin:16px;background:#f5f5f7;color:#111}}
h1{{font-size:22px}} .card{{background:white;border-radius:14px;padding:14px;margin:12px 0;box-shadow:0 1px 4px #ddd}}
.meta{{font-size:12px;color:#666;word-break:break-all;margin-bottom:8px}}
textarea{{width:100%;height:82px;font-size:16px;line-height:1.4;box-sizing:border-box}}
button{{margin-top:10px;background:#ff6200;color:#fff;border:0;border-radius:9px;padding:11px 14px;font-size:16px}}
.status{{margin-left:8px;color:#16803c}}
</style>
<h1>淘金币双11助力</h1>
<p>在 iPhone Safari 点对应按钮，确认显示“已复制”，再打开淘宝。</p>
{body}
<script>
async function copyRaw(text, button) {{
  const status = button.nextElementSibling;
  const ta = document.createElement('textarea');
  ta.value = text; ta.style.position='fixed'; ta.style.opacity='0';
  document.body.appendChild(ta); ta.focus(); ta.select();
  let ok = false;
  try {{ ok = document.execCommand('copy'); }} catch (e) {{}}
  if (!ok && navigator.clipboard) {{ try {{ await navigator.clipboard.writeText(text); ok = true; }} catch(e) {{}} }}
  ta.remove();
  status.textContent = ok ? '已复制完整文本' : '复制失败，请重试';
}}
</script>"""
    return document.encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        try:
            content = page()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as exc:  # pragma: no cover - diagnostic page
            content = f"助力链接读取失败：{html.escape(str(exc))}".encode()
            self.send_response(502)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

    def log_message(self, _format: str, *_args: object) -> None:
        return


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"serving on {HOST}:{PORT}", flush=True)
    server.serve_forever()
