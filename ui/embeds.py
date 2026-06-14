"""
ui/embeds.py — Zeta
Complete embeds file including onboarding sequence + card collection viewer.
"""
import random
from datetime import datetime, timezone

import discord

from game.data import (
    BUILDINGS,
    CARDS,
    CLASSES,
    ENEMIES,
    ITEMS,
    NPCS,
    RACES,
    RARITY_EMOJI,
    SEC_COLORS,
    SEC_ICONS,
    ZONES,
    get_buildings_in_zone,
    get_card,
    get_class,
    get_enemies_in_zone,
    get_enemy,
    get_item,
    get_npc,
    get_npcs_in_zone,
    get_race,
    get_zone,
)
from game.engine import energy_pips, hp_bar, status_summary

COLOR_MAIN     = 0x7F77DD
COLOR_BATTLE   = 0xE24B4A
COLOR_DIALOGUE = 0x5DCAA5
COLOR_WARNING  = 0xEF9F27
COLOR_SUCCESS  = 0x57B05E
COLOR_DEATH    = 0x2B2B2B

ZONE_ATMOSPHERES = {
    "town_square": [
        "A Council soldier eyes you from across the square.",
        "Mercer's portrait watches from every wall.",
        "Children run past. Their parents don't look up.",
        "The city hums with the sound of controlled routine.",
        "The Adventurer's Guild board has new contracts posted this morning. Someone has already torn one down.",
        "Two merchants argue in lowered voices near the guild steps. They stop when they notice you.",
        "The fountain in the center hasn't been cleaned recently. The water is slightly green.",
        "A notice has been pinned to the guild board: 'OUTSTANDING DEBT — SEE COUNCIL HALL.' The name is torn off.",
        "The square smells like bread from the inn and something chemical from the direction of the docks.",
        "A pair of guards do a slow circuit of the square. They walk like men who aren't expecting trouble but wouldn't mind some.",
        "An old woman feeds pigeons near the fountain. She's been doing it every morning for as long as anyone can remember.",
        "Someone has left a bouquet of flowers at the base of Mercer's portrait. They're wilting.",
        "A boy is selling newspapers near the guild steps. The headline is about improved shipping efficiencies.",
        "The morning crowd moves with the particular rhythm of people who've learned not to dawdle near guards.",
        "A street sweeper works the cobblestones slowly, methodically. They've been doing this for thirty years.",
    ],
    "market_quarter": [
        "Shopkeepers smile at precisely the right moments.",
        "The prices are fair. Mercer sets them.",
        "A tax collector passes with a clipboard and a practiced frown.",
        "Everything is available here. For a price.",
        "Nurse Hana's shop is meticulously clean through the window. Everything labeled. Everything in its place.",
        "Old Tomás talks to every customer the same way — like they're the most interesting person he's seen all week.",
        "Market noise: bartering, footsteps, the specific creak of a cart wheel that needs oil.",
        "A customer leaves the general store with less than they came in with. Tomás waves them off warmly.",
        "The auction house board has active listings. You scan them without stopping.",
        "Two sailors argue over a card at the card shop entrance. Vex watches from inside without expression.",
        "The equipment shop has a new display in the window. Functional, not decorative.",
        "A child tries to steal an apple from a fruit stall. The merchant sees them. Lets it go.",
    ],
    "port_district": [
        "Salt air and the creak of rigging.",
        "A sailor argues loudly about something. Nobody intervenes.",
        "The guard patrol is lazy here. Predictably.",
        "Ships from everywhere. Stories from nowhere.",
        "The harbour office light is on. Maren never seems to leave.",
        "Smell of tar and rope and something chemical that might be preservative.",
        "A drunk sailor sleeps against the tavern wall. Someone has put a hat over his face.",
        "Three men in Mercer's badges stand near the dock road watching the water.",
        "Bora's tavern is full. You can hear it from here.",
        "A wanted notice has been posted on the harbour office wall. The drawing doesn't look like anyone.",
        "The smell of the port changes at high tide. More immediate. More honest.",
        "The evening crowd in the port is different from the day crowd. Quieter. More purposeful.",
    ],
    "harbour_docks": [
        "Crates stacked six high along the dock road. Most are labeled. Some aren't.",
        "The tide is going out. The smell changes when that happens.",
        "A tax collector with a clipboard walks the dockside at a pace that suggests they've found something.",
        "Four men unload a ship in practiced silence.",
        "The water here is darker than it should be.",
        "A gull lands on the nearest crate and immediately flies off.",
        "A night shift supervisor counts crates by lamplight, lips moving silently.",
        "One of the dock workers has a dark stain on their hands that isn't standard cargo residue.",
        "The docks at this hour are quieter. The work doesn't stop but the people doing it try to be invisible.",
    ],
    "farmlands": [
        "The harvest looks good. That means the collectors will be here soon.",
        "A farmer watches you from their field without waving.",
        "Forty percent. That's what Mercer takes. Every month.",
        "Wind across the fields. The crops move. The people working them don't, much.",
        "A rent collector rides past on horseback going toward town.",
        "Open sky. You keep forgetting Ironhaven has this much of it.",
        "A child runs between the rows of crops playing something.",
        "The road through the farmlands is well-maintained. Council maintained.",
        "A dog barks twice at you from behind a fence.",
        "Someone has marked the edge of their plot with small stones. Boundary dispute, probably.",
    ],
    "ashwood_forest": [
        "The trees close in. Sound behaves differently in here.",
        "Something moved at the edge of your vision. When you look, nothing.",
        "Cart tracks on a path that isn't on any official map.",
        "The light is wrong in here. Has been for a while.",
        "A bird call you don't recognise. Then silence.",
        "The trees are old. Older than Ironhaven.",
        "You find a snapped torch handle half-buried in the undergrowth.",
        "The undergrowth has been cleared in places. Deliberately.",
        "The forest smell: pine, earth, and underneath that, something mineral.",
        "A marker tied to a tree at eye height. Not a trail marker.",
        "Your footsteps are louder here than they should be.",
        "The path splits. Both directions look equally unused. One of them is lying.",
    ],
    "cursed_grove": [
        "The trees have gone black at the roots.",
        "An animal watches you from the shadows. Its eyes are wrong.",
        "The air temperature drops when you step into the grove.",
        "The ground gives slightly underfoot.",
        "Insects but no birds.",
        "The black color on the trees moves upward from the roots.",
        "You hear something that might be breathing that isn't yours.",
        "The ore deposits here are larger. Exposed. Wrong.",
        "A path through the grove, pressed flat by passage.",
        "The light here is dim but sourceless.",
    ],
    "ancient_ruins": [
        "No wind. The silence feels deliberate.",
        "Footprints in the dust that aren't yours. Recent.",
        "Old stone remembers. You can't say how you know that.",
        "Whatever this place was, it was built by people who expected it to last.",
        "The carvings on the walls are in a script you don't recognise.",
        "Your voice, if you used it, would echo longer than the space explains.",
        "Something has been moved recently. A stone block, shifted.",
        "The ruins sit in a clearing. The forest doesn't grow right up to the edge.",
        "A fire pit, cold. Someone camps here.",
        "The stonework is finer than anything in Ironhaven.",
    ],
    "fishermans_cove": [
        "The sea is the only thing Mercer hasn't figured out how to tax.",
        "Old boats. Older debts.",
        "The fishermen don't talk to strangers. Not anymore.",
        "The water near the caves has changed color slightly.",
        "Old Grull's shack has smoke coming from the chimney.",
        "The cove is independent from the official docks. Deliberately.",
        "Seagulls fight over something on the beach.",
        "The tide marks on the cave cliffs show the water reaches higher than it used to.",
        "Three fishermen mend nets without speaking.",
        "A child runs along the dock edge.",
    ],
    "sea_caves": [
        "The tide is low. The cave breathes cold air.",
        "Sound travels strangely in here.",
        "The walls are wet. Not from the tide.",
        "Bioluminescent patches on the cave ceiling.",
        "The dark here is complete when you're away from the entrance.",
        "Water sounds from deeper in. Not waves.",
        "The black ore veins in the cave walls are larger than the ones in the forest.",
        "The smell changes the deeper you go. Less salt. More metal.",
        "Something large moves in the water channel to your right.",
    ],
    "smugglers_trail": [
        "The path isn't on any official map.",
        "Fresh wheel ruts. Heavy cargo, recently.",
        "Mercer's private mercenaries use this route.",
        "Move quietly.",
        "The brush on either side has been cut back just enough.",
        "A marker on a tree that you almost walk past.",
        "The trail runs between two worlds: the city and the forest.",
        "At the midpoint, you can see both Ironhaven's towers and the Ashwood's canopy.",
    ],
    "shadow_den": [
        "Armed. Professional. Expensive.",
        "This is where people end up when they stop being useful.",
        "Nobody comes here by accident.",
        "The compound is built into the ruins.",
        "Two guards at every entrance.",
        "The equipment here is better than Council standard.",
        "Commander Voss runs this place like a military operation.",
        "The air here is colder than the ruins outside.",
    ],
    "residential_ward": [
        "Every door has a debt notice.",
        "A child watches you from a window.",
        "The ward is quiet in the way that means people have learned to be quiet.",
        "Washing lines between buildings.",
        "Someone is cooking. The smell reaches the street.",
        "Three neighbours talk in lowered voices at a corner.",
        "The streets are clean.",
        "A dog sleeps in a doorway.",
        "A child's drawing chalked on the pavement: a fish, a boat, an island.",
    ],
}


def _atmosphere(zone_id: str) -> str:
    lines = ZONE_ATMOSPHERES.get(zone_id, ["The city watches."])
    return random.choice(lines)


def _time_of_day() -> str:
    hour = datetime.now(timezone.utc).hour
    if 5 <= hour < 9:    return "🌅 Dawn"
    elif 9 <= hour < 17: return "☀️ Day"
    elif 17 <= hour < 21:return "🌆 Dusk"
    else:                return "🌙 Night"


# ---------------------------------------------------------------------------
# ZONE Embed
# ---------------------------------------------------------------------------

