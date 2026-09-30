Daily content routine for @makeseo.ai. Follow CLAUDE.md and the carousel skill exactly.

1. Read used-angles.md. If the newest CAROUSEL entry is younger than `carousel_every_days`
   from config.json, write "No carousel due today" in the session summary and stop.
2. Research what is new and useful in SEO this week: Google Search Central blog, Google Search
   Status Dashboard, Search Engine Roundtable, Search Engine Land, plus AI search changes
   (ChatGPT search, Perplexity, Google AI Overviews / AI Mode). Prefer primary sources.
3. Pick ONE angle for store and site owners that is not in used-angles.md (last 60 days) and
   fits the least recently used pillar. Evergreen how-to topics are fine when news is thin.
4. Use `default_keyword` from config.json unless another approved keyword fits clearly better.
5. Create queue/<today>/ with deck.json, render it, visually check 3 slides, then write
   caption.txt, alt.txt, sources.md and review.md.
6. Append the angle to used-angles.md.
7. Commit on branch content/<today> and open a PR titled "Carousel <today>: <angle>" with
   review.md as the PR description and the first 3 slide images linked.
