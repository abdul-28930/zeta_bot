"""
game/world_state.py

Zone description overrides based on world flags (Arc 1 completion, etc.).
Checked in zone_embed() in ui/embeds.py.

Usage:
    from game.world_state import get_zone_state_description
    override = get_zone_state_description(zone_id, player_flags)
    if override:
        embed.description = override
"""

# ---------------------------------------------------------------------------
# World state overrides
# Key = flag that must be set → list of (zone_id, new_description)
# Multiple flags can stack — last matching override wins
# ---------------------------------------------------------------------------

WORLD_STATE_ZONES: dict[str, list[tuple[str, str]]] = {

    # ── Arc 1 resolved (resist path) ────────────────────────────────────────
    "arc1_resolved": [
        (
            "town_square",
            "The square has changed. Mercer's portrait on the east wall has been "
            "defaced — the eyes crossed out, a single word written underneath that "
            "the soldiers are still trying to scrub off. The Council badge on the "
            "guards' uniforms looks different now, worn with less certainty. "
            "People in the square are talking to each other. Not all of them are "
            "being careful about it.",
        ),
        (
            "market_quarter",
            "Old Tomás's shop has a new sign in the window: *Temporarily reduced "
            "hours. Back soon.* The market still runs. But the conversation between "
            "stalls has changed — quieter in some places, louder in others. "
            "Nurse Hana's lights are on at all hours. The queue outside "
            "the Potion Emporium is longer than it's ever been.",
        ),
        (
            "port_district",
            "Maren's office light doesn't go off anymore. The docks are "
            "operating under emergency audit — Councilmember Aldric's people "
            "are walking the manifests with clipboards, stopping every crate. "
            "The sailors move differently. Like men who've heard something "
            "and are waiting to see if it's true.",
        ),
        (
            "ashwood_forest",
            "The ore operation has gone quiet. The cart tracks stop mid-trail. "
            "The workers who were out here have dispersed — some came back "
            "to the city, some went further into the forest, some nobody "
            "is sure about. The silence in the forest feels different now. "
            "Less watchful. More uncertain.",
        ),
        (
            "ancient_ruins",
            "Signs of a recent gathering. Ash from multiple fires, all cold. "
            "Footprints from a dozen different directions converging on the "
            "central plaza, then dispersing. Someone has left flowers at the "
            "base of the carved wall — not Ironhaven flowers, something from "
            "further afield. Someone who came a long way for this.",
        ),
        (
            "fishermans_cove",
            "Old Grull is fishing from a different spot on the dock — one he "
            "hasn't used in years. When you ask why, he says: *'Better view.'* "
            "The cove feels slightly less braced. Like a place that's been "
            "holding its breath and has just, carefully, let some of it out.",
        ),
    ],

    # ── Arc 1 resolved (bribed path — player took Mercer's money) ───────────
    "arc1_complete_bribed": [
        (
            "town_square",
            "The square is quieter than it should be. Mercer's portrait is "
            "untouched. The guards move with the specific confidence of people "
            "who have recently been proven right about something. There's a "
            "new posting on the Guild board — a bounty notice, the name "
            "redacted, the reward significant.",
        ),
        (
            "market_quarter",
            "Vex's shop is closed. The sign says *Back in two weeks* but "
            "the sign looks new and the store looks emptied. Old Tomás is "
            "behind the counter as always, but he keeps looking at the door "
            "in a way that suggests he's waiting for news that isn't coming.",
        ),
        (
            "ancient_ruins",
            "The ruins are empty. The fire pits are cold. Whatever gathering "
            "happened here left few traces — deliberately. Someone swept the "
            "plaza. Carefully.",
        ),
    ],

    # ── Evidence revealed publicly ───────────────────────────────────────────
    "revelation_public": [
        (
            "town_square",
            "The notice boards are bare — the soldiers pulled everything down "
            "within the hour, but not before most of the city saw it. The Guild "
            "board has a fresh nail where something was posted. Three people "
            "have already asked you what you know about it. Two of them didn't "
            "wait for your answer.",
        ),
        (
            "port_district",
            "The harbour office has guards on the door now — new ones, Mercer's "
            "people, not the usual Council rotation. Maren hasn't been seen "
            "outside since this morning. But her light is still on.",
        ),
    ],

    # ── Shade joined the resistance ──────────────────────────────────────────
    "shade_joined": [
        (
            "ancient_ruins",
            "The ruins feel different. The specific watchfulness that used to "
            "live here — the sense of being assessed — is gone. The stonework "
            "is the same. The silence is the same. But the presence that "
            "used to occupy this space has moved on to somewhere else.",
        ),
    ],
}


def get_zone_state_description(
    zone_id: str,
    player_flags: dict[str, str | None],
) -> str | None:
    """
    Returns an updated zone description if any world state flags apply,
    or None if the zone description should remain unchanged.

    player_flags: dict of {flag_key: flag_value} for this player.
    Last matching override wins (most specific takes priority).
    """
    result = None
    for flag_key, zone_overrides in WORLD_STATE_ZONES.items():
        if player_flags.get(flag_key):
            for z_id, description in zone_overrides:
                if z_id == zone_id:
                    result = description
    return result


async def get_zone_state_description_async(
    zone_id: str,
    user_id: int,
    session,
) -> str | None:
    """
    Async version — loads relevant flags from DB and returns override.
    Use this from zone_embed() when you have a DB session.
    """
    from game.world import get_flag
    relevant_flags = list(WORLD_STATE_ZONES.keys())
    player_flags   = {}
    for flag_key in relevant_flags:
        val = await get_flag(user_id, flag_key, session)
        if val:
            player_flags[flag_key] = val

    return get_zone_state_description(zone_id, player_flags)