def zone_embed(player, zone_data: dict, world_override: str | None = None, zone_status: dict | None = None) -> discord.Embed:
    security  = zone_data.get("security", "high")
    color     = SEC_COLORS.get(security, COLOR_MAIN)
    sec_icon  = SEC_ICONS.get(security, "🟢")
    prog      = player.progression
    stats     = player.stats
    max_hp    = stats.vit * 5
    cls       = get_class(player.class_id) or {}
    hp_display= hp_bar(prog.current_hp, max_hp)

    embed = discord.Embed(
        title=f"{zone_data['emoji']}  {zone_data['name']}  ·  {_time_of_day()}",
        color=color,
    )
    atmosphere = _atmosphere(zone_data["id"])
    base_desc = world_override if world_override else zone_data['description']
    embed.description = f"*{base_desc}*\n\n_{atmosphere}_"
    embed.add_field(
        name=f"{sec_icon} {security.title()} Zone  ·  {cls.get('emoji','')} {player.character_name}  Lv.{prog.level}",
        value=f"`{hp_display}` **{prog.current_hp}/{max_hp}** HP  ·  💰 **{prog.zet_wallet:,} Ƶ**",
        inline=False,
    )
    npcs      = get_npcs_in_zone(zone_data["id"])
    enemies   = get_enemies_in_zone(zone_data["id"])
    buildings = get_buildings_in_zone(zone_data["id"])
    presence  = []
    if npcs:
        presence.append("  ".join(f"{n['emoji']} {n['name']}" for n in npcs))
    if enemies:
        presence.append("  ".join(f"{e['emoji']} ~~{e['name']}~~" for e in enemies))
    if presence:
        embed.add_field(name="👁 Here", value="  ·  ".join(presence), inline=False)
    if buildings:
        embed.add_field(
            name="🏛️ Places",
            value="  ".join(f"{b['emoji']} {b['name']}" for b in buildings[:5]),
            inline=False,
        )
    if zone_status:
        from game.respawn import format_respawn_time
        if zone_status.get("enemy_cleared") and zone_status.get("enemy_respawn_secs", 0) > 0:
            t = format_respawn_time(zone_status["enemy_respawn_secs"])
            embed.add_field(
                name="⏱ Zone Quiet",
                value=f"Enemies cleared — respawn in **{t}**",
                inline=True,
            )
        if zone_status.get("miniboss_id"):
            if zone_status.get("miniboss_alive"):
                from game.data import ENEMIES, MINI_BOSSES
                mb_id   = MINI_BOSSES.get(zone_data["id"], "")
                mb      = ENEMIES.get(mb_id, {})
                embed.add_field(
                    name=f"{mb.get('emoji','⚔️')} Elite Spotted",
                    value=f"**{mb.get('name','Mini-boss')}** is in this zone. Walk to encounter.",
                    inline=True,
                )
            elif zone_status.get("miniboss_respawn_secs", 0) > 0:
                t        = format_respawn_time(zone_status["miniboss_respawn_secs"])
                defeated = zone_status.get("miniboss_defeated_by", "someone")
                embed.add_field(
                    name="💀 Elite Defeated",
                    value=f"Slain by **{defeated}** — respawns in **{t}**",
                    inline=True,
                )
    embed.set_footer(text="Walk to explore · Visit buildings · Travel to move zones")
    return embed


# ---------------------------------------------------------------------------
# WALK Embed
# ---------------------------------------------------------------------------

def walk_embed(player, zone_data: dict, walk_result: dict) -> discord.Embed:
    security    = zone_data.get("security", "high")
    color       = SEC_COLORS.get(security, COLOR_MAIN)
    prog        = player.progression
    stats       = player.stats
    max_hp      = stats.vit * 5
    event_type  = walk_result["event_type"]
    daily_steps = walk_result["daily_steps"]
    total_steps = walk_result["total_steps"]
    xp_gained   = walk_result["xp_gained"]

    embed = discord.Embed(
        title=f"{zone_data['emoji']}  {zone_data['name']}  ·  Step {daily_steps}",
        color=color,
    )

    atmosphere   = walk_result["atmosphere"]
    event_prefix = ""
    extra_field  = None

    if event_type == "npc_moment" and walk_result.get("npc_moment"):
        atmosphere   = walk_result["npc_moment"]["line"]
        event_prefix = "👤 "

    elif event_type == "discovery" and walk_result.get("discovery"):
        atmosphere   = walk_result["discovery"]["text"]
        event_prefix = "\U0001f50d "

    elif event_type == "item_find" and walk_result.get("item_find"):
        find         = walk_result["item_find"]
        atmosphere   = find.get("text", "You find something.")
        event_prefix = "\U0001f4e6 "
        extra_field  = ("\U0001f9f3 Added to bag", "Check your inventory.")

    elif event_type == "overheard" and walk_result.get("overheard"):
        atmosphere   = walk_result["overheard"]
        event_prefix = "💬 "

    elif event_type == "rumour" and walk_result.get("rumour"):
        atmosphere   = walk_result["rumour"]
        event_prefix = "\U0001f5e3\ufe0f "

    elif event_type == "lore_fragment" and walk_result.get("lore_fragment"):
        atmosphere   = walk_result["lore_fragment"]
        event_prefix = ""

    embed.description = f"*{event_prefix}{atmosphere}*"

    hp_display  = hp_bar(prog.current_hp, max_hp)
    zet_dropped = walk_result.get("zet_dropped", 0)
    step_line   = f"+1 Step  ·  +{xp_gained} XP"
    if zet_dropped > 0:
        step_line += f"  ·  +{zet_dropped} Ƶ"
    if walk_result.get("xp_cap_warning"):
        step_line += "  _(XP rate reduced after step 20)_"
    embed.add_field(
        name=f"`{hp_display}` {prog.current_hp}/{max_hp} HP  ·  💰 {prog.zet_wallet:,} Ƶ  ·  Lv.{prog.level}",
        value=step_line,
        inline=False,
    )

    if extra_field:
        embed.add_field(name=extra_field[0], value=extra_field[1], inline=False)

    if event_type == "quiet":
        quote = walk_result.get("quote")
        if quote:
            text, attribution = quote
            if attribution:
                embed.add_field(name="", value=f"💬 *{text}*\n\u2014 {attribution}", inline=False)
            else:
                embed.add_field(name="", value=text, inline=False)

    if walk_result.get("relationship_npc_name"):
        embed.add_field(
            name="",
            value=f"\U0001f49c +1 Relationship with **{walk_result['relationship_npc_name']}**",
            inline=False,
        )

    m = walk_result.get("mastery_milestone")
    if m and isinstance(m, dict):
        embed.add_field(
            name=f"{m['emoji']}  {m['label']} Unlocked!  ·  +{m['xp']} XP",
            value=m["lore"] if m.get("lore") else "You know this zone better than most.",
            inline=False,
        )

    if walk_result.get("quest_ready_message"):
        embed.add_field(
            name="",
            value=walk_result["quest_ready_message"],
            inline=False,
        )

    if walk_result.get("zone_cleared"):
        t = walk_result.get("zone_cleared_respawn", 1800)
        from game.respawn import format_respawn_time
        embed.add_field(
            name="⏱ Zone Cleared",
            value=f"Enemies are regrouping — respawn in **{format_respawn_time(t)}**",
            inline=False,
        )

    embed.set_footer(text=f"Step {daily_steps} today · {total_steps} total in this zone")
    return embed


# ---------------------------------------------------------------------------
# WALK ENCOUNTER Embed
# ---------------------------------------------------------------------------

def walk_encounter_embed(player, zone_data: dict, enemy: dict, step: int) -> discord.Embed:
    prog   = player.progression
    stats  = player.stats
    max_hp = stats.vit * 5
    embed  = discord.Embed(title=f"⚔️  Encounter!  ·  Step {step}", color=COLOR_BATTLE)
    embed.description = (
        f"*{enemy['emoji']} A **{enemy['name']}** blocks your path.*\n\n"
        f"_{enemy['description']}_"
    )
    embed.add_field(
        name="Your Status",
        value=f"`{hp_bar(prog.current_hp, max_hp)}` {prog.current_hp}/{max_hp} HP",
        inline=False,
    )
    embed.add_field(
        name=f"{enemy['emoji']} {enemy['name']}",
        value=f"❤️ {enemy['hp']} HP  ·  ⚔️ {enemy['atk']} ATK  ·  🛡️ {enemy['defense']} DEF",
        inline=False,
    )
    embed.set_footer(text="Fight, flee, or bluff — choose wisely.")
    return embed


# ---------------------------------------------------------------------------
# TRAVEL Embed
# ---------------------------------------------------------------------------

def travel_embed(player, from_zone: dict, to_zone: dict, travel_line: str) -> discord.Embed:
    security = to_zone.get("security", "high")
    color    = SEC_COLORS.get(security, COLOR_MAIN)
    prog     = player.progression
    stats    = player.stats
    max_hp   = stats.vit * 5
    embed    = discord.Embed(
        title=f"🚶  {from_zone['name']}  →  {to_zone['emoji']} {to_zone['name']}",
        description=f"*{travel_line}*",
        color=color,
    )
    embed.add_field(
        name=f"{SEC_ICONS.get(to_zone.get('security','high'),'')} {to_zone.get('security','').title()} Zone",
        value=to_zone.get("description","")[:120] + "...",
        inline=False,
    )
    embed.add_field(
        name="❤️ Status",
        value=f"`{hp_bar(prog.current_hp, max_hp)}` {prog.current_hp}/{max_hp} HP  ·  💰 {prog.zet_wallet:,} Ƶ",
        inline=False,
    )
    embed.set_footer(text="You've arrived. Start walking to explore.")
    return embed


# ---------------------------------------------------------------------------
# VISIT / EXITS Embeds
# ---------------------------------------------------------------------------

def visit_embed(zone_data: dict) -> discord.Embed:
    color = SEC_COLORS.get(zone_data.get("security","high"), COLOR_MAIN)
    embed = discord.Embed(
        title=f"🏛️  {zone_data['name']}  —  Buildings",
        description="Where do you want to go?",
        color=color,
    )
    embed.set_footer(text="Enter a building or go back to keep walking.")
    return embed


def exits_embed(zone_data: dict) -> discord.Embed:
    color     = SEC_COLORS.get(zone_data.get("security","high"), COLOR_MAIN)
    embed     = discord.Embed(
        title=f"🚶  Travel from {zone_data['name']}",
        description="Where are you headed?",
        color=color,
    )
    connected = zone_data.get("connected_to", [])
    if connected:
        zone_list = []
        for zid in connected:
            z = ZONES.get(zid)
            if z:
                sec = z.get("security","high")
                zone_list.append(f"{z['emoji']} **{z['name']}** — {SEC_ICONS.get(sec,'')} {sec.title()}")
        embed.add_field(name="Exits", value="\n".join(zone_list), inline=False)
    embed.set_footer(text="Tap a destination or go back.")
    return embed


