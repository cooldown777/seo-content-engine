#!/usr/bin/env python3
"""Save the owner's Telegram messages to the bot (links, notes, screenshots) as learnings.
Needs env: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID. Only messages from that chat are kept.
Writes research/inbox/YYYY-MM-DD.md (+ research/inbox/img/*.jpg) and research/inbox/.offset."""
import datetime, os, pathlib, re, sys, requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
INBOX = ROOT / "research" / "inbox"
OFFSET = INBOX / ".offset"
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT = str(os.environ["TELEGRAM_CHAT_ID"])
API = f"https://api.telegram.org/bot{TOKEN}"

def api(method, **params):
    r = requests.post(f"{API}/{method}", data=params, timeout=60)
    if r.status_code >= 400 or not r.json().get("ok"):
        sys.exit(f"Telegram API error {r.status_code}: {r.text}")
    return r.json()["result"]

def download(file_id, dest):
    path = api("getFile", file_id=file_id)["file_path"]
    r = requests.get(f"https://api.telegram.org/file/bot{TOKEN}/{path}", timeout=120)
    r.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(r.content)

def links(msg):
    text = msg.get("text") or msg.get("caption") or ""
    ents = msg.get("entities") or msg.get("caption_entities") or []
    urls = [e["url"] for e in ents if e.get("type") == "text_link"]
    urls += [text[e["offset"]:e["offset"] + e["length"]] for e in ents if e.get("type") == "url"]
    return list(dict.fromkeys(urls + re.findall(r"https?://\S+", text)))

def main():
    INBOX.mkdir(parents=True, exist_ok=True)
    offset = int(OFFSET.read_text()) if OFFSET.exists() else 0
    updates = api("getUpdates", offset=offset, timeout=0, allowed_updates='["message"]')
    saved = 0
    for u in updates:
        offset = u["update_id"] + 1
        msg = u.get("message")
        if not msg or str(msg["chat"]["id"]) != CHAT:
            continue  # ignore anyone who isn't the owner
        text = (msg.get("text") or msg.get("caption") or "").strip()
        if text.startswith("/"):
            continue  # bot commands like /start
        when = datetime.datetime.fromtimestamp(msg["date"], datetime.timezone.utc)
        day = when.strftime("%Y-%m-%d")
        entry = [f"## {when.strftime('%H:%M')} UTC · msg {msg['message_id']}"]
        if msg.get("forward_origin"):
            o = msg["forward_origin"]
            src = (o.get("chat") or {}).get("title") or (o.get("sender_user") or {}).get("username") or o.get("sender_user_name") or o.get("type")
            entry.append(f"Forwarded from: {src}")
        if text:
            entry.append("> " + text.replace("\n", "\n> "))
        for url in links(msg):
            entry.append(f"- link: {url}")
        media = None
        if msg.get("photo"):
            media = (msg["photo"][-1]["file_id"], ".jpg")
        elif msg.get("document", {}).get("mime_type", "").startswith("image/"):
            name = msg["document"].get("file_name", "image.jpg")
            media = (msg["document"]["file_id"], pathlib.Path(name).suffix or ".jpg")
        if media:
            img = INBOX / "img" / f"{day}_{msg['message_id']}{media[1]}"
            download(media[0], img)
            entry.append(f"- image: img/{img.name}")
        if len(entry) == 1:
            continue  # stickers, voice notes etc.
        f = INBOX / f"{day}.md"
        head = "" if f.exists() else f"# Owner inbox {day}\n\n"
        with f.open("a", encoding="utf-8") as fh:
            fh.write(head + "\n".join(entry) + "\n\n")
        saved += 1
        api("sendMessage", chat_id=CHAT, text="✅ Saved to learnings",
            reply_parameters=f'{{"message_id": {msg["message_id"]}}}')
    OFFSET.write_text(str(offset))
    print("saved", saved, "message(s)")

if __name__ == "__main__":
    main()
