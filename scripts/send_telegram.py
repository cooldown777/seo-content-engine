#!/usr/bin/env python3
"""Send queue/<date>/ to Telegram for manual review + posting.
Needs env: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID.
Sends: review note -> slides as one album (documents = full 1080x1440 quality) -> caption (copy-ready)."""
import json, os, sys, pathlib, requests

ROOT = pathlib.Path(__file__).resolve().parent.parent

def call(method, files=None, **data):
    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/{method}"
    r = requests.post(url, data=data, files=files, timeout=120)
    if r.status_code >= 400 or not r.json().get("ok"):
        sys.exit(f"Telegram API error {r.status_code}: {r.text}")
    return r.json()

def read(p):
    return p.read_text(encoding="utf-8").strip() if p.exists() else ""

def main(folder):
    folder = ROOT / folder
    chat = os.environ["TELEGRAM_CHAT_ID"]
    jpgs = sorted((folder / "slides").glob("*.jpg"))[:10]
    if len(jpgs) < 2:
        sys.exit("need 2–10 JPG slides")

    review = read(folder / "review.md")
    alt = read(folder / "alt.txt")
    head = f"📸 New carousel: {folder.name}\n\n{review}"
    if alt:
        head += f"\n\nAlt text: {alt}"
    call("sendMessage", chat_id=chat, text=head[:4096], disable_web_page_preview="true")

    media = [{"type": "document", "media": f"attach://s{i}"} for i in range(len(jpgs))]
    files = {f"s{i}": (j.name, j.open("rb"), "image/jpeg") for i, j in enumerate(jpgs)}
    call("sendMediaGroup", files=files, chat_id=chat, media=json.dumps(media))

    call("sendMessage", chat_id=chat, text=read(folder / "caption.txt")[:4096])
    print("sent", folder.name, len(jpgs), "slides")

if __name__ == "__main__":
    main(sys.argv[1])
