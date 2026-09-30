---
name: carousel
description: Turn one SEO topic into a rendered Instagram carousel (deck.json + slides + caption) for @makeseo.ai
---

# Carousel skill

## Templates available in render.py (1080×1440, dark system)
| type | fields | use |
|---|---|---|
| checkHook | eyebrow [2 lines, caps], title (use <br>, max ~13 chars/line, 3 lines), accentLine | slide 1 |
| checkItem | n, total, title (line 1, ≤16 chars), titleAccent (line 2, ≤16 chars), body (≤115 chars), action (≤95 chars), example (≤95 chars) | one point each |
| checkSummary | eyebrow, title, titleAccent, items [= one short line per point, ≤34 chars], seed (optional 1 line, may hint "an AI can do this") | second to last |
| darkCTA | eyebrow "BEFORE YOU GO", keyword, body "and I'll send you <promise>.", sub | always last |

Length limits matter: longer text overflows the layout. After rendering, open 2–3 PNGs and
check nothing overlaps or runs off the canvas; shorten and re-render if it does.

## Recipe
1. Topic → reduce to 4–7 concrete, checkable points (a list, steps or myths). Complete overview
   beats single tip.
2. Hook: concrete number + outcome, contains "SEO" (e.g. "5 SEO fixes for category pages").
3. Each checkItem: body = why it matters (named tool/brand where natural: Google, ChatGPT,
   Perplexity, Search Console, Shopify, WordPress), action = what to do today, example = one
   concrete, realistic example.
4. Exactly one accent element per slide (the template already handles it).
5. Summary: all points as short lines. CTA: keyword + promise from config.json.
6. `total` must equal the number of checkItems. Slide count 6–10.
7. Render, visually check, write caption/alt/sources/review, append to used-angles.md.
