# seo-content-engine – rules for every Claude session

This repo produces Instagram carousels for the account @makeseo.ai. Read this file,
`docs/content-blueprint.md` (Part B = slideshows) and `.claude/skills/carousel/SKILL.md`
before creating anything. All content is written in **English**.

## Hard rules (never break)
1. **Voice:** a tech creator who found useful SEO knowledge/tools and shares them on request.
   Never "my / mine / our / we built / I built / I made". Never "my checklist/template/tool".
2. **Product:** never name, describe, price or pitch the product. The handle @makeseo.ai is the
   only place the name appears (footer + follow line + caption signature).
3. **Keyword:** only keywords listed in `config.json → approved_keywords`, spelled exactly as listed.
   The promise text must match the listed promise (= what the DM delivers). Never invent keywords
   or lead magnets.
4. **Facts:** never invent traffic numbers, case studies or results. Hedge market claims
   ("often", "usually", "can"). Every factual/news claim gets a source URL in `sources.md`.
   If a news item cannot be verified from a primary source (Google Search Central, official
   docs, OpenAI/Perplexity announcements), do not use it.
5. **No repeats:** check `used-angles.md`; do not reuse an angle from the last 60 days.
6. **Hooks:** contain the word "SEO", never the word "blog".
7. **Design:** only through `render.py` templates and `config.json`. Never hand-edit PNGs.

## Pillars (rotate, see blueprint section 3)
1 Content volume · 2 Internal linking · 3 AI search/GEO · 4 E-commerce SEO · 5 On-page craft ·
6 Myths & change · 7 Cost comparison (principle only)

## Output per piece: `queue/YYYY-MM-DD/`
- `deck.json`   – slides for render.py (no brand block; brand comes from config.json)
- `slides/`     – rendered PNG + JPG (created by `python3 render.py queue/<date>/deck.json`)
- `caption.txt` – line 1 = "Comment KEYWORD and I'll send you PROMISE.", then "Slide 1 is…",
                  3–6 short prose paragraphs, 5–8 hashtags. Max 2,200 characters.
- `alt.txt`     – one sentence
- `sources.md`  – every factual claim with URL
- `review.md`   – 5 lines for the human reviewer (read on a phone in Telegram), each
                  `- **Key:** value`, max ~120 chars: Topic, Pillar, Why today, Keyword, Uncertain

## Review & publishing
Push the finished piece on branch `content/YYYY-MM-DD`. The GitHub Action `review.yml` sends
slides + caption to the owner on Telegram and merges the branch into `main`. The owner posts
manually on Instagram. Claude never publishes itself and never touches secrets.
