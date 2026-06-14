"""
NPC Dialogue powered by GPT-5 Nano.
Falls back to pre-written opening lines if OPENAI_API_KEY is not set.
"""
import json
import random
from openai import AsyncOpenAI

from config import settings
from game.data import get_npc
from game.world import (
    get_dialogue_history,
    get_or_create_relationship,
    increment_npc_visit,
    save_dialogue_turn,
)

# Initialize OpenAI client lazily
_client: AsyncOpenAI | None = None


def get_client() -> AsyncOpenAI | None:
    global _client
    if not settings.openai_api_key:
        return None
    if _client is None:
        _client = AsyncOpenAI(api_key=settings.openai_api_key)
    return _client


# ---------------------------------------------------------------------------
# Fallback suggestion sets per NPC
# Used when OpenAI is unavailable or suggestion generation fails
# ---------------------------------------------------------------------------

_NPC_FALLBACK_SUGGESTIONS: dict[str, list[str]] = {
    "old_tomas": [
        "How's business lately?",
        "Tell me about your son.",
        "What was Ironhaven like before Mercer?",
    ],
    "maren": [
        "What moves through this port?",
        "Tell me about the night shipments.",
        "How long have you worked the docks?",
    ],
    "nurse_hana": [
        "What injuries are you seeing lately?",
        "Have you treated workers from the forest?",
        "What do you know about the black ore?",
    ],
    "captain_rel": [
        "What's happening in this city?",
        "Tell me about your past.",
        "What should I watch out for?",
    ],
    "vex": [
        "What cards do you have?",
        "How did you end up in Ironhaven?",
        "What do you know about the ruins symbol?",
    ],
    "bora": [
        "What do people talk about in here?",
        "What have the soldiers been saying?",
        "Tell me about Ironhaven.",
    ],
    "shade": [
        "Who are you?",
        "What are you doing in the ruins?",
        "What do you know about Mercer?",
    ],
    "old_grull": [
        "How's the fishing?",
        "What's changed near the caves?",
        "Tell me about the cove.",
    ],
}

_DEFAULT_FALLBACK_SUGGESTIONS = [
    "How are things in Ironhaven?",
    "What do you know about Mercer?",
    "Anything I should know about this city?",
]


# ---------------------------------------------------------------------------
# System prompt builder
# ---------------------------------------------------------------------------

def build_system_prompt(npc: dict, relationship, player_name: str) -> str:
    rel_level = relationship.relationship_level if relationship else "Stranger"
    visits    = relationship.visit_count if relationship else 0

    milestones   = npc.get("relationship_milestones", {})
    context_notes = []
    for threshold, note in milestones.items():
        if visits >= int(threshold):
            context_notes.append(note)
    context_str = "\n".join(f"- {n}" for n in context_notes) if context_notes else "- No history yet."

    return f"""You are an NPC in an RPG game set in Ironhaven, a port city under the control of a corrupt merchant lord named Mercer.

{npc['persona']}

--- PLAYER INFO ---
Name: {player_name}
Your relationship: {rel_level} (visits: {visits})

--- RELATIONSHIP CONTEXT ---
{context_str}

--- RULES ---
- Keep responses SHORT (2-5 sentences max). This is a game, not a novel.
- Stay completely in character. No meta-commentary.
- Reflect the relationship level in your tone and what you're willing to share.
- Advance the story naturally through conversation.
- Do not use asterisks for actions — just write dialogue and description naturally.
- Never break character or acknowledge you are an AI.
"""


# ---------------------------------------------------------------------------
# Main reply function
# ---------------------------------------------------------------------------

async def get_npc_reply(
    npc_id: str,
    user_id: int,
    player_message: str,
    player_name: str,
    session,
) -> str:
    npc = get_npc(npc_id)
    if not npc:
        return "..."

    relationship = await increment_npc_visit(user_id, npc_id, session)
    client       = get_client()

    if client is None:
        return _fallback_reply(npc, relationship)

    history  = await get_dialogue_history(user_id, npc_id, session, limit=8)
    messages = []
    for turn in history:
        messages.append({"role": turn.role, "content": turn.content})
    messages.append({"role": "user", "content": player_message})

    system_prompt = build_system_prompt(npc, relationship, player_name)

    try:
        response = await client.chat.completions.create(
            model=settings.nano_model,
            messages=[{"role": "system", "content": system_prompt}] + messages,
            max_completion_tokens=200,
            temperature=0.85,
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[NPC AI Error] {npc_id}: {e}")
        reply = _fallback_reply(npc, relationship)

    await save_dialogue_turn(user_id, npc_id, "user",      player_message, session)
    await save_dialogue_turn(user_id, npc_id, "assistant", reply,          session)

    return reply


# ---------------------------------------------------------------------------
# Suggestion buttons generator
# ---------------------------------------------------------------------------

async def get_dialogue_suggestions(
    npc_id: str,
    last_reply: str,
    player_name: str,
    relationship,
) -> list[str]:
    """
    Generate 3 short conversation suggestion buttons based on the NPC's last reply.
    Falls back to static suggestions if generation fails.

    Returns a list of 3 strings (max 80 chars each).
    """
    client = get_client()

    if client is None:
        return _get_fallback_suggestions(npc_id)

    npc = get_npc(npc_id)
    if not npc:
        return _get_fallback_suggestions(npc_id)

    rel_level = relationship.relationship_level if relationship else "Stranger"

    prompt = (
        f"You are generating conversation options for a player talking to {npc['name']} "
        f"({npc.get('role','NPC')}) in an RPG.\n\n"
        f"The NPC just said:\n\"{last_reply}\"\n\n"
        f"The player's relationship with this NPC: {rel_level}\n\n"
        f"Generate exactly 3 short conversation replies the player might say next. "
        f"Each must be under 60 characters. "
        f"Make them feel natural, varied, and in keeping with the tone. "
        f"Return ONLY a JSON array of 3 strings. No other text. Example:\n"
        f'["Reply one.", "Reply two.", "Reply three."]'
    )

    try:
        response = await client.chat.completions.create(
            model=settings.nano_model,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=80,
            temperature=0.8,
        )
        raw = response.choices[0].message.content.strip()
        # Strip markdown code fences if present
        raw = raw.replace("```json", "").replace("```", "").strip()
        suggestions = json.loads(raw)
        if isinstance(suggestions, list) and len(suggestions) >= 3:
            return [str(s)[:80] for s in suggestions[:3]]
    except Exception as e:
        print(f"[Suggestion Error] {npc_id}: {e}")

    return _get_fallback_suggestions(npc_id)


def _get_fallback_suggestions(npc_id: str) -> list[str]:
    return _NPC_FALLBACK_SUGGESTIONS.get(npc_id, _DEFAULT_FALLBACK_SUGGESTIONS)


def _fallback_reply(npc: dict, relationship) -> str:
    opening_lines = npc.get("opening_lines", ["..."])
    return random.choice(opening_lines)