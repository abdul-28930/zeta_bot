"""
game/npc_scenes.py

Scripted milestone scenes that override AI dialogue at key relationship thresholds.

How it works:
    In _send_dialogue_message (views.py), before calling the AI, check if the
    player's relationship score just crossed a threshold for the current NPC.
    If a scene exists and its flag has NOT been set, show the scripted scene
    instead of running AI.

Usage:
    from game.npc_scenes import get_milestone_scene

    scene = await get_milestone_scene(user_id, npc_id, current_score, session)
    if scene:
        # show scripted embed + set scene flag
"""

from sqlalchemy.ext.asyncio import AsyncSession

# ---------------------------------------------------------------------------
# Scene data
# Each entry: threshold → {flag, title, text, footer}
# flag is set after the scene fires so it never repeats.
# ---------------------------------------------------------------------------

NPC_MILESTONE_SCENES: dict[str, dict[int, dict]] = {

    "maren": {
        10: {
            "flag":   "maren_scene_10",
            "title":  "The Cormorant",
            "text": (
                "She sets down her clipboard and looks at you directly for the first "
                "time — not the assessing look she gives new faces, but the measured "
                "look she gives people she's decided to trust.\n\n"
                "*\"I had a ship,\"* she says. *\"The Cormorant. Twenty-two tons. "
                "Best vessel that ever worked out of this port.\"*\n\n"
                "She picks the clipboard back up. *\"Mercer's bank took it three "
                "years ago. Debt restructuring. Everything legal, everything signed.\"*\n\n"
                "She goes back to her numbers. *\"I just thought you should know "
                "why I count every crate that moves through this port.\"*"
            ),
            "footer": "Trust: Acquaintance",
        },
        25: {
            "flag":   "maren_scene_25",
            "title":  "The Real Manifest",
            "text": (
                "She waits until the last harbour worker has left for the evening.\n\n"
                "Then she opens the bottom drawer and takes out a folder — not the "
                "official filing system, something older and more careful.\n\n"
                "*\"The Dawnbreak manifest.\"* She sets it in front of you. "
                "*\"The original, before the Council stamp. Someone altered the "
                "destination codes. I have the original version and the filed "
                "version. They don't match.\"*\n\n"
                "She taps the circled entry. *\"That's where the ore goes. "
                "That's the facility.\"*\n\n"
                "*\"I can't take this anywhere officially. But you're not official.\"*"
            ),
            "footer": "Trust: Friendly · Evidence obtained",
        },
    },

    "old_tomas": {
        10: {
            "flag":   "tomas_scene_10",
            "title":  "The Discount",
            "text": (
                "He waves away your payment.\n\n"
                "*\"Regular customer rate,\"* he says, with a wink that doesn't "
                "quite reach his eyes. *\"Don't tell anyone — I'll have half the "
                "city expecting it.\"*\n\n"
                "He busies himself with something behind the counter. A pause.\n\n"
                "*\"My son used to help me in the shop, you know. Before — well. "
                "He's working now. Good steady work.\"* Another pause. "
                "*\"He's fine.\"*\n\n"
                "He says it the way people say things they need to be true."
            ),
            "footer": "Trust: Acquaintance",
        },
        20: {
            "flag":   "tomas_scene_20",
            "title":  "Dario",
            "text": (
                "He mentions his son without meaning to — mid-sentence, talking "
                "about something else entirely.\n\n"
                "He stops. Catches himself.\n\n"
                "For a moment his hands are very still, and you see the weight of "
                "it — the thing he carries every day behind the warmth and the "
                "weather talk and the perfectly-timed smiles.\n\n"
                "*\"Dario,\"* he says. *\"My son's name is Dario.\"*\n\n"
                "He changes the subject. But the name sits in the room "
                "after he does."
            ),
            "footer": "Trust: Friendly",
        },
        35: {
            "flag":   "tomas_scene_35",
            "title":  "The Letter",
            "text": (
                "He pulls an envelope from under the counter — worn at the edges, "
                "read and refolded many times.\n\n"
                "*\"From Dario.\"* He holds it for a moment. "
                "*\"He's fine. He says so.\"*\n\n"
                "He holds it out to you. You can see the last line through the "
                "paper — the ink is darker there, pressed harder: "
                "*Don't come looking.*\n\n"
                "Tomás takes it back before you can say anything. Puts it away.\n\n"
                "*\"Good steady work,\"* he says again. *\"He's fine.\"*"
            ),
            "footer": "Trust: Trusted · See Storylet: Tomás and the Letter",
        },
    },

    "vex": {
        15: {
            "flag":   "vex_scene_15",
            "title":  "Not For Sale",
            "text": (
                "He takes a card from under the display case. Sets it on the counter, "
                "face up, between you.\n\n"
                "It's unlike anything in the display — the art is stranger, "
                "the border different, the card stock heavier.\n\n"
                "*\"Not for sale,\"* he says. *\"Not yet.\"* He looks at it, "
                "not at you. *\"There are cards that only mean something at the "
                "right moment. Play them too early and they're wasted.\"*\n\n"
                "He takes it back. *\"You're starting to understand what I mean.\"*"
            ),
            "footer": "Trust: Acquaintance",
        },
        30: {
            "flag":   "vex_scene_30",
            "title":  "The Question",
            "text": (
                "He waits until the last customer leaves.\n\n"
                "He leans on the counter the way someone leans on something when "
                "they've made a decision and are giving themselves one last moment.\n\n"
                "*\"If the game was rigged from the start,\"* he says. "
                "*\"Not stacked against you — rigged. The outcome fixed before "
                "the first card was played.\"*\n\n"
                "He looks at you.\n\n"
                "*\"Would you still play?\"*\n\n"
                "He doesn't wait for an answer. He writes something on a small "
                "card and slides it across the counter. An address. A time.\n\n"
                "*\"Think about it.\"*"
            ),
            "footer": "Trust: Friendly · See Storylet: Vex's Test",
        },
    },

    "nurse_hana": {
        15: {
            "flag":   "hana_scene_15",
            "title":  "Pattern Recognition",
            "text": (
                "She's labeling something when you come in. She doesn't stop.\n\n"
                "*\"I had a patient this morning,\"* she says. Clinically. "
                "*\"Forest worker. Laceration on the left forearm, consistent "
                "with a fall against a sharp edge.\"* She sets the vial down "
                "precisely. *\"That's what he told me. I wrote it down.\"*\n\n"
                "She looks at you.\n\n"
                "*\"It was the fourth patient this month with the same injury "
                "in the same location. Workers don't fall four times the same way.\"*\n\n"
                "She goes back to labeling. *\"I documented what I was told.\"*"
            ),
            "footer": "Trust: Acquaintance",
        },
        30: {
            "flag":   "hana_scene_30",
            "title":  "The Note",
            "text": (
                "She wraps the potion carefully, the way she wraps everything.\n\n"
                "Then she takes a small piece of paper — very small, folded once — "
                "and slips it underneath the label before she hands it to you.\n\n"
                "*\"Read it when you're somewhere quiet,\"* she says. "
                "*\"Not here.\"*\n\n"
                "The next customer is already waiting. She turns away.\n\n"
                "The note, when you read it later, says three things: a location, "
                "a time, and *I've been documenting. I need someone to give it to.*"
            ),
            "footer": "Trust: Friendly · See Storylet: Hana's Records",
        },
    },

    "captain_rel": {
        15: {
            "flag":   "rel_scene_15",
            "title":  "The Battle",
            "text": (
                "He tells you about a battle. Twenty years ago. A port city — "
                "not this one. A Council that had made promises and then made "
                "different ones when it became convenient.\n\n"
                "*\"We won,\"* he says. *\"In the sense that we held the position. "
                "In the sense that fewer people died than would have otherwise.\"*\n\n"
                "He's quiet for a moment.\n\n"
                "*\"We lost in the sense that nothing changed.\"*\n\n"
                "He resumes the drill without explaining further. But he's told "
                "you something. You're not sure yet what."
            ),
            "footer": "Trust: Acquaintance",
        },
        30: {
            "flag":   "rel_scene_30",
            "title":  "Retired",
            "text": (
                "He's watching the square when you arrive. Not training — just watching.\n\n"
                "*\"The Council calls me retired,\"* he says. Not to you. "
                "To the square, to the portrait, to Mercer's badges on the guards' "
                "chests. *\"Accurate enough. I'm retired from the old Council.\"*\n\n"
                "He looks at you for the first time.\n\n"
                "*\"Doesn't mean I'm finished.\"*\n\n"
                "He returns to his training. But something has shifted — "
                "the weight of a decision made."
            ),
            "footer": "Trust: Friendly · See Storylet: Rel's History",
        },
    },

    "shade": {
        10: {
            "flag":   "shade_scene_10",
            "title":  "Before",
            "text": (
                "He's looking at the ruins when you find him. Not inspecting them — "
                "something older than that.\n\n"
                "*\"This place had a different name before,\"* he says. "
                "Not looking at you. *\"People came here to meet in secret. "
                "Eleven years ago.\"*\n\n"
                "A pause.\n\n"
                "*\"I was one of them. For about six months, I was one of them.\"*\n\n"
                "He leaves it there. Doesn't explain. Doesn't defend.\n\n"
                "But he stays — which, from Shade, counts as an invitation."
            ),
            "footer": "Trust: Stranger → Acquaintance",
        },
        25: {
            "flag":   "shade_scene_25",
            "title":  "The Question",
            "text": (
                "*\"I'm going to ask you something,\"* he says. "
                "*\"I'd prefer an honest answer over a correct one.\"*\n\n"
                "He looks at you directly — the enforcer's assessment, but underneath "
                "it something that's been there for a long time, waiting.\n\n"
                "*\"Are you here because someone sent you? Or because you decided to be?\"*\n\n"
                "He waits. He means it.\n\n"
                "Whatever you say, he nods. Just once. And then:\n\n"
                "*\"There's a difference. It matters. Remember it.\"*"
            ),
            "footer": "Trust: Friendly",
        },
    },

    "bora": {
        10: {
            "flag":   "bora_scene_10",
            "title":  "The Usual",
            "text": (
                "He has your order ready before you sit down.\n\n"
                "*\"I remembered,\"* he says, with the satisfaction of someone "
                "who considers this a minor personal achievement. *\"Everyone "
                "has a usual. Some people just don't know it yet.\"*\n\n"
                "He leans on the bar. *\"Had a fascinating conversation with a "
                "Council sergeant last week. Three drinks in, very talkative. "
                "You know what's funny — he told me the entire watch schedule "
                "for the harbour and didn't seem to notice he was doing it.\"*\n\n"
                "He straightens up. *\"Not that I'd remember a thing like that.\"*"
            ),
            "footer": "Trust: Acquaintance",
        },
        25: {
            "flag":   "bora_scene_25",
            "title":  "Late",
            "text": (
                "The tavern is nearly empty. He pours you something he "
                "doesn't put a price on.\n\n"
                "*\"I had a friend once,\"* he says, in the tone of someone beginning "
                "one of his stories. *\"Ran a place like this, different city. "
                "Good man. Served everyone — soldiers, rebels, merchants, whoever "
                "came through the door.\"*\n\n"
                "He wipes the bar slowly.\n\n"
                "*\"He used to say: a tavern is the most useful building in any "
                "city, because everyone needs to eat, everyone needs to drink, "
                "and everyone, eventually, needs to talk.\"*\n\n"
                "He looks at you. *\"I think he was right about that.\"*\n\n"
                "He refills your cup without being asked."
            ),
            "footer": "Trust: Friendly",
        },
    },

    "old_grull": {
        10: {
            "flag":   "grull_scene_10",
            "title":  "The Good Spot",
            "text": (
                "He doesn't say anything. He just jerks his head toward the water "
                "and starts walking — the assumption being that you'll follow, "
                "and that you'll figure out why.\n\n"
                "He stops at a point on the dock that looks identical to every "
                "other point on the dock.\n\n"
                "*\"Here,\"* he says.\n\n"
                "You fish. You catch more than you would have otherwise.\n\n"
                "Walking back, he says: *\"Not everyone gets that spot.\"*\n\n"
                "That's it. That's the milestone."
            ),
            "footer": "Trust: Acquaintance",
        },
    },
}


# ---------------------------------------------------------------------------
# Runtime check — called from _send_dialogue_message in views.py
# ---------------------------------------------------------------------------

async def get_milestone_scene(
    user_id: int,
    npc_id: str,
    current_score: int,
    session: AsyncSession,
) -> dict | None:
    """
    Check if the player's relationship with this NPC has just crossed a milestone.
    Returns the scene dict if one should fire, None otherwise.

    A scene fires if:
      - current_score >= threshold
      - the scene's flag has not been set for this player
    Returns the LOWEST unfired threshold that qualifies.
    """
    from game.world import get_flag, set_flag

    npc_scenes = NPC_MILESTONE_SCENES.get(npc_id)
    if not npc_scenes:
        return None

    for threshold in sorted(npc_scenes.keys()):
        if current_score >= threshold:
            scene = npc_scenes[threshold]
            flag_val = await get_flag(user_id, scene["flag"], session)
            if not flag_val:
                # Mark it fired
                await set_flag(user_id, scene["flag"], "true", session)
                return {**scene, "npc_id": npc_id, "threshold": threshold}

    return None