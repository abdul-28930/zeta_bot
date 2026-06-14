# Zeta — AI RPG Discord Bot

One Piece-inspired RPG that runs entirely through a single Discord message. Card combat, AI-powered NPCs, Ironhaven island narrative.

## Stack

| Layer | Tech |
|-------|------|
| Bot | discord.py 2.x |
| DB | PostgreSQL (Neon free tier) |
| Cache | Redis (Upstash free tier) |
| AI | OpenAI GPT-5.4 Nano |
| Host | Fly.io |

---

## Quick Setup

### 1. Clone & install

```bash
git clone <repo>
cd zeta_bot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your values:
```

| Variable | Where to get it |
|----------|----------------|
| `DISCORD_TOKEN` | [Discord Developer Portal](https://discord.com/developers/applications) → Bot → Token |
| `OPENAI_API_KEY` | [OpenAI Platform](https://platform.openai.com/api-keys) |
| `DATABASE_URL` | [Neon](https://neon.tech) → Connection string (use `postgresql+asyncpg://...`) |
| `REDIS_URL` | [Upstash](https://upstash.com) → Redis → Connection string |
| `NANO_MODEL` | `gpt-5.4-nano` (or `gpt-4o-mini` for fallback) |

### 3. Discord Bot setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create application → Bot
3. Enable **Privileged Gateway Intents**: Message Content Intent
4. OAuth2 → URL Generator → Scopes: `bot`, `applications.commands`
5. Bot Permissions: `Send Messages`, `Embed Links`, `Attach Files`
6. Copy the invite URL and add the bot to your server

### 4. Initialize database

```bash
python scripts/seed_db.py
```

### 5. Run

```bash
python main.py
```

---

## Deploying to Fly.io

```bash
fly launch
fly secrets set DISCORD_TOKEN=... OPENAI_API_KEY=... DATABASE_URL=... REDIS_URL=...
fly deploy
```

Create a `fly.toml`:
```toml
[build]

[env]
  DEBUG = "false"

[[services]]
  internal_port = 8080
  protocol = "tcp"

[processes]
  app = "python main.py"
```

---

## Game Overview

### Commands

| Command | Description |
|---------|-------------|
| `/zeta` | Open your game (creates character if new) |
| `/zeta_rest` | Rest at the inn (20 Ƶ, restores HP) |
| `/zeta_resetbattle` | Emergency battle reset if stuck |

### Character Creation

1. Select your **Race** (Human / Fishman / Skyborn / Mink / Giant)
2. Select your **Class** (Warrior / Mage / Guardian / Rogue / Ranger / Cleric)
3. Name your character
4. You start in Ironhaven's **Town Square**

### Exploration

From any zone, use the buttons:

- **🚶 Move** — Travel to connected zones
- **💬 Talk** — Speak with NPCs (AI-powered)
- **⚔️ Fight** — Engage enemies in card combat
- **🎒 Bag** — View inventory
- **👤 Profile** — View stats and level
- **🗺️ Map** — Ironhaven overview

### Card Combat

- Start with **3 energy** (max 6, regens 2/turn)
- Draw **4 cards** at battle start, +1 per turn
- Play cards by clicking their button
- **Pass** to skip to enemy's turn
- **Flee** to escape (costs 10 Ƶ)

### Economy

Currency is **Ƶ (Zet)**.
- Earn from battles and quests
- Spend at shops in the Market Quarter
- Rest at the inn for 20 Ƶ

### NPC Relationships

Every NPC tracks:
- **Visit count** — how often you've talked to them
- **Relationship score** — improves with positive interactions
- **Relationship level** — Stranger → Acquaintance → Friendly → Trusted → Beloved

Higher relationship = richer AI responses and unlocked story content.

### Arc 1: Ironhaven

The merchant lord **Mercer** controls Ironhaven through debt and intimidation.
Storylets trigger automatically as you explore and build NPC relationships.

- Speak with **Maren** (Port District) 3+ times to start Arc 1
- Follow the trail into **Ashwood Forest**
- Confront **Shade** at the **Ancient Ruins**

---

## Architecture

```
zeta_bot/
├── main.py           # Bot entry point
├── config.py         # Pydantic settings
├── core/
│   ├── database.py   # Async SQLAlchemy engine
│   ├── models.py     # ORM models
│   └── cache.py      # Redis helpers
├── game/
│   ├── data.py       # All world data (in-memory)
│   ├── engine.py     # Battle engine
│   └── world.py      # DB helpers for player state
├── ai/
│   └── npc.py        # OpenAI NPC dialogue
├── ui/
│   ├── embeds.py     # Discord embed builders
│   └── views.py      # Discord Views / Buttons / Modals
└── cogs/
    └── game.py       # /zeta slash command
```

**Key pattern:**
- World data (zones, NPCs, enemies, cards) = Python dicts in `game/data.py`
- Player state = PostgreSQL via SQLAlchemy
- Active battle state = Redis (1hr TTL)
- Every button callback: fetch state → compute → `edit_message()`

---

## Without OpenAI

The bot works without an `OPENAI_API_KEY`. NPCs fall back to pre-written opening lines instead of dynamic AI responses. Set `OPENAI_API_KEY=` (empty) in `.env`.
