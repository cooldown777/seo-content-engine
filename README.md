# seo-content-engine
Daily Instagram carousels for @makeseo.ai.
Claude Code routine researches + renders → opens a PR → you review on GitHub → merge = post.

- Render locally: `bash scripts/setup.sh && python3 render.py queue/example/deck.json`
- Rules: CLAUDE.md · Design: docs/carousel-system.pdf · Content: docs/content-blueprint.md
- Routine prompt: routine-prompt.md
- Publishing: .github/workflows/publish.yml (secrets IG_USER_ID, IG_ACCESS_TOKEN)