# ---------------------------------------------------------------------------
# BATTLE Embed
# ---------------------------------------------------------------------------

def battle_embed(battle_state: dict, card_list: list) -> discord.Embed:
    enemy_name    = battle_state["enemy_name"]
    enemy_hp      = max(0, battle_state["enemy_hp"])
    enemy_max     = battle_state["enemy_max_hp"]
    enemy_shield  = battle_state.get("enemy_shield", 0)
    player_hp     = max(0, battle_state["player_hp"])
    player_max    = battle_state["player_max_hp"]
    player_shield = battle_state.get("player_shield", 0)
    energy        = battle_state["energy"]
    max_energy    = battle_state["max_energy"]
    turn          = battle_state["turn"]
    embed         = discord.Embed(
        title=f"⚔️  {enemy_name}  vs  {battle_state.get('player_name','You')}  ·  Turn {turn}",
        color=COLOR_BATTLE,
    )
    enemy_status_str = status_summary(battle_state.get("enemy_statuses", {}))
    shield_str = f"  🛡️{enemy_shield}" if enemy_shield > 0 else ""
    embed.add_field(
        name=f"👹 {enemy_name}",
        value=f"`{hp_bar(enemy_hp,enemy_max)}` {enemy_hp}/{enemy_max}{shield_str}\n{enemy_status_str or '─'}",
        inline=True,
    )
    player_status_str = status_summary(battle_state.get("player_statuses", {}))
    p_shield_str = f"  🛡️{player_shield}" if player_shield > 0 else ""
    embed.add_field(
        name="🧙 You",
        value=f"`{hp_bar(player_hp,player_max)}` {player_hp}/{player_max}{p_shield_str}\n{energy_pips(energy,max_energy)} {energy}/{max_energy}⚡",
        inline=True,
    )
    if player_status_str:
        embed.add_field(name="🩹 Statuses", value=player_status_str, inline=False)
    hand = battle_state.get("hand", [])
    card_levels = battle_state.get("card_levels", {})
    if hand:
        hand_str = ""
        for i, card_id in enumerate(hand[:4]):
            card = get_card(card_id)
            if card:
                can   = "✅" if card["cost"] <= energy else "❌"
                lvl   = card_levels.get(card_id, 1)
                stars = f" ⭐Lv.{lvl}" if lvl > 1 else ""
                hand_str += f"{can} {card['emoji']} **{card['name']}**{stars} `{card['cost']}⚡`\n"
        embed.add_field(name="🃏 Hand", value=hand_str or "Empty", inline=False)
    log = battle_state.get("log", [])
    if log:
        embed.add_field(name="📜", value="\n".join(log[-4:]), inline=False)
    embed.set_footer(text=f"Deck: {len(battle_state.get('deck',[]))} cards · Play cards then Pass Turn · Flee costs 10 Ƶ")
    return embed


# ---------------------------------------------------------------------------
# BATTLE RESULT Embed
# ---------------------------------------------------------------------------

def battle_result_embed(won: bool, drops: dict, xp_result: dict, enemy_name: str) -> discord.Embed:
    if won:
        embed = discord.Embed(title="✅  Victory!", description=f"You defeated **{enemy_name}**.", color=COLOR_SUCCESS)
        reward_lines = []
        if drops.get("zet", 0) > 0:
            reward_lines.append(f"💰 +{drops['zet']} Ƶ")
        for card_id in drops.get("cards", []):
            card = get_card(card_id)
            if card:
                reward_lines.append(f"🃏 **{card['name']}** [{card['rarity'].title()}]")
        for item_id in drops.get("items", []):
            item = get_item(item_id)
            if item:
                reward_lines.append(f"{item['emoji']} **{item['name']}**")
        if xp_result.get("xp_gained"):
            reward_lines.append(f"⭐ +{xp_result['xp_gained']} XP")
        if reward_lines:
            embed.add_field(name="🎁 Rewards", value="\n".join(reward_lines), inline=False)
        if xp_result.get("leveled_up"):
            embed.add_field(name="🎊 Level Up!", value=f"You are now **Level {xp_result['new_level']}**!", inline=False)
            upgraded = xp_result.get("upgraded_cards", [])
            if upgraded:
                unique = list(dict.fromkeys(upgraded))
                embed.add_field(
                    name="🃏 Cards Leveled Up!",
                    value="\n".join(f"• {name}" for name in unique[:10]),
                    inline=False,
                )
    else:
        embed = discord.Embed(
            title="💀  Defeated",
            description=f"**{enemy_name}** put you down. You wake up at the inn — bruised, lighter, alive.",
            color=COLOR_DEATH,
        )
        embed.add_field(name="Cost", value="Respawned at 25% HP. Lost 10 Ƶ.", inline=False)
    embed.set_footer(text="Return to the city.")
    return embed


# ---------------------------------------------------------------------------
# DIALOGUE Embeds
# ---------------------------------------------------------------------------

def dialogue_embed(npc: dict, relationship, reply: str, player_name: str, player_message: str = "") -> discord.Embed:
    rel_level = relationship.relationship_level if relationship else "Stranger"
    visits    = relationship.visit_count if relationship else 0
    color     = 0x3A3A5C if npc["id"] == "shade" else COLOR_DIALOGUE
    embed     = discord.Embed(color=color)
    embed.set_author(name=f"{npc['name']}  ·  {npc['role']}  ·  {rel_level}")
    if player_message:
        embed.description = f"**{player_name}:** *\"{player_message}\"*\n\n{npc['emoji']} **{npc['name']}:**\n> {reply}"
    else:
        embed.description = f"{npc['emoji']} **{npc['name']}:**\n> {reply}"
    bar = "█" * min(10, visits) + "░" * max(0, 10 - visits)
    embed.set_footer(text=f"Trust: {bar}  ·  {rel_level}  ·  {visits} conversations")
    return embed


def dialogue_opening_embed(npc: dict) -> discord.Embed:
    opening = random.choice(npc.get("opening_lines", ["..."]))
    color   = 0x3A3A5C if npc["id"] == "shade" else COLOR_DIALOGUE
    embed   = discord.Embed(color=color)
    embed.set_author(name=f"{npc['name']}  ·  {npc['role']}")
    embed.description = f"{npc['emoji']} **{npc['name']}:**\n> {opening}"
    embed.set_footer(text="Choose a reply below, or type freely.")
    return embed


def milestone_scene_embed(npc: dict, scene: dict) -> discord.Embed:
    color = 0x3A3A5C if npc.get("id") == "shade" else COLOR_DIALOGUE
    embed = discord.Embed(color=color)
    embed.set_author(name=f"{npc['emoji']}  {npc['name']}  ·  {scene['title']}")
    embed.description = scene["text"]
    embed.set_footer(text=scene.get("footer", "A moment passes between you."))
    return embed


# ---------------------------------------------------------------------------
# INVENTORY Embed
# ---------------------------------------------------------------------------

