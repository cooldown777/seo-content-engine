Daily content routine for @makeseo.ai. Follow CLAUDE.md and the reel + carousel skills exactly.
Today's date decides the folder: queue/<YYYY-MM-DD>/.

1. CONTEXT
   Read CLAUDE.md, config.json, used-angles.md, docs/competitor-ads-blueprint.md and the latest
   research/accounts/patterns.md plus the newest scan files in research/accounts/.
   Read research/learnings.md and every research/inbox/*.md from the last 14 days (open the
   images they reference). Apply the owner's feedback; add any durable lesson as one dated line
   to research/learnings.md. Note which pillar was used least recently,
   whether a carousel is due (newest CAROUSEL entry ≥ carousel_every_days old) and how many
   pillar-8 (AI radar) pieces were posted in the last 7 days (max 2).

2. AI RADAR (last `ai_radar_lookback_days` days, primary sources only)
   Check for new releases or major updates from:
   - Anthropic: anthropic.com/news, Claude / Claude Code release notes (models, skills, tools)
   - OpenAI: openai.com/news, GPT model releases, ChatGPT search, Codex changelog
   - Google: blog.google, Gemini releases, AI Mode, AI Overviews,
     developers.google.com/search/blog
   - Perplexity: perplexity.ai/hub
   - AI tools that @borja.obeso or @lawrenceaiseo featured in the latest scans (e.g. Jev):
     verify each on its official site before using it
   For each hit record: official name, date, what changed (from the source), link.
   A hit qualifies only if it has a clear, testable SEO use for store and site owners.

3. SEO NEWS (last 7 days)
   Google Search Central blog, Google Search Status Dashboard (core/spam updates),
   Search Engine Roundtable, Search Engine Land. Prefer the primary source behind each story.

4. PICK TODAY'S TOPIC
   - If a qualifying AI-radar release is not yet in used-angles.md and the weekly limit allows
     → make it today's topic (pillar 8), angle = "what it changes for your SEO" + one task
     the viewer can do with it today.
   - Otherwise prefer an unused angle from docs/competitor-ads-blueprint.md section 5 that fits
     current news, then the strongest SEO news item, or an evergreen how-to from the least recently
     used pillar if the news is thin.
   - Never reuse an angle from the last 60 days.

5. REEL (every day)
   Write queue/<date>/reel/script.md and reel/caption.txt following the reel skill.

6. CAROUSEL (only if due)
   Same topic, or a closely related "complete overview" angle. Write deck.json, render with
   `python3 render.py queue/<date>/deck.json`, open 3 slides and fix any overflow, then write
   caption.txt and alt.txt.

7. SOURCES + REVIEW
   - sources.md: every factual claim (names, dates, numbers, capabilities) with its URL.
     Drop any claim you could not verify.
   - review.md for the human reviewer: topic, pillar, why today, keyword, AI-radar findings
     (including releases you skipped and why), anything uncertain.
   Keywords only from config.json.

8. SHIP
   Append one line per piece to used-angles.md (date | REEL/CAROUSEL | pillar | angle | keyword).
   Commit everything (queue/<date>/ incl. slides/*.jpg, used-angles.md, research/learnings.md)
   on branch content/<date> with the message "Content <date>: <angle>" and push that branch.
   Do not open a PR. The review.yml Action sends it to Telegram and merges it into main.
