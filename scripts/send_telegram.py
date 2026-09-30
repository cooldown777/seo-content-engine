#!/usr/bin/env python3
"""Send queue/<date>/ to Telegram for manual review + posting.
Needs env: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID.
Sends: review card -> slides as one album (documents = full 1080x1440 quality) -> caption (copy-ready)."""
import datetime, html, json, os, re, sys, pathlib, requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
ICONS = {"topic": "📝", "pillar": "🏛", "why today": "📅", "keyword": "🔑", "uncertain": "⚠️"}

def call(method, files=None, **data):
    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/{method}"
    r = requests.post(url, data=data, files=files, timeout=120)
    if r.status_code >= 400 or not r.json().get("ok"):
        sys.exit(f"Telegram API error {r.status_code}: {r.text}")
    return r.json()

def read(p):
    return p.read_text(encoding="utf-8").strip() if p.exists() else ""

def inline(text):
    """Escape for Telegram HTML, then turn **bold** and `code` into tags."""
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return re.sub(r"`(.+?)`", r"<code>\1</code>", t)

def card(folder):
    try:
        date = datetime.date.fromisoformat(folder.name).strftime("%a, %d %b %Y")
    except ValueError:
        date = folder.name
    deck = json.loads(read(folder / "deck.json") or "{}")
    hook = next((s for s in deck.get("slides", []) if s.get("type") == "checkHook"), {})
    title = re.sub(r"<br\s*/?>", " ", hook.get("title", "")).strip()

    lines = [f"📸 <b>New carousel</b> · {date}"]
    if title:
        lines += ["", f"<b>{html.escape(title)}</b>"]
    lines.append("")
    for raw in read(folder / "review.md").splitlines():
        raw = re.sub(r"^\s*(?:[-•]|\*(?!\*))\s*", "", raw).strip()
        m = re.match(r"\*\*(.+?):?\*\*:?\s*(.*)", raw)
        if m:
            key, val = m.group(1).strip().rstrip(":"), m.group(2)
            icon = ICONS.get(key.lower(), "•")
            lines.append(f"{icon} <b>{html.escape(key)}:</b> {inline(val)}")
        elif raw:
            lines.append(inline(raw))
    alt = read(folder / "alt.txt")
    if alt:
        lines += ["", "🖼 <b>Alt text</b> (Advanced settings → Accessibility)",
                  f"<blockquote expandable>{html.escape(alt)}</blockquote>"]
    parts = (["reel"] if (folder / "reel" / "script.md").exists() else []) + \
            ([f"{len(list((folder / 'slides').glob('*.jpg')))}-slide carousel"] if (folder / "slides").exists() else [])
    lines += ["", f"👇 Below: {' + '.join(parts)}. Captions come as separate messages: long-press → <b>Copy</b>"]
    return "\n".join(lines)

def label(chat, text):
    call("sendMessage", chat_id=chat, text=text, parse_mode="HTML")

def main(folder):
    folder = ROOT / str(folder).rstrip("/")
    chat = os.environ["TELEGRAM_CHAT_ID"]
    reel = folder / "reel"
    jpgs = sorted((folder / "slides").glob("*.jpg"))[:10]
    if not jpgs and not (reel / "script.md").exists():
        sys.exit(f"nothing to send in {folder}")

    call("sendMessage", chat_id=chat, text=card(folder)[:4096], parse_mode="HTML",
         link_preview_options=json.dumps({"is_disabled": True}))

    if (reel / "script.md").exists():
        video = reel / "video.mp4"
        if video.exists() and video.stat().st_size < 50_000_000:  # Bot API upload limit
            with video.open("rb") as v:
                call("sendVideo", files={"video": ("video.mp4", v, "video/mp4")}, chat_id=chat,
                     caption="🎬 Reel video", supports_streaming="true")
        label(chat, "🎬 <b>Reel script</b>")
        call("sendMessage", chat_id=chat, text=read(reel / "script.md")[:4096])
        label(chat, "🎬 <b>Reel caption</b> · long-press → Copy")
        call("sendMessage", chat_id=chat, text=read(reel / "caption.txt")[:4096] or "(no caption)")

    if jpgs:
        label(chat, f"🖼 <b>Carousel</b> · {len(jpgs)} slides")
        media = [{"type": "document", "media": f"attach://s{i}"} for i in range(len(jpgs))]
        files = {f"s{i}": (j.name, j.open("rb"), "image/jpeg") for i, j in enumerate(jpgs)}
        call("sendMediaGroup", files=files, chat_id=chat, media=json.dumps(media))
        label(chat, "🖼 <b>Carousel caption</b> · long-press → Copy")
        call("sendMessage", chat_id=chat, text=read(folder / "caption.txt")[:4096])
    print("sent", folder.name, "reel" if (reel / "script.md").exists() else "", len(jpgs), "slides")

if __name__ == "__main__":
    main(sys.argv[1])
