# seo-content-engine
Daily Instagram carousels for @makeseo.ai.
Claude Code routine researches + renders → pushes content/<date> → Telegram message with slides + caption → you post manually.

- Render locally: `bash scripts/setup.sh && python3 render.py queue/example/deck.json`
- Rules: CLAUDE.md · Design: docs/carousel-system.pdf · Content: docs/content-blueprint.md
- Routine prompt: routine-prompt.md
- Review: .github/workflows/review.yml (secrets TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
- Optional auto-posting: .github/workflows/publish.yml (manual trigger only; secrets IG_USER_ID, IG_ACCESS_TOKEN)
