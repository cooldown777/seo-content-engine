#!/usr/bin/env python3
"""Publish queue/<date>/ as an Instagram carousel via the Instagram Graph API.
Needs env: IG_USER_ID, IG_ACCESS_TOKEN. Images must be public JPEGs (raw GitHub URLs of main)."""
import json, os, sys, time, pathlib, requests

API = "https://graph.facebook.com/v23.0"
ROOT = pathlib.Path(__file__).resolve().parent.parent

def call(method, path, **params):
    params["access_token"] = os.environ["IG_ACCESS_TOKEN"]
    r = requests.request(method, f"{API}/{path}", data=params if method == "POST" else None,
                         params=params if method == "GET" else None, timeout=60)
    if r.status_code >= 400:
        sys.exit(f"Instagram API error {r.status_code}: {r.text}")
    return r.json()

def wait_ready(cid):
    for _ in range(30):
        if call("GET", cid, fields="status_code")["status_code"] == "FINISHED":
            return
        time.sleep(5)
    sys.exit(f"container {cid} not ready")

def main(folder):
    folder = ROOT / folder
    if (folder / ".published").exists():
        print("already published"); return
    cfg = json.loads((ROOT / "config.json").read_text())
    base = cfg["github_raw_base"].rstrip("/")
    jpgs = sorted((folder / "slides").glob("*.jpg"))[:10]
    if len(jpgs) < 2:
        sys.exit("need 2–10 JPG slides")
    caption = (folder / "caption.txt").read_text(encoding="utf-8").strip()
    uid = os.environ["IG_USER_ID"]
    children = []
    for j in jpgs:
        url = f"{base}/{j.relative_to(ROOT).as_posix()}"
        cid = call("POST", f"{uid}/media", image_url=url, is_carousel_item="true")["id"]
        wait_ready(cid); children.append(cid)
    parent = call("POST", f"{uid}/media", media_type="CAROUSEL",
                  children=",".join(children), caption=caption)["id"]
    wait_ready(parent)
    media = call("POST", f"{uid}/media_publish", creation_id=parent)["id"]
    (folder / ".published").write_text(media)
    print("published", media)

if __name__ == "__main__":
    main(sys.argv[1])