def inventory_embed(
    inventory: list[dict],
    page: int = 0,
    capacity: int = 20,
    slot_count: int = 0,
) -> discord.Embed:
    items_per_page = 8
    start          = page * items_per_page
    page_items     = inventory[start:start + items_per_page]
    total_pages    = max(1, -(-len(inventory) // items_per_page))

    pct = slot_count / max(capacity, 1)
    if pct >= 1.0:
        color = COLOR_BATTLE
    elif pct >= 0.75:
        color = COLOR_WARNING
    else:
        color = COLOR_MAIN

    cap_bar = "█" * int(pct * 10) + "░" * (10 - int(pct * 10))
    title   = f"🎒  Bag  ·  {slot_count}/{capacity} slots"

    embed = discord.Embed(title=title, color=color)
    embed.description = f"`{cap_bar}` {slot_count}/{capacity} slots used"

    if slot_count >= capacity:
        embed.description += "\n⚠️ **Bag full!** Buy a bigger bag from the Market Quarter."

    if not page_items:
        embed.add_field(name="", value="*Your bag is empty.*", inline=False)
    else:
        for entry in page_items:
            item = get_item(entry["item_id"])
            if item:
                type_tag = ""
                if item.get("type") == "bag_upgrade":
                    type_tag = " _(Bag Upgrade)_"
                elif item.get("type") == "key_item":
                    type_tag = " _(Key Item)_"
                elif item.get("hp_restore"):
                    type_tag = f" _(+{item['hp_restore']} HP)_"
                embed.add_field(
                    name=f"{item['emoji']} {item['name']} ×{entry['quantity']}{type_tag}",
                    value=f"_{item['description']}_",
                    inline=False,
                )
    embed.set_footer(text=f"Page {page+1}/{total_pages}  ·  Upgrades at the Market Quarter")
    return embed


# ---------------------------------------------------------------------------
# CARD COLLECTION Embed
# ---------------------------------------------------------------------------

def card_collection_embed(collection: list[dict], page: int = 0) -> discord.Embed:
    TYPE_EMOJI  = {"attack": "⚔️", "defense": "🛡️", "skill": "✨"}
    ITEMS_PER_PAGE = 6

    total_pages = max(1, -(-len(collection) // ITEMS_PER_PAGE))
    page_items  = collection[page * ITEMS_PER_PAGE:(page + 1) * ITEMS_PER_PAGE]

    embed = discord.Embed(
        title=f"🃏  Card Collection  ·  {len(collection)} cards",
        color=COLOR_MAIN,
    )

    if not page_items:
        embed.description = "*No cards yet. Win battles and buy from Vex to build your collection.*"
        embed.set_footer(text="Cards auto-level as your character levels up")
        return embed

    for entry in page_items:
        card = get_card(entry["card_id"])
        if not card:
            continue

        level       = entry.get("level", 1)
        rarity_tag  = RARITY_EMOJI.get(card["rarity"], "⬜")
        type_tag    = TYPE_EMOJI.get(card.get("type", "attack"), "🃏")
        level_stars = "⭐" * level + f"  Lv.{level}"
        restriction = card.get("class_restriction")
        class_tag   = restriction.title() if restriction else "Any class"
        qty_tag     = f" ×{entry['quantity']}" if entry["quantity"] > 1 else ""

        effect    = card.get("effect", {})
        etype     = effect.get("type", "")
        bonus_pct = int((level - 1) * 15)
        scale_tag = (
            f"  _(+{bonus_pct}% at Lv.{level})_"
            if level > 1 and etype in ("damage", "magic_damage", "heal", "shield")
            else ""
        )

        embed.add_field(
            name=(
                f"{card['emoji']} **{card['name']}**{qty_tag}  ·  "
                f"{rarity_tag} {card['rarity'].title()}  ·  {level_stars}"
            ),
            value=(
                f"{type_tag} {card.get('type','attack').title()}  ·  "
                f"`{card['cost']}⚡`  ·  {class_tag}{scale_tag}\n"
                f"_{card['description']}_"
            ),
            inline=False,
        )

    embed.set_footer(text=f"Page {page + 1}/{total_pages}  ·  Cards auto-level as you level up")
    return embed


# ---------------------------------------------------------------------------
# PROFILE Embed
# ---------------------------------------------------------------------------

def profile_embed(player, level_up_pending: bool = False) -> discord.Embed:
    prog      = player.progression
    stats     = player.stats
    race      = RACES.get(player.race_id, {})
    cls       = CLASSES.get(player.class_id, {})
    max_hp    = stats.vit * 5
    xp_needed = prog.xp_to_next()
    embed     = discord.Embed(title=f"👤  {player.character_name}", color=COLOR_MAIN)
    embed.add_field(
        name="Identity",
        value=(
            f"{race.get('emoji','')} **{race.get('name','?')}**  ·  "
            f"{cls.get('emoji','')} **{cls.get('name','?')}**\n"
            f"📍 {ZONES.get(prog.current_zone_id, {}).get('name','?')}"
        ),
        inline=False,
    )
    embed.add_field(
        name=f"Level {prog.level}",
        value=f"`{hp_bar(prog.xp, xp_needed)}` {prog.xp:,}/{xp_needed:,} XP",
        inline=True,
    )
    embed.add_field(
        name="Vitals",
        value=f"❤️ {prog.current_hp}/{max_hp} HP\n💰 {prog.zet_wallet:,} Ƶ",
        inline=True,
    )
    embed.add_field(
        name="Stats",
        value=(
            f"⚔️ STR **{stats.strength}**  🛡️ DEF **{stats.defense}**\n"
            f"💨 AGI **{stats.agility}**  🔮 INT **{stats.intel}**\n"
            f"💚 VIT **{stats.vit}** → {max_hp}HP  🍀 LCK **{stats.lck}**"
        ),
        inline=False,
    )
    embed.add_field(name="Passive", value=race.get("passive","None"), inline=False)
    if stats.unspent_points > 0:
        embed.add_field(
            name="⚠️ Unspent Points",
            value=f"**{stats.unspent_points}** stat points available!",
            inline=False,
        )
    embed.set_footer(text="Your story continues in Ironhaven.")
    return embed


# ---------------------------------------------------------------------------
# MAP Embed
# ---------------------------------------------------------------------------

MAP_ASCII = """```
         [RESIDENTIAL]
               │
[FARMLANDS]──[TOWN SQUARE]──[MARKET QUARTER]
               │
        [PORT DISTRICT]──[HARBOUR DOCKS]──[COVE]──[SEA CAVES]
               │
       [SMUGGLERS TRAIL]──[ASHWOOD FOREST]──[CURSED GROVE]
                                  │
                           [ANCIENT RUINS]──[SHADOW DEN]
```"""


def map_embed(player) -> discord.Embed:
    current_zone = player.progression.current_zone_id
    zone_data    = ZONES.get(current_zone, {})
    embed = discord.Embed(title="🗺️  Ironhaven", description=MAP_ASCII, color=COLOR_MAIN)
    embed.add_field(
        name="📍 You",
        value=f"**{zone_data.get('name','?')}**  ·  {SEC_ICONS.get(zone_data.get('security','high'),'')} {zone_data.get('security','').title()}",
        inline=False,
    )
    legend = "\n".join(
        f"{SEC_ICONS[k]} **{k.title()}** — {v}"
        for k, v in {
            "high": "Safe. Guards patrol.",
            "medium": "Some risk.",
            "low": "Dangerous. No law.",
            "null": "Lawless. Fight to survive.",
            "bumpyard": "Endgame. Lethal.",
        }.items()
    )
    embed.add_field(name="Security", value=legend, inline=False)
    return embed


# ---------------------------------------------------------------------------
# SHOP Embed
# ---------------------------------------------------------------------------

def shop_embed(shop: dict, player_zet: int) -> discord.Embed:
    npc_id = shop.get("npc_id")
    npc    = NPCS.get(npc_id, {}) if npc_id else {}
    embed  = discord.Embed(title=f"{npc.get('emoji','🏪')}  {shop['name']}", color=COLOR_MAIN)
    embed.add_field(name="💰 Wallet", value=f"{player_zet:,} Ƶ", inline=False)
    for entry in shop.get("stock", []):
        price = entry.get("price", 0)
        can   = "✅" if player_zet >= price else "❌"
        if "item_id" in entry:
            item = get_item(entry["item_id"])
            if item:
                embed.add_field(name=f"{can} {item['emoji']} {item['name']} — {price:,} Ƶ", value=f"_{item['description']}_", inline=False)
        elif "card_id" in entry:
            card = get_card(entry["card_id"])
            if card:
                embed.add_field(name=f"{can} {card['emoji']} {card['name']} [{card['rarity'].title()}] — {price:,} Ƶ", value=f"_{card['description']}_ · {card['cost']}⚡", inline=False)
    embed.set_footer(text="Click to purchase.")
    return embed


# ---------------------------------------------------------------------------
# STORYLET Embed
# ---------------------------------------------------------------------------

def storylet_embed(storylet: dict) -> discord.Embed:
    return discord.Embed(
        title=f"📜  {storylet['title']}",
        description=storylet["description"],
        color=COLOR_WARNING,
    )


# ---------------------------------------------------------------------------
# CHARACTER CREATION Embeds
# ---------------------------------------------------------------------------

def char_creation_race_embed() -> discord.Embed:
    embed = discord.Embed(
        title="⚓  You arrive in Ironhaven",
        description=(
            "*The ship docks without ceremony. Nobody asks where you came from. "
            "In this city, origins are a luxury most people can't afford.*\n\n"
            "**Choose your Race:**"
        ),
        color=COLOR_MAIN,
    )
    for race in RACES.values():
        embed.add_field(name=f"{race['emoji']} {race['name']}", value=f"_{race['passive']}_", inline=False)
    embed.set_footer(text="Step 1 of 3 — Race")
    return embed


def char_creation_class_embed(race_id: str) -> discord.Embed:
    race  = RACES[race_id]
    embed = discord.Embed(
        title=f"{race['emoji']} {race['name']} — Choose Your Class",
        description="Your class shapes how you fight and who you are.",
        color=COLOR_MAIN,
    )
    for cls in CLASSES.values():
        embed.add_field(name=f"{cls['emoji']} {cls['name']}", value=f"_{cls['archetype']}_", inline=False)
    embed.set_footer(text="Step 2 of 3 — Class")
    return embed


def char_creation_confirm_embed(race_id: str, class_id: str, char_name: str) -> discord.Embed:
    race  = RACES[race_id]
    cls   = CLASSES[class_id]
    embed = discord.Embed(
        title=f"✅  {char_name} is ready.",
        description="*The city doesn't know you yet. That's about to change.*",
        color=COLOR_SUCCESS,
    )
    embed.add_field(name="Race",  value=f"{race['emoji']} {race['name']}", inline=True)
    embed.add_field(name="Class", value=f"{cls['emoji']} {cls['name']}",  inline=True)
    embed.add_field(name="Starting Zone", value="🏛️ Town Square, Ironhaven", inline=False)
    embed.set_footer(text="Your story begins.")
    return embed


# ---------------------------------------------------------------------------
# BUILDING Embed
# ---------------------------------------------------------------------------

def building_embed(building: dict) -> discord.Embed:
    embed = discord.Embed(
        title=f"{building['emoji']}  {building['name']}",
        description=building["description"],
        color=COLOR_MAIN,
    )
    if building.get("npc"):
        npc = NPCS.get(building["npc"])
        if npc:
            embed.add_field(name="👤 Inside", value=f"{npc['emoji']} **{npc['name']}** — {npc['role']}", inline=False)
    return embed


def error_embed(message: str) -> discord.Embed:
    return discord.Embed(title="⚠️", description=message, color=COLOR_WARNING)


# ---------------------------------------------------------------------------
# QUEST Embeds
# ---------------------------------------------------------------------------

def quest_offer_embed(npc: dict, quest: dict) -> discord.Embed:
    color      = 0x3A3A5C if npc["id"] == "shade" else COLOR_WARNING
    type_icons = {"errand": "📦 Errand", "investigation": "🔍 Investigation", "intervention": "🤝 Intervention"}
    quest_type = type_icons.get(quest.get("type","errand"), "📋 Quest")
    embed      = discord.Embed(
        title=f"{npc['emoji']}  {npc['name']}  —  {quest['title']}",
        color=color,
    )
    embed.set_author(name=f"{quest_type}  ·  {npc['role']}")
    embed.description = quest["briefing"]
    rewards = []
    if quest.get("xp"):
        rewards.append(f"⭐ {quest['xp']} XP")
    if quest.get("zet"):
        rewards.append(f"💰 {quest['zet']} Ƶ")
    rewards.append(f"💜 +{quest.get('relationship_gain', 0)} relationship")
    embed.add_field(name="Rewards", value="  ·  ".join(rewards), inline=False)
    embed.set_footer(text="Accept to begin. Decline to come back later.")
    return embed


def quest_active_embed(npc: dict, quest: dict, progress: dict) -> discord.Embed:
    from game.quests import get_quest_progress_display
    color = 0x3A3A5C if npc["id"] == "shade" else COLOR_MAIN
    embed = discord.Embed(title=f"{npc['emoji']}  {quest['title']}", color=color)
    embed.set_author(name=f"Active Quest  ·  {npc['name']}")
    embed.add_field(name="Objective", value=quest["objective"], inline=False)
    embed.add_field(name="Progress", value=get_quest_progress_display(progress, quest), inline=False)
    embed.set_footer(text="Complete the objective and return to claim your reward.")
    return embed


def quest_complete_embed(npc: dict, quest: dict, result: dict) -> discord.Embed:
    color = 0x3A3A5C if npc["id"] == "shade" else COLOR_SUCCESS
    embed = discord.Embed(title=f"✅  {quest['title']}  —  Complete", color=color)
    embed.set_author(name=f"{npc['emoji']} {npc['name']}")
    embed.description = quest["completion_line"]
    reward_lines = []
    if result.get("xp_gained"):
        reward_lines.append(f"⭐ +{result['xp_gained']} XP")
    if result.get("zet_gained"):
        reward_lines.append(f"💰 +{result['zet_gained']} Ƶ")
    if result.get("relationship_gain"):
        reward_lines.append(f"💜 +{result['relationship_gain']} relationship with {npc['name']}")
    if reward_lines:
        embed.add_field(name="Rewards", value="\n".join(reward_lines), inline=False)
    if result.get("leveled_up"):
        embed.add_field(name="🎊 Level Up!", value=f"You reached **Level {result['new_level']}**!", inline=False)
    embed.set_footer(text="Return to continue your journey.")
    return embed


def quest_log_embed(quest_log: dict, player) -> discord.Embed:
    embed   = discord.Embed(title="📋  Quest Log", color=COLOR_MAIN)
    active  = quest_log.get("active", [])
    completed_count = quest_log.get("completed_count", 0)
    if not active:
        embed.description = (
            "*No active quests. Talk to people around Ironhaven — "
            "they usually have something they need help with.*"
        )
    else:
        from game.quests import get_quest_progress_display, _all_objectives_met
        for quest_data, quest_row in active:
            npc       = NPCS.get(quest_data.get("giver_npc",""), {})
            npc_name  = npc.get("name","Unknown")
            npc_emoji = npc.get("emoji","👤")
            all_done  = _all_objectives_met(quest_row.progress)
            if all_done:
                status = f"✅ **Done! Return to {npc_name} to complete.**"
            else:
                status = get_quest_progress_display(quest_row.progress, quest_data)
            embed.add_field(
                name=f"{npc_emoji} {quest_data['title']}  ·  {npc_name}",
                value=f"_{quest_data['objective']}_\n{status}",
                inline=False,
            )
    embed.set_footer(text=f"{len(active)} active  ·  {completed_count} completed  ·  Talk to NPCs to get quests")
    return embed


def quest_detail_embed(npc: dict, quest: dict, progress: dict) -> discord.Embed:
    from game.quests import get_quest_progress_display
    type_icons = {"errand": "📦 Errand", "investigation": "🔍 Investigation", "intervention": "🤝 Intervention"}
    quest_type = type_icons.get(quest.get("type", "errand"), "📋 Quest")
    color      = 0x3A3A5C if npc["id"] == "shade" else COLOR_MAIN

    embed = discord.Embed(title=f"{npc['emoji']}  {quest['title']}", color=color)
    embed.set_author(name=f"{quest_type}  ·  {npc['name']}  ·  {npc['role']}")
    embed.description = quest["briefing"]
    embed.add_field(name="📌 Objective", value=quest["objective"], inline=False)
    embed.add_field(name="📊 Progress", value=get_quest_progress_display(progress, quest), inline=False)
    rewards = []
    if quest.get("xp"):
        rewards.append(f"⭐ {quest['xp']} XP")
    if quest.get("zet"):
        rewards.append(f"💰 {quest['zet']} Ƶ")
    rewards.append(f"💜 +{quest.get('relationship_gain', 0)} relationship")
    embed.add_field(name="🎁 Rewards", value="  ·  ".join(rewards), inline=False)
    embed.set_footer(text="Return to the NPC to hand in once complete.")
    return embed


def stat_allocation_embed(player, message: str = "") -> discord.Embed:
    prog   = player.progression
    stats  = player.stats
    race   = RACES.get(player.race_id, {})
    cls    = CLASSES.get(player.class_id, {})
    max_hp = stats.vit * 5

    embed = discord.Embed(
        title=f"⚡  Allocate Stat Points  —  {player.character_name}",
        color=COLOR_WARNING,
    )
    embed.add_field(
        name="Unspent Points",
        value=f"**{stats.unspent_points}** point{'s' if stats.unspent_points != 1 else ''} to spend",
        inline=False,
    )
    embed.add_field(
        name="Current Stats",
        value=(
            f"⚔️ **STR** {stats.strength}  ·  🛡️ **DEF** {stats.defense}  ·  "
            f"💨 **AGI** {stats.agility}  ·  🔮 **INT** {stats.intel}\n"
            f"💚 **VIT** {stats.vit} → {max_hp} HP  ·  🍀 **LCK** {stats.lck}"
        ),
        inline=False,
    )
    embed.add_field(
        name="What each stat does",
        value=(
            "⚔️ **STR** — Attack damage\n"
            "🛡️ **DEF** — Damage reduction\n"
            "💨 **AGI** — Bluff success chance, turn order\n"
            "🔮 **INT** — Special card effects\n"
            "💚 **VIT** — Max HP (+5 per point)\n"
            "🍀 **LCK** — Drop rates, rare finds"
        ),
        inline=False,
    )
    if message:
        embed.add_field(name="", value=message, inline=False)
    embed.set_footer(text="Each point is permanent. Choose carefully.")
    return embed


# ---------------------------------------------------------------------------
# ONBOARDING Embeds
# ---------------------------------------------------------------------------

def onboarding_arrival_embed(char_name: str) -> discord.Embed:
    embed = discord.Embed(title="⚓  You arrive in Ironhaven", color=0x1A1A2E)
    embed.description = (
        f"*The ship docks without ceremony.*\n\n"
        f"Nobody asks where you came from. In Ironhaven, that's not unusual — "
        f"the city has been filling up with people who don't talk about their past "
        f"for eleven years now, ever since Mercer arrived and made the past "
        f"something worth leaving behind.\n\n"
        f"The city rises above the harbour. Proper walls, proper towers, "
        f"the kind of organized weight that takes decades to build. "
        f"Everything looks functional. Everything looks controlled.\n\n"
        f"There's a portrait on the eastern wall of the square. "
        f"A man in a merchant's coat, looking satisfied. "
        f"His name is Mercer. He runs the bank, sets the prices, "
        f"takes forty percent of every harvest.\n\n"
        f"*This is Ironhaven. You've arrived at an interesting time, **{char_name}.***"
    )
    embed.set_footer(text="1 / 4  ·  Continue to learn how to play")
    return embed


def onboarding_explore_embed() -> discord.Embed:
    embed = discord.Embed(title="🚶  How to Explore", color=COLOR_MAIN)
    embed.description = (
        "Ironhaven is made of zones — each one with its own atmosphere, "
        "people, and dangers. Three buttons move you through the world:"
    )
    embed.add_field(
        name="🚶 Walk",
        value=(
            "Move through your current zone one step at a time. "
            "Things happen as you walk — scenes, conversations, discoveries, encounters. "
            "**This is how you explore.** Tap it often."
        ),
        inline=False,
    )
    embed.add_field(
        name="🏪 Visit",
        value=(
            "Enter a building in your current zone. "
            "Shops, the tavern, the training grounds, the clinic — "
            "each one has someone inside worth knowing."
        ),
        inline=False,
    )
    embed.add_field(
        name="🗺️ Travel",
        value=(
            "Move to a different zone entirely. "
            "Ironhaven has twelve zones — from the controlled Town Square "
            "to the lawless Ancient Ruins. Each is different."
        ),
        inline=False,
    )
    embed.set_footer(text="2 / 4  ·  Continue")
    return embed


def onboarding_people_embed() -> discord.Embed:
    embed = discord.Embed(title="👥  The People", color=COLOR_DIALOGUE)
    embed.description = (
        "The most important thing in Ironhaven isn't the combat or the economy. "
        "It's the people.\n\n"
        "Every NPC in this city has a real life, real problems, "
        "and things they won't say directly — at first."
    )
    embed.add_field(
        name="💬 Talk to people",
        value=(
            "Find NPCs by visiting buildings or walking until you encounter them. "
            "Talk to them. Come back. Trust builds over time, not in a single conversation."
        ),
        inline=False,
    )
    embed.add_field(
        name="📋 Quests come from relationships",
        value=(
            "There's no bulletin board. NPCs offer quests when they trust you enough. "
            "The more you talk to someone, the more they share — "
            "and the more they ask for your help."
        ),
        inline=False,
    )
    embed.add_field(
        name="⚔️ Combat and leveling",
        value=(
            "Low and Null Security zones have enemies. Fighting them earns XP and cards. "
            "Walking earns XP too. Your level determines which zones you can safely enter."
        ),
        inline=False,
    )
    embed.set_footer(text="3 / 5  ·  Continue")
    return embed


def onboarding_inventory_embed() -> discord.Embed:
    embed = discord.Embed(title="🎒  Your Character", color=COLOR_MAIN)
    embed.description = (
        "The bottom two rows of buttons are always available — "
        "check on yourself any time without leaving the zone."
    )
    embed.add_field(
        name="🎒 Bag",
        value=(
            "Your inventory. Items you find while walking, buy from shops, "
            "or receive as quest rewards end up here. "
            "Potions restore HP. Some items are story-relevant — don't sell everything."
        ),
        inline=False,
    )
    embed.add_field(
        name="👤 Profile",
        value=(
            "Your character sheet — level, XP progress, HP, Ƶ wallet, and stats. "
            "Also shows your card collection. "
            "Every few levels you get unspent points to allocate. "
            "STR boosts attack · VIT boosts HP · AGI improves bluffing · LCK improves drops."
        ),
        inline=False,
    )
    embed.add_field(
        name="🗺️ Map",
        value=(
            "The full map of Ironhaven with security levels shown. "
            "🟢 High — safe, guards patrol  "
            "🟠 Low — enemies spawn, PvP on  "
            "🔴 Null — lawless, fight to survive. "
            "Your level determines where you can safely go."
        ),
        inline=False,
    )
    embed.add_field(
        name="📋 Quests",
        value=(
            "Your active quest log. Shows every quest in progress, "
            "the objective, and what you've completed so far. "
            "Check here whenever you forget where to go next."
        ),
        inline=False,
    )
    embed.set_footer(text="4 / 5  ·  Continue")
    return embed


def onboarding_rel_embed() -> discord.Embed:
    embed = discord.Embed(title="🥋  Captain Rel", color=0x2C2C3E)
    embed.description = (
        "A figure at the training ground turns when you enter the square.\n\n"
        "Not toward you specifically. Just — turns. Aware.\n\n"
        "*\"New face.\"*\n\n"
        "He crosses the yard at the pace of someone who decided long ago "
        "exactly how fast he needs to move, and has been right about it ever since.\n\n"
        "*\"Rel. Captain, technically — mostly historical now. "
        "I ran operations under the old Council. "
        "Before Mercer\'s appointments replaced everyone useful with everyone loyal.\"*\n\n"
        "He looks at you. Waiting."
    )
    embed.set_footer(text="5 / 5  ·  Ask what you want to know")
    return embed


REL_ANSWERS = {
    "ironhaven": (
        "*\"Ironhaven used to be independent. "
        "Proper port — ships from everywhere, real trade. "
        "Eleven years ago Mercer arrived with a bank charter and a Council seat. "
        "By the time anyone understood what was happening, he had both.\"*\n\n"
        "He glances at the portrait on the eastern wall.\n\n"
        "*\"That wasn\'t there before. Small detail. Tells you everything.\n\n"
        "Now he controls the loans, the supply lines, the prices. "
        "Forty percent of every harvest goes to his ledgers "
        "before the farmer touches a single grain. "
        "The Council still meets — they just vote the way they\'re told.\"*"
    ),
    "mercer": (
        "*\"Smart man. Patient. He didn\'t take anything by force — "
        "he made himself necessary first. "
        "The bank, the import licenses, the debt restructuring. "
        "By the time people were struggling, he was the only one offering help.\n\n"
        "The help came with terms.\"*\n\n"
        "Rel is quiet for a moment.\n\n"
        "*\"I\'ve been watching him for eleven years. "
        "He\'s not greedy — greedy people make mistakes. "
        "He\'s thorough. There\'s a difference.\"*"
    ),
    "people": (
        "*\"Tomás at the general store in the Market Quarter. "
        "Thirty years here, knows everyone, charges fairly. "
        "Worth earning his trust.\n\n"
        "Hana at the clinic. Precise. "
        "Everyone comes to her eventually — she notices everything.\n\n"
        "Maren at the harbour office. "
        "If anything moves through this city she\'s tracked it. "
        "Don\'t waste her time and she won\'t waste yours.\"*\n\n"
        "*\"Pay attention to what people don\'t say. "
        "That\'s where the real information is.\"*"
    ),
    "watchout": (
        "*\"Port district is fine — lighter patrol, people mind their own business. "
        "Market Quarter is safe. Town Square is watched constantly.\n\n"
        "The forest — stay out until you know what you\'re doing. "
        "There are things out there not on any official map.\"*\n\n"
        "He says it plainly. Not to frighten. Because he means it.\n\n"
        "*\"Learn the city first. It will tell you what\'s happening "
        "if you pay attention.\"*"
    ),
}


def onboarding_rel_answer_embed(question: str) -> discord.Embed:
    embed = discord.Embed(title="🥋  Captain Rel", color=0x2C2C3E)
    embed.description = REL_ANSWERS.get(question, "*\"Ask me something else.\"*")
    embed.set_footer(text="Keep asking, or tell him you're ready to help")
    return embed


# ---------------------------------------------------------------------------
# ADVENTURER'S GUILD Embeds
# ---------------------------------------------------------------------------

def guild_embed() -> discord.Embed:
    embed = discord.Embed(title="📋  Adventurer's Guild", color=COLOR_MAIN)
    embed.description = (
        "The Guild board has today's contracts posted. "
        "Complete them for guaranteed XP and Ƶ rewards."
    )
    embed.add_field(
        name="📋 Daily Contracts",
        value="Three contracts per day — Bronze, Silver, Gold. Reset at midnight UTC.",
        inline=False,
    )
    embed.add_field(
        name="🏆 Leaderboard",
        value="Top adventurers by level and XP.",
        inline=False,
    )
    embed.set_footer(text="You can hold up to 3 active contracts at once.")
    return embed


def guild_contracts_embed(daily_contracts: list, player_contracts: list) -> discord.Embed:
    from game.guild import TIER_CONFIG
    embed = discord.Embed(title="📋  Daily Contracts", color=COLOR_MAIN)
    embed.description = "Complete these for XP and Ƶ rewards. Resets at midnight UTC."

    player_contract_ids = {row.contract_id: row for row, _ in player_contracts}

    for contract in daily_contracts:
        tier_cfg = TIER_CONFIG[contract.tier]
        player_c = player_contract_ids.get(contract.id)

        if player_c is None:
            status_str   = "Available"
            status_emoji = "⬜"
        elif player_c.status == "active":
            status_str   = f"In Progress ({player_c.progress}/{contract.target_count})"
            status_emoji = "🔄"
        elif player_c.status == "completed":
            status_str   = "✅ Complete — Claim Reward!"
            status_emoji = "✅"
        else:
            status_str   = "Claimed"
            status_emoji = "☑️"

        embed.add_field(
            name=f"{tier_cfg['emoji']} {contract.tier.title()} Contract  ·  {status_emoji} {status_str}",
            value=(
                f"_{contract.description}_\n"
                f"⭐ {contract.reward_xp} XP  ·  💰 {contract.reward_zet} Ƶ"
            ),
            inline=False,
        )

    if not daily_contracts:
        embed.description = "*No contracts available today. Check back later.*"

    embed.set_footer(text="Accept contracts below · Claim when complete")
    return embed


def guild_leaderboard_embed(rows: list) -> discord.Embed:
    embed = discord.Embed(title="🏆  Leaderboard", color=COLOR_WARNING)
    if not rows:
        embed.description = "*No adventurers yet. Be the first.*"
    else:
        medals = ["🥇", "🥈", "🥉"]
        lines  = []
        for i, (name, level, xp) in enumerate(rows):
            medal = medals[i] if i < 3 else f"**{i+1}.**"
            lines.append(f"{medal} **{name}**  ·  Lv.{level}  ·  {xp:,} XP")
        embed.description = "\n".join(lines)
    embed.set_footer(text="Rankings by level and XP")
    return embed


# ---------------------------------------------------------------------------
# AUCTION HOUSE / MARKET Embeds
# ---------------------------------------------------------------------------

def market_browse_embed(
    listings: list,
    seller_names: dict,
    filter_type: str = "all",
    sort: str = "recent",
    page: int = 0,
    total: int = 0,
    viewer_id: int = 0,
) -> discord.Embed:
    from game.data import get_item
    from game.market import PAGE_SIZE
    total_pages = max(1, -(-total // PAGE_SIZE))

    SORT_LABELS = {
        "recent":    "🆕 Recent",
        "cheapest":  "💰 Cheapest",
        "expensive": "💎 Expensive",
        "expiring":  "⏳ Expiring Soon",
    }
    embed = discord.Embed(
        title=f"🏷️  Market  ·  {filter_type.title()}  ·  {SORT_LABELS.get(sort, sort)}",
        color=COLOR_MAIN,
    )
    embed.description = f"**{total:,}** listing{'s' if total != 1 else ''} found"

    if not listings:
        embed.description += "\n\n*No listings in this category. Be the first to list!*"
    else:
        from datetime import datetime, timezone as tz
        now = datetime.now(tz.utc)
        for listing in listings:
            item       = get_item(listing.item_id) if listing.item_id else None
            name       = item["name"]  if item else (listing.item_id or "Unknown")
            emoji      = item["emoji"] if item else "📦"
            price_per  = listing.price // max(listing.quantity, 1)
            hours_left = max(0, int((listing.expires_at - now).total_seconds() / 3600)) if listing.expires_at else 48
            seller     = seller_names.get(listing.seller_id, "Unknown")
            is_own     = listing.seller_id == viewer_id
            tag        = " *(your listing)*" if is_own else f" · by **{seller}**"
            embed.add_field(
                name=f"{emoji} {name} ×{listing.quantity}  ·  {price_per:,} Ƶ each  ·  #{listing.id}",
                value=f"Total: **{listing.price:,} Ƶ**  ·  ⏳ {hours_left}h left{tag}",
                inline=False,
            )

    embed.set_footer(text=f"Page {page+1}/{total_pages}  ·  5% fee on listing  ·  48h expiry")
    return embed


def market_my_listings_embed(listings: list, player_zet: int) -> discord.Embed:
    from game.data import get_item
    embed = discord.Embed(title="📦  My Listings", color=COLOR_MAIN)
    embed.add_field(name="💰 Wallet", value=f"{player_zet:,} Ƶ", inline=False)

    if not listings:
        embed.description = "*You have no active listings. List items to earn Ƶ from other players.*"
    else:
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        for listing in listings:
            item       = get_item(listing.item_id)
            name       = item["name"]  if item else (listing.item_id or "Unknown")
            emoji      = item["emoji"] if item else "📦"
            price_per  = listing.price // max(listing.quantity, 1)
            hours_left = max(0, int((listing.expires_at - now).total_seconds() / 3600)) if listing.expires_at else 48
            embed.add_field(
                name=f"{emoji} {name} ×{listing.quantity}  ·  {price_per:,} Ƶ each",
                value=f"Total: **{listing.price:,} Ƶ**  ·  ⏳ {hours_left}h left  ·  ID: #{listing.id}",
                inline=False,
            )

    embed.set_footer(text=f"Max {5} listings · Cancel to reclaim items")
    return embed


def market_list_item_embed(inventory: list, player_zet: int) -> discord.Embed:
    from game.data import get_item
    from game.market import UNLISTED_ITEM_TYPES
    embed = discord.Embed(title="📋  List an Item", color=COLOR_MAIN)
    embed.description = "Select an item from your bag to list on the market."
    embed.add_field(name="💰 Wallet", value=f"{player_zet:,} Ƶ (listing fee: 5%)", inline=False)

    listable = []
    for entry in inventory:
        item = get_item(entry["item_id"])
        if item and item.get("type") not in UNLISTED_ITEM_TYPES:
            listable.append(entry)

    if not listable:
        embed.add_field(
            name="Empty",
            value="*No listable items in your bag. Key items and bag upgrades can't be listed.*",
            inline=False,
        )

    embed.set_footer(text="Listing fee is charged when you list. Item returned if cancelled.")
    return embed


# ---------------------------------------------------------------------------
# NPC SELL Embeds
# ---------------------------------------------------------------------------

def npc_sell_embed(sellable: list, npc: dict, player_zet: int) -> discord.Embed:
    from game.data import get_item
    embed = discord.Embed(
        title=f"{npc['emoji']}  {npc['name']}  — Sell Items",
        color=COLOR_DIALOGUE,
    )
    embed.add_field(name="💰 Wallet", value=f"{player_zet:,} Ƶ", inline=False)

    if not sellable:
        embed.description = "*Nothing in your bag that this NPC will buy right now.*"
    else:
        for entry in sellable[:8]:
            item = get_item(entry["item_id"])
            if item:
                total = entry["buy_price"] * entry["quantity"]
                embed.add_field(
                    name=f"{item['emoji']} {item['name']} ×{entry['quantity']}",
                    value=f"{entry['buy_price']:,} Ƶ each  ·  Total: **{total:,} Ƶ**",
                    inline=False,
                )

    embed.set_footer(text="Specialist NPCs pay full price for certain items · Others pay 70%")
    return embed


# ---------------------------------------------------------------------------
# GATHERING Embeds
# ---------------------------------------------------------------------------

RARITY_COLORS = {
    "common":   COLOR_MAIN,
    "uncommon": COLOR_SUCCESS,
    "rare":     COLOR_WARNING,
}

SKILL_EMOJI = {
    "fishing":    "🎣",
    "mining":     "⛏️",
    "herbalism":  "🌿",
    "scavenging": "🔍",
    "woodcutting":"🪓",
    "excavation": "🏺",
}


def gathering_node_embed(player, zone_data: dict, node: dict) -> discord.Embed:
    from game.gathering import get_skill
    skill     = get_skill(node["skill"])
    rarity    = node.get("rarity", "common")
    color     = RARITY_COLORS.get(rarity, COLOR_MAIN)
    skill_emoji = SKILL_EMOJI.get(node["skill"], "🔍")

    embed = discord.Embed(
        title=f"{node['emoji']}  {node['name']} Spotted",
        description=f"*{node['walk_text']}*",
        color=color,
    )
    embed.add_field(
        name=f"{skill_emoji} {skill['name']}",
        value=(
            f"Rarity: **{rarity.title()}**\n"
            + (f"Requires: **{skill['tool_slot'].replace('_',' ').title()}** equipped" if skill.get("tool_slot") else "No tool required")
        ),
        inline=True,
    )
    prog   = player.progression
    stats  = player.stats
    max_hp = stats.vit * 5
    embed.add_field(
        name="Status",
        value=f"❤️ {prog.current_hp}/{max_hp} HP  ·  💰 {prog.zet_wallet:,} Ƶ",
        inline=True,
    )
    embed.set_footer(text="Gather to collect · Keep Walking to skip")
    return embed


def gathering_result_embed(player, node: dict, result: dict) -> discord.Embed:
    from game.gathering import get_skill, SKILL_MAX_LEVEL, skill_xp_to_next

    skill_id   = node["skill"]
    skill      = get_skill(skill_id)
    skill_res  = result.get("skill_result", {})
    new_level  = skill_res.get("new_level", 1)
    xp_gained  = skill_res.get("skill_xp_gained", 0)
    leveled_up = skill_res.get("leveled_up", False)
    main_xp    = result.get("main_xp", 0)
    skill_emoji = SKILL_EMOJI.get(skill_id, "🔍")

    if result["success"]:
        color = COLOR_SUCCESS
        embed = discord.Embed(
            title=f"{result['item_emoji']}  {skill['verb_past']}!",
            description=f"*{node.get('gather_text', result['message'])}*",
            color=color,
        )
        embed.add_field(
            name="Found",
            value=f"**1× {result['item_emoji']} {result['item_name']}**",
            inline=True,
        )
        xp_line = f"+{xp_gained} {skill_emoji} {skill['name']} XP"
        if main_xp > 0:
            xp_line += f"  ·  +{main_xp} ⭐ XP"
        embed.add_field(name="XP", value=xp_line, inline=True)
        if leveled_up:
            embed.add_field(
                name=f"🎉 {skill['name']} Level Up!",
                value=f"**{skill['name']}** is now **Level {new_level}**! Higher level nodes unlocked.",
                inline=False,
            )
        if new_level < SKILL_MAX_LEVEL:
            threshold  = skill_xp_to_next(new_level)
            current_xp = skill_res.get("xp_remaining", 0)
            pct        = min(1.0, current_xp / max(threshold, 1))
            bar        = "█" * int(pct * 10) + "░" * (10 - int(pct * 10))
            embed.add_field(
                name=f"{skill_emoji} {skill['name']} Lv.{new_level}",
                value=f"`{bar}` {current_xp}/{threshold} XP to next level",
                inline=False,
            )
        else:
            embed.add_field(
                name=f"{skill_emoji} {skill['name']} Lv.{new_level}",
                value="**MAX LEVEL** — Island 1 cap reached.",
                inline=False,
            )
    else:
        color = COLOR_WARNING
        embed = discord.Embed(
            title=f"❌  Couldn't Gather",
            description=result["message"],
            color=color,
        )
        if result.get("need_tool") and result.get("tool_slot"):
            slot = result["tool_slot"].replace("_", " ").title()
            embed.add_field(
                name="🛠️ Need a Tool",
                value=f"Equip a **{slot}** from your bag, then try again.",
                inline=False,
            )

    embed.set_footer(text="Keep walking to find more · Tools can be bought at the Armory")
    return embed


def gathering_skills_embed(skills_data: list[dict]) -> discord.Embed:
    from game.gathering import GATHERING_SKILLS, SKILL_MAX_LEVEL, skill_xp_to_next

    embed = discord.Embed(
        title="⚒️  Gathering Skills",
        color=COLOR_MAIN,
    )

    if not skills_data:
        embed.description = (
            "*No gathering skills yet. Walk through zones to discover nodes "
            "— fishing, mining, herbalism, scavenging, woodcutting, excavation.*"
        )
        embed.set_footer(text="Tools available at the Ironhaven Armory")
        return embed

    skill_map = {s["skill_type"]: s for s in skills_data}

    for skill_id, skill_def in GATHERING_SKILLS.items():
        row   = skill_map.get(skill_id)
        level = row["level"] if row else 1
        xp    = row["xp"]    if row else 0
        emoji = SKILL_EMOJI.get(skill_id, "🔍")
        tool  = skill_def.get("tool_slot")
        tool_tag = f"Needs: {tool.replace('_',' ').title()}" if tool else "No tool required"

        if level >= SKILL_MAX_LEVEL:
            bar      = "█" * 10
            xp_line  = "**MAX**"
        else:
            threshold = skill_xp_to_next(level)
            pct       = min(1.0, xp / max(threshold, 1))
            bar       = "█" * int(pct * 10) + "░" * (10 - int(pct * 10))
            xp_line   = f"{xp}/{threshold} XP"

        embed.add_field(
            name=f"{emoji} {skill_def['name']}  ·  Lv.{level}",
            value=f"`{bar}` {xp_line}\n_{tool_tag}_",
            inline=True,
        )

    embed.set_footer(text="Max level 10 per skill (Island 1) · Walk to gain skill XP")
    return embed


# ---------------------------------------------------------------------------
# MINI-BOSS Embeds  (Phase 3)
# ---------------------------------------------------------------------------

def miniboss_encounter_embed(player, zone_data: dict, enemy: dict) -> discord.Embed:
    prog     = player.progression
    stats    = player.stats
    max_hp   = stats.vit * 5
    embed = discord.Embed(
        title=f"{enemy.get('emoji','⚔️')}  {enemy['name']}  ·  Elite Encounter",
        color=0x8B0000,
    )
    enemy_desc = enemy.get("description", "An elite enemy blocks your path.")
    embed.description = f"*{enemy_desc}*\n\nThis is no ordinary opponent. Proceed carefully."
    hp_display = hp_bar(prog.current_hp, max_hp)
    embed.add_field(
        name=f"Your Status  ·  Lv.{prog.level}",
        value=f"`{hp_display}` **{prog.current_hp}/{max_hp}** HP  ·  💰 **{prog.zet_wallet:,} Ƶ**",
        inline=False,
    )
    enemy_hp = enemy.get("hp", 100)
    embed.add_field(
        name=f"{enemy.get('emoji','⚔️')} {enemy['name']}",
        value=f"HP: **{enemy_hp}**  ·  ATK: **{enemy.get('atk',0)}**  ·  DEF: **{enemy.get('defense',0)}**",
        inline=False,
    )
    embed.add_field(
        name="⚠️ Elite",
        value="Guaranteed rare/epic drops on defeat. Respawns in 6 hours.",
        inline=False,
    )
    embed.set_footer(text=f"{zone_data.get('name', zone_data['id'])}  ·  Elite spawn")
    return embed


def miniboss_defeat_embed(player, enemy: dict, drops: dict, xp_result: dict, announce: str) -> discord.Embed:
    enemy_name = enemy.get("name", "Elite")
    embed = discord.Embed(title=f"⚔️  {enemy_name} Defeated!", color=0xFFD700)
    embed.description = (
        f"*You stand over the fallen {enemy_name}. The zone feels different now.*\n\n"
        f"📣 **Server announcement:** {announce}"
    )
    rewards = []
    if drops.get("zet"):
        rewards.append(f"💰 +{drops['zet']:,} Ƶ")
    for card_id in drops.get("cards", []):
        from game.data import get_card
        card = get_card(card_id)
        if card:
            rewards.append(f"{card['emoji']} {card['name']} *(card)*")
    for item_id in drops.get("items", []):
        from game.data import get_item
        item = get_item(item_id)
        if item:
            rewards.append(f"{item['emoji']} {item['name']}")
    if rewards:
        embed.add_field(name="🏆 Drops", value="\n".join(rewards), inline=False)
    xp = xp_result.get("xp_gained", 0)
    embed.add_field(name="✨ XP", value=f"+{xp} XP", inline=True)
    if xp_result.get("leveled_up"):
        embed.add_field(name="🆙 Level Up!", value=f"Now **Lv.{xp_result['new_level']}**", inline=True)
    embed.set_footer(text="Elite respawns in 6 hours")
    return embed


# ---------------------------------------------------------------------------
# BANK Embed
# ---------------------------------------------------------------------------

def bank_embed(player, bank_balance: int) -> discord.Embed:
    prog  = player.progression
    embed = discord.Embed(
        title="🏦  Mercer Bank",
        description=(
            "*Marble columns. A queue of anxious debtors. "
            "The teller's smile doesn't reach their eyes.*\n\n"
            "Your Ƶ is safe here — for a modest processing fee on withdrawal."
        ),
        color=COLOR_MAIN,
    )
    embed.add_field(name="💰 Wallet",       value=f"**{prog.zet_wallet:,} Ƶ**", inline=True)
    embed.add_field(name="🏦 Bank Balance", value=f"**{bank_balance:,} Ƶ**",    inline=True)
    embed.add_field(
        name="ℹ️ How it works",
        value=(
            "**Deposit** — free, instant.\n"
            "**Withdraw** — Mercer charges **5%** processing fee.\n"
            "Bank balance is safe from PvP losses."
        ),
        inline=False,
    )
    embed.set_footer(text="Minimum 10 Ƶ per transaction")
    return embed


# ---------------------------------------------------------------------------
# COUNCIL HALL Embed
# ---------------------------------------------------------------------------

_COUNCIL_NOTICES = [
    (
        "Revised Licensing Ordinance 44-C",
        "All independent traders in the Port District must renew trading licenses by end of month. "
        "Fee: 200 Ƶ. Non-compliance results in immediate suspension of trading rights.\n"
        "*— Council Secretary, on behalf of the Mercer Trading Company*",
    ),
    (
        "Public Safety — Conservation Zone",
        "Citizens are reminded that Ashwood Forest is strictly off-limits without a Council permit. "
        "Unauthorized entry is a criminal offence. Permit applications: 500 Ƶ processing fee.\n"
        "*— Council, Town Safety Division*",
    ),
    (
        "Harvest Tax Notice — Farmlands",
        "The quarterly harvest assessment takes place on the 15th. "
        "All farmland operators: the standard 40% levy applies. Irregularities will be investigated.\n"
        "*— Revenue Division, Mercer Trading Company*",
    ),
    (
        "Dock Access — New Restrictions",
        "All dock access between 22:00 and 06:00 requires advance written approval. "
        "Applications must be submitted 48 hours in advance.\n"
        "*— Port Authority, Mercer Trading Company*",
    ),
    (
        "Debt Settlement Programme",
        "Citizens with outstanding debt to Mercer Bank may now apply for extended repayment plans. "
        "Interest rates may vary. Terms subject to change without notice.\n"
        "*— Mercer Bank, Ironhaven Branch*",
    ),
]

_COUNCIL_NOTICES_POST_ARC1 = [
    (
        "Emergency Audit — In Progress",
        "A full audit of Mercer Trading Company forest contracts is underway. "
        "Citizens with relevant information may contact the Council Hall directly.\n"
        "*— Independent Oversight Committee*",
    ),
    (
        "Licensing Ordinances — Under Review",
        "Several licensing ordinances are suspended pending the ongoing audit. "
        "Citizens: hold renewal applications until further notice.\n"
        "*— Council Hall*",
    ),
    (
        "Public Statement — Councilmember Aldric",
        "The Council is committed to transparency. All operations affecting Ironhaven citizens "
        "will be reviewed. We thank those who came forward.\n"
        "*— Councilmember Aldric*",
    ),
]


def council_hall_embed(arc1_done: bool = False) -> discord.Embed:
    embed = discord.Embed(
        title="🏛️  Council Hall — Notice Board",
        description=(
            "*Imposing bronze doors, always slightly ajar. "
            "Inside: rows of clerks, stacks of ledgers, "
            "and the specific smell of bureaucracy working for someone else.*"
        ),
        color=COLOR_MAIN,
    )
    notices = _COUNCIL_NOTICES_POST_ARC1 if arc1_done else _COUNCIL_NOTICES
    shown   = random.sample(notices, min(2, len(notices)))
    for title, text in shown:
        embed.add_field(name=f"📋 {title}", value=text, inline=False)
    if arc1_done:
        embed.add_field(
            name="📌 Current Mood",
            value="*The atmosphere in the Hall has shifted. Clerks speak in lower voices.*",
            inline=False,
        )
    embed.set_footer(text="Notices rotate periodically · The Council acts on Mercer's behalf")
    return embed


# ---------------------------------------------------------------------------
# BARN Embeds
# ---------------------------------------------------------------------------

def barn_embed(barn: dict, player) -> discord.Embed:
    from game.data import get_item
    BARN_MAX   = 50
    slots_used = len(barn)
    pct        = slots_used / max(BARN_MAX, 1)
    bar        = "█" * int(pct * 10) + "░" * (10 - int(pct * 10))
    embed = discord.Embed(
        title="🏚️  Farmlands Barn — Community Storage",
        description=(
            f"*Communal storage for the farming community. "
            f"Mercer takes 40% of the harvest — he doesn't take what's in here. Not yet.*\n\n"
            f"`{bar}` **{slots_used}/{BARN_MAX}** item types stored"
        ),
        color=COLOR_MAIN,
    )
    if not barn:
        embed.add_field(name="Empty", value="*Nothing stored yet. Deposit items from your bag.*", inline=False)
    else:
        lines = []
        for item_id, qty in list(barn.items())[:10]:
            item = get_item(item_id)
            if item:
                lines.append(f"{item['emoji']} **{item['name']}** ×{qty}")
        embed.add_field(name="📦 Contents", value="\n".join(lines) or "*Empty*", inline=False)
        if len(barn) > 10:
            embed.add_field(name="", value=f"*…and {len(barn) - 10} more item types*", inline=False)
    embed.add_field(name="💰 Wallet", value=f"{player.progression.zet_wallet:,} Ƶ", inline=True)
    embed.set_footer(text="Key items, equipment, and cosmetics can't be stored · No capacity limit on quantities")
    return embed


def barn_deposit_embed(depositable: list) -> discord.Embed:
    from game.data import get_item
    embed = discord.Embed(
        title="⬇️  Deposit to Barn",
        description="Select an item to store. The full stack will be deposited.",
        color=COLOR_MAIN,
    )
    for entry in depositable[:4]:
        item = get_item(entry["item_id"])
        if item:
            embed.add_field(
                name=f"{item['emoji']} {item['name']} ×{entry['quantity']}",
                value=f"_{item['description'][:80]}_",
                inline=False,
            )
    embed.set_footer(text="Deposits your entire stack of the selected item")
    return embed


def barn_withdraw_embed(barn: dict) -> discord.Embed:
    from game.data import get_item
    embed = discord.Embed(
        title="⬆️  Withdraw from Barn",
        description="Select an item to retrieve. The full stack will be returned to your bag.",
        color=COLOR_MAIN,
    )
    for item_id, qty in list(barn.items())[:4]:
        item = get_item(item_id)
        if item:
            embed.add_field(
                name=f"{item['emoji']} {item['name']} ×{qty}",
                value=f"_{item['description'][:80]}_",
                inline=False,
            )
    embed.set_footer(text="Make sure your bag has a free slot before withdrawing")
    return embed


# ---------------------------------------------------------------------------
# FISH MARKET Embed
# ---------------------------------------------------------------------------

def fish_market_embed(sellable: list, player) -> discord.Embed:
    from game.data import get_item
    embed = discord.Embed(
        title="🐟  Fish Market",
        description=(
            "*The fish market buyers are independent — for now. "
            "They pay honest prices. Unlike everything else in Ironhaven.*"
        ),
        color=COLOR_MAIN,
    )
    embed.add_field(name="💰 Wallet", value=f"{player.progression.zet_wallet:,} Ƶ", inline=False)
    if not sellable:
        embed.add_field(
            name="Nothing to sell",
            value="*You don't have any sellable items. Fish and gathered materials appear here.*",
            inline=False,
        )
    else:
        for entry in sellable[:6]:
            item = get_item(entry["item_id"])
            if item:
                total = entry["sell_price"] * entry["quantity"]
                embed.add_field(
                    name=f"{item['emoji']} {item['name']} ×{entry['quantity']}",
                    value=f"{entry['sell_price']:,} Ƶ each  ·  Total: **{total:,} Ƶ**",
                    inline=False,
                )
    embed.set_footer(text="Sells your full stack · Independent from Mercer's pricing")
    return embed


# ---------------------------------------------------------------------------
# ANCIENT VAULT Embeds
# ---------------------------------------------------------------------------

def vault_embed(zone_cleared: bool, on_cooldown: bool, cd_secs: int = 0) -> discord.Embed:
    from game.respawn import format_respawn_time
    embed = discord.Embed(
        title="🗝️  Ancient Vault",
        description=(
            "*A sealed stone chamber in the deepest part of the ruins. "
            "It was opened recently. Something was taken — or left.*"
        ),
        color=COLOR_MAIN,
    )
    if on_cooldown:
        t = format_respawn_time(cd_secs)
        embed.add_field(
            name="🔒 Recently Looted",
            value=f"The vault was opened not long ago. Resets in **{t}**.",
            inline=False,
        )
        embed.color = COLOR_WARNING
    elif not zone_cleared:
        embed.add_field(
            name="🔒 Vault Sealed",
            value=(
                "The vault won't open while enemies roam the ruins.\n"
                "Clear the zone first — defeat enemies until the zone goes quiet."
            ),
            inline=False,
        )
        embed.color = COLOR_WARNING
    else:
        embed.add_field(
            name="🔓 Vault Open",
            value="The ruins are quiet. The vault can be opened.",
            inline=False,
        )
        embed.color = COLOR_SUCCESS
    embed.set_footer(text="Resets every 6 hours · Rare/Epic/Legendary card inside")
    return embed


def vault_opened_embed(player, card: dict | None, bonus_xp: int, xp_result: dict) -> discord.Embed:
    embed = discord.Embed(
        title="✨  Vault Opened",
        description=(
            "*The stone door grinds. Inside: a chamber untouched for decades. "
            "The air is cold and absolutely still.*"
        ),
        color=COLOR_SUCCESS,
    )
    rewards = []
    if card:
        rewards.append(f"{card['emoji']} **{card['name']}** [{card['rarity'].title()}] — added to deck")
    rewards.append(f"⭐ **+{bonus_xp} XP**")
    embed.add_field(name="🎁 Found Inside", value="\n".join(rewards), inline=False)
    if xp_result.get("leveled_up"):
        embed.add_field(
            name="🆙 Level Up!",
            value=f"You are now **Level {xp_result['new_level']}**!",
            inline=False,
        )
    embed.set_footer(text="The vault seals again for 6 hours")
    return embed