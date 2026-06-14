"""
ui/views.py — Zeta
Complete views file with Walk + Quest + Onboarding + Card Collection systems.
"""
import discord

from core.cache import (
    clear_battle_state,
    clear_char_creation,
    get_battle_state,
    get_char_creation,
    set_battle_state,
    set_char_creation,
    get_step_count,
    increment_step,
    get_total_steps,
    increment_total_steps,
    clear_walk_state,
)
from core.database import get_session
from game.data import (
    CARDS, CLASSES, ENEMIES, ITEMS, NPCS, RACES, SHOPS, ZONES,
    get_card, get_class, get_enemies_in_zone, get_item, get_npc,
    get_npcs_in_zone, get_race, get_shop_for_building, get_zone,
    get_buildings_in_zone,
)
from game.engine import (
    build_initial_battle_state, check_battle_outcome, generate_drops,
    resolve_card, resolve_enemy_turn, tick_start_of_player_turn,
)
from game.walk import process_walk_step
from game.walk_data import get_travel_line
from game.world import (
    add_card_to_collection, add_card_to_deck, add_item, add_xp, add_zet,
    deduct_zet, full_heal_player, get_card_collection, get_card_collection_levels,
    get_deck_list, get_full_player, get_inventory, get_or_create_relationship,
    remove_item, set_flag, update_player_hp, update_player_zone, use_consumable,
)
from ui.embeds import (
    battle_embed, battle_result_embed, building_embed, card_collection_embed,
    char_creation_class_embed, char_creation_confirm_embed, char_creation_race_embed,
    dialogue_embed, dialogue_opening_embed, error_embed, exits_embed,
    guild_contracts_embed, guild_embed, guild_leaderboard_embed, inventory_embed,
    map_embed, market_browse_embed, market_list_item_embed, market_my_listings_embed,
    npc_sell_embed, onboarding_arrival_embed, onboarding_explore_embed,
    onboarding_inventory_embed, onboarding_people_embed, onboarding_rel_answer_embed,
    onboarding_rel_embed, profile_embed, stat_allocation_embed,
    quest_active_embed, quest_complete_embed, quest_detail_embed, quest_log_embed,
    quest_offer_embed, shop_embed, storylet_embed, travel_embed, visit_embed,
    walk_embed, walk_encounter_embed, zone_embed,
    gathering_node_embed,
    gathering_result_embed,
    gathering_skills_embed,
    milestone_scene_embed,
    miniboss_encounter_embed,
    miniboss_defeat_embed,
)


def _not_your_game(interaction: discord.Interaction, user_id: int) -> bool:
    return interaction.user.id != user_id


# =============================================================================
# CHARACTER CREATION
# =============================================================================

class RaceSelectView(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.add_item(RaceSelect(user_id))


class RaceSelect(discord.ui.Select):
    def __init__(self, user_id: int):
        self.user_id = user_id
        options = [
            discord.SelectOption(label=r["name"], value=r["id"], description=r["passive"][:80], emoji=r["emoji"])
            for r in RACES.values()
        ]
        super().__init__(placeholder="Choose your race...", options=options)

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your character!", ephemeral=True)
        race_id = self.values[0]
        await set_char_creation(self.user_id, {"race_id": race_id})
        embed = char_creation_class_embed(race_id)
        view  = ClassSelectView(self.user_id, race_id)
        await interaction.response.edit_message(embed=embed, view=view)


class ClassSelectView(discord.ui.View):
    def __init__(self, user_id: int, race_id: str):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.add_item(ClassSelect(user_id, race_id))


class ClassSelect(discord.ui.Select):
    def __init__(self, user_id: int, race_id: str):
        self.user_id = user_id
        self.race_id = race_id
        options = [
            discord.SelectOption(label=c["name"], value=c["id"], description=c["archetype"][:80], emoji=c["emoji"])
            for c in CLASSES.values()
        ]
        super().__init__(placeholder="Choose your class...", options=options)

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your character!", ephemeral=True)
        class_id = self.values[0]
        creation = await get_char_creation(self.user_id) or {}
        creation["class_id"] = class_id
        await set_char_creation(self.user_id, creation)
        await interaction.response.send_modal(NameModal(self.user_id, self.race_id, class_id))


class NameModal(discord.ui.Modal, title="Name Your Character"):
    name_input = discord.ui.TextInput(label="Character Name", placeholder="2-20 characters", min_length=2, max_length=20)

    def __init__(self, user_id: int, race_id: str, class_id: str):
        super().__init__()
        self.user_id  = user_id
        self.race_id  = race_id
        self.class_id = class_id

    async def on_submit(self, interaction: discord.Interaction):
        from game.world import create_player
        try:
            await interaction.response.defer()
        except discord.errors.NotFound:
            return
        char_name = self.name_input.value.strip()
        async with get_session() as session:
            await create_player(
                user_id=self.user_id, discord_name=str(interaction.user),
                character_name=char_name, race_id=self.race_id,
                class_id=self.class_id, session=session,
            )
        await clear_char_creation(self.user_id)
        embed = char_creation_confirm_embed(self.race_id, self.class_id, char_name)
        view  = EnterWorldView(self.user_id, char_name)
        await interaction.edit_original_response(embed=embed, view=view)


class EnterWorldView(discord.ui.View):
    def __init__(self, user_id: int, char_name: str = ""):
        super().__init__(timeout=300)
        self.user_id   = user_id
        self.char_name = char_name

    @discord.ui.button(label="Enter Ironhaven", style=discord.ButtonStyle.success, emoji="⚓")
    async def enter(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        embed = onboarding_arrival_embed(self.char_name)
        view  = OnboardingView(self.user_id, screen=1)
        await interaction.response.edit_message(embed=embed, view=view)


# =============================================================================
# ONBOARDING
# =============================================================================

class OnboardingView(discord.ui.View):
    def __init__(self, user_id: int, screen: int):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.screen  = screen
        self.add_item(OnboardingNextButton(user_id, screen))


class OnboardingRelConvoView(discord.ui.View):
    def __init__(self, user_id: int, asked: set = None):
        super().__init__(timeout=600)
        self.user_id = user_id
        self.asked   = asked or set()
        questions = [
            ("ironhaven", "What happened to Ironhaven?"),
            ("mercer",    "Tell me about Mercer"),
            ("people",    "Who should I talk to?"),
            ("watchout",  "What should I watch out for?"),
        ]
        row = 0
        col = 0
        for key, label in questions:
            if key not in self.asked:
                self.add_item(RelAskButton(user_id, key, label, self.asked, row=row))
                col += 1
                if col >= 2:
                    col = 0
                    row += 1
        if self.asked:
            self.add_item(RelReadyButton(user_id, row=2))


class OnboardingNextButton(discord.ui.Button):
    def __init__(self, user_id: int, current_screen: int):
        super().__init__(label="Continue →", style=discord.ButtonStyle.primary, emoji="▶️")
        self.user_id        = user_id
        self.current_screen = current_screen

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        next_screen = self.current_screen + 1
        if next_screen == 2:
            embed = onboarding_explore_embed()
            view  = OnboardingView(self.user_id, screen=next_screen)
        elif next_screen == 3:
            embed = onboarding_people_embed()
            view  = OnboardingView(self.user_id, screen=next_screen)
        elif next_screen == 4:
            embed = onboarding_inventory_embed()
            view  = OnboardingView(self.user_id, screen=next_screen)
        elif next_screen == 5:
            embed = onboarding_rel_embed()
            view  = OnboardingRelConvoView(self.user_id)
        else:
            embed = onboarding_arrival_embed("")
            view  = OnboardingView(self.user_id, screen=next_screen)
        await interaction.response.edit_message(embed=embed, view=view)


class OnboardingStartButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Start Playing", style=discord.ButtonStyle.success, emoji="⚔️")
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            await set_flag(self.user_id, "onboarding_complete", "true", session)
            await add_zet(self.user_id, 50, session)
            player = await get_full_player(self.user_id, session)
        zone  = get_zone("town_square")
        embed = zone_embed(player, zone)
        embed.add_field(name="💡 Getting started", value="Head to the **Training Grounds** and talk to **Captain Rel**.", inline=False)
        view = MainZoneView(self.user_id, player, zone)
        await interaction.response.edit_message(embed=embed, view=view)


class OnboardingQuestOfferView(discord.ui.View):
    def __init__(self, user_id: int, npc_id: str, quest: dict):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.npc_id  = npc_id
        self.quest   = quest

    @discord.ui.button(label="Accept quest", emoji="✅", style=discord.ButtonStyle.success, row=0)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        from game.quests import offer_quest, accept_quest
        async with get_session() as session:
            await offer_quest(self.user_id, self.quest, session)
            await session.flush()
            await accept_quest(self.user_id, self.quest["id"], session)
            player = await get_full_player(self.user_id, session)
        progress = {}
        for zone_id in self.quest.get("zone_targets", []):
            progress[f"zone:{zone_id}"] = False
        for npc_target in self.quest.get("npc_targets", []):
            progress[f"npc:{npc_target}"] = False
        npc   = get_npc(self.npc_id)
        embed = quest_active_embed(npc, self.quest, progress)
        embed.set_footer(text="Head to the Residential Ward to complete your first quest.")
        view  = FirstQuestAcceptedView(self.user_id)
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Explore first", emoji="🚶", style=discord.ButtonStyle.secondary, row=0)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        zone  = get_zone("town_square")
        embed = zone_embed(player, zone)
        embed.add_field(name="💡 Tip", value="Talk to **Captain Rel** when you're ready for your first quest.", inline=False)
        view  = MainZoneView(self.user_id, player, zone)
        await interaction.response.edit_message(embed=embed, view=view)


class FirstQuestAcceptedView(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=300)
        self.user_id = user_id

    @discord.ui.button(label="Start exploring", emoji="🚶", style=discord.ButtonStyle.success)
    async def go(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        zone  = get_zone("town_square")
        embed = zone_embed(player, zone)
        view  = MainZoneView(self.user_id, player, zone)
        await interaction.response.edit_message(embed=embed, view=view)


class RelAskButton(discord.ui.Button):
    def __init__(self, user_id: int, question_key: str, label: str, asked: set, row: int = 0):
        super().__init__(label=label, style=discord.ButtonStyle.secondary, row=row)
        self.user_id      = user_id
        self.question_key = question_key
        self.asked        = asked

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        new_asked = self.asked | {self.question_key}
        embed = onboarding_rel_answer_embed(self.question_key)
        view  = OnboardingRelConvoView(self.user_id, asked=new_asked)
        await interaction.response.edit_message(embed=embed, view=view)


class RelReadyButton(discord.ui.Button):
    def __init__(self, user_id: int, row: int = 2):
        super().__init__(label="I'm ready to help", emoji="⚔️", style=discord.ButtonStyle.success, row=row)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            await set_flag(self.user_id, "onboarding_complete", "true", session)
            await add_zet(self.user_id, 50, session)
            player = await get_full_player(self.user_id, session)
        from game.quest_chains import QUEST_CHAINS
        rel_chain   = QUEST_CHAINS.get("captain_rel", [])
        first_quest = rel_chain[0] if rel_chain else None
        if first_quest:
            npc   = get_npc("captain_rel")
            embed = quest_offer_embed(npc, first_quest)
            embed.add_field(
                name="How quests work",
                value="Complete the objective, then return and talk to Rel. Every NPC offers quests as you build trust.",
                inline=False,
            )
            view = OnboardingQuestOfferView(self.user_id, "captain_rel", first_quest)
        else:
            zone  = get_zone("town_square")
            embed = zone_embed(player, zone)
            view  = MainZoneView(self.user_id, player, zone)
        await interaction.response.edit_message(embed=embed, view=view)


def _drop_into_zone(user_id: int, player) -> "MainZoneView":
    zone = get_zone("town_square")
    return MainZoneView(user_id, player, zone)


# =============================================================================
# MAIN ZONE VIEW
# =============================================================================

class MainZoneView(discord.ui.View):
    def __init__(self, user_id: int, player=None, zone_data: dict = None):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.add_item(WalkButton(user_id))
        self.add_item(VisitButton(user_id))
        self.add_item(TravelButton(user_id))
        self.add_item(BagButton(user_id))
        self.add_item(ProfileButton(user_id))
        self.add_item(MapButton(user_id))
        self.add_item(QuestLogButton(user_id))


# =============================================================================
# WALK
# =============================================================================

class WalkButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Walk", emoji="🚶", style=discord.ButtonStyle.success, row=0)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        try:
            await interaction.response.defer()
        except discord.errors.NotFound:
            return

        async with get_session() as session:
            player = await get_full_player(self.user_id, session)

        zone_id     = player.progression.current_zone_id
        zone_data   = get_zone(zone_id)
        daily_steps = await get_step_count(self.user_id, zone_id)
        total_steps = await get_total_steps(self.user_id, zone_id)

        # Phase 3: check zone cleared before rolling encounters
        from game.respawn import (
            check_encounter_allowed, should_encounter_miniboss,
            get_miniboss_for_zone, get_zone_status,
        )
        from core.cache import is_zone_cleared, get_zone_respawn_seconds
        zone_cleared_flag = await is_zone_cleared(self.user_id, zone_id)

        walk_result = await process_walk_step(
            user_id=self.user_id, zone_id=zone_id,
            daily_steps=daily_steps, total_steps=total_steps,
            zone_cleared=zone_cleared_flag,
        )

        await increment_step(self.user_id, zone_id)
        await increment_total_steps(self.user_id, zone_id)

        async with get_session() as session:
            await add_xp(self.user_id, walk_result["xp_gained"], session)
            if walk_result.get("zet_dropped", 0) > 0:
                await add_zet(self.user_id, walk_result["zet_dropped"], session)
            from game.quests import record_zone_visit, has_ready_to_complete
            await record_zone_visit(self.user_id, zone_id, session)
            from game.quest_chains import QUEST_CHAINS
            quest_ready_message = None
            for npc_id_check, chain in QUEST_CHAINS.items():
                ready = await has_ready_to_complete(self.user_id, npc_id_check, session)
                if ready:
                    npc_data_check = get_npc(npc_id_check)
                    if npc_data_check:
                        quest_ready_message = (
                            f"📋 **Quest ready!** Return to **{npc_data_check['name']}** to complete *{ready['title']}*."
                        )
                    break
            walk_result["quest_ready_message"] = quest_ready_message
            if walk_result["event_type"] == "npc_moment" and walk_result.get("npc_moment"):
                npc_id = walk_result["npc_moment"].get("npc")
                if npc_id:
                    rel = await get_or_create_relationship(self.user_id, npc_id, session)
                    rel.relationship_score = min(100, (rel.relationship_score or 0) + 1)
                    npc_data = get_npc(npc_id)
                    if npc_data:
                        walk_result["relationship_npc_name"] = npc_data["name"]
            player = await get_full_player(self.user_id, session)

        # Phase 3: mini-boss encounter (rolls before regular encounter)
        if not zone_cleared_flag and walk_result["event_type"] != "gathering_node":
            if await should_encounter_miniboss(zone_id):
                mb_enemy = await get_miniboss_for_zone(zone_id)
                if mb_enemy:
                    embed = miniboss_encounter_embed(player, zone_data, mb_enemy)
                    view  = MiniBossEncounterView(self.user_id, mb_enemy["id"], zone_id)
                    return await interaction.edit_original_response(embed=embed, view=view)

        if walk_result["event_type"] == "encounter" and walk_result.get("enemy_id"):
            enemy = ENEMIES.get(walk_result["enemy_id"])
            if enemy:
                embed = walk_encounter_embed(player, zone_data, enemy, walk_result["daily_steps"])
                view  = WalkEncounterView(self.user_id, walk_result["enemy_id"], zone_id)
                return await interaction.edit_original_response(embed=embed, view=view)

        if walk_result["event_type"] == "discovery":
            disc = walk_result.get("discovery") or {}
            if disc.get("item"):
                async with get_session() as session:
                    from game.world import safe_add_item
                    success, item_msg = await safe_add_item(self.user_id, disc["item"], 1, session)
                    player = await get_full_player(self.user_id, session)

        if walk_result["event_type"] == "item_find":
            find = walk_result.get("item_find") or {}
            if find.get("item_id"):
                async with get_session() as session:
                    from game.world import safe_add_item
                    success, item_msg = await safe_add_item(self.user_id, find["item_id"], 1, session)
                    if not success:
                        walk_result["item_find_failed"] = item_msg
                    player = await get_full_player(self.user_id, session)

        if walk_result["event_type"] == "gathering_node" and walk_result.get("gathering_node"):
            node  = walk_result["gathering_node"]
            embed = gathering_node_embed(player, zone_data, node)
            view  = GatheringNodeView(self.user_id, node["id"], zone_id)
            return await interaction.edit_original_response(embed=embed, view=view)

        # Check if a walk-triggered storylet should fire
        async with get_session() as session:
            from game.storylets import check_storylet_trigger
            from game.world_state import get_zone_state_description_async
            active_storylet = await check_storylet_trigger(
                user_id=self.user_id, zone_id=zone_id, npc_id=None, session=session,
            )
            world_override = await get_zone_state_description_async(zone_id, self.user_id, session)

        if active_storylet:
            embed = storylet_embed(active_storylet)
            view  = StoryletView(self.user_id, active_storylet)
            return await interaction.edit_original_response(embed=embed, view=view)

        # Phase 3: get zone status for embed display (respawn countdowns)
        zone_status = await get_zone_status(self.user_id, zone_id)
        walk_result["zone_cleared"]          = zone_cleared_flag
        walk_result["zone_cleared_respawn"]  = zone_status.get("enemy_respawn_secs", 1800)

        embed = walk_embed(player, zone_data, walk_result)
        view  = WalkingView(self.user_id)
        await interaction.edit_original_response(embed=embed, view=view)


class WalkingView(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.add_item(WalkButton(user_id))
        self.add_item(VisitButton(user_id))
        self.add_item(TravelButton(user_id))
        self.add_item(BagButton(user_id))
        self.add_item(ProfileButton(user_id))
        self.add_item(MapButton(user_id))
        self.add_item(QuestLogButton(user_id))


class WalkEncounterView(discord.ui.View):
    def __init__(self, user_id: int, enemy_id: str, zone_id: str):
        super().__init__(timeout=300)
        self.user_id  = user_id
        self.enemy_id = enemy_id
        self.zone_id  = zone_id

    @discord.ui.button(label="Fight", emoji="⚔️", style=discord.ButtonStyle.danger, row=0)
    async def fight(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        await interaction.response.defer()
        await _start_battle(interaction, self.user_id, self.enemy_id)

    @discord.ui.button(label="Flee", emoji="🏃", style=discord.ButtonStyle.secondary, row=0)
    async def flee(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        try:
            await interaction.response.defer()
        except discord.errors.NotFound:
            return
        import random
        async with get_session() as session:
            await deduct_zet(self.user_id, 5, session)
            player = await get_full_player(self.user_id, session)
        zone_data   = get_zone(self.zone_id)
        daily_steps = await get_step_count(self.user_id, self.zone_id)
        total_steps = await get_total_steps(self.user_id, self.zone_id)
        from game.walk_data import get_walk_data
        walk_data   = get_walk_data(self.zone_id)
        atmosphere  = random.choice(walk_data.get("atmosphere", ["You slip away."]))
        fake_result = {
            "event_type": "quiet", "atmosphere": f"You slip away. -5 Ƶ.\n\n*{atmosphere}*",
            "xp_gained": 0, "daily_steps": daily_steps, "total_steps": total_steps,
            "quote": None, "npc_moment": None, "discovery": None,
            "enemy_id": None, "mastery_milestone": None, "xp_cap_warning": False,
        }
        embed = walk_embed(player, zone_data, fake_result)
        view  = WalkingView(self.user_id)
        await interaction.edit_original_response(embed=embed, view=view)

    @discord.ui.button(label="Bluff", emoji="🎲", style=discord.ButtonStyle.primary, row=0)
    async def bluff(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        try:
            await interaction.response.defer()
        except discord.errors.NotFound:
            return
        import random
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        agi         = player.stats.agility
        success     = random.random() < min(0.8, 0.3 + agi * 0.03)
        zone_data   = get_zone(self.zone_id)
        daily_steps = await get_step_count(self.user_id, self.zone_id)
        total_steps = await get_total_steps(self.user_id, self.zone_id)
        if not success:
            await _start_battle(interaction, self.user_id, self.enemy_id)
            return
        async with get_session() as session:
            await add_xp(self.user_id, 5, session)
            player = await get_full_player(self.user_id, session)
        fake_result = {
            "event_type": "quiet", "atmosphere": "Your bluff works. They back off, uncertain. You walk away.",
            "xp_gained": 5, "daily_steps": daily_steps, "total_steps": total_steps,
            "quote": None, "npc_moment": None, "discovery": None,
            "enemy_id": None, "mastery_milestone": None, "xp_cap_warning": False,
        }
        embed = walk_embed(player, zone_data, fake_result)
        view  = WalkingView(self.user_id)
        await interaction.edit_original_response(embed=embed, view=view)


# =============================================================================
# VISIT
# =============================================================================

class VisitButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Visit", emoji="🏪", style=discord.ButtonStyle.secondary, row=0)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        zone_id   = player.progression.current_zone_id
        zone_data = get_zone(zone_id)
        buildings = get_buildings_in_zone(zone_id)
        npcs      = get_npcs_in_zone(zone_id)
        if not buildings and not npcs:
            return await interaction.response.send_message("Nothing to visit here.", ephemeral=True)
        embed = visit_embed(zone_data)
        view  = VisitView(self.user_id, zone_data, buildings, npcs)
        await interaction.response.edit_message(embed=embed, view=view)


class VisitView(discord.ui.View):
    def __init__(self, user_id: int, zone_data: dict, buildings: list, npcs: list):
        super().__init__(timeout=180)
        self.user_id = user_id
        for i, bldg in enumerate(buildings[:6]):
            self.add_item(BuildingButton(user_id, bldg, row=i // 3))
        for npc in npcs[:2]:
            npc_building = npc.get("building_id")
            building_ids = [b["id"] for b in buildings]
            if not npc_building or npc_building not in building_ids:
                self.add_item(NPCButton(user_id, npc, row=2))
        self.add_item(BackToWalkButton(user_id, row=3))


class BuildingButton(discord.ui.Button):
    def __init__(self, user_id: int, building: dict, row: int = 0):
        super().__init__(label=building["name"][:20], emoji=building.get("emoji", "🏛️"),
                         style=discord.ButtonStyle.secondary, row=row)
        self.user_id  = user_id
        self.building = building

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        embed = building_embed(self.building)
        view  = BuildingView(self.user_id, self.building)
        await interaction.response.edit_message(embed=embed, view=view)


class BuildingView(discord.ui.View):
    def __init__(self, user_id: int, building: dict):
        super().__init__(timeout=180)
        self.user_id  = user_id
        self.building = building
        if building.get("npc"):
            npc = get_npc(building["npc"])
            if npc:
                self.add_item(TalkToNPCButton(user_id, building["npc"]))
        shop = get_shop_for_building(building["id"])
        if shop:
            self.add_item(OpenShopButton(user_id, shop["id"]))
        btype = building.get("type")
        if btype == "heal":
            self.add_item(HealButton(user_id))
        elif btype == "rest":
            self.add_item(RestButton(user_id))
        elif btype == "training":
            self.add_item(TrainButton(user_id))
        elif btype == "quest":
            self.add_item(OpenGuildButton(user_id))
        elif btype == "market":
            self.add_item(OpenAuctionButton(user_id))
        if building.get("npc") and get_shop_for_building(building["id"]):
            self.add_item(OpenSellButton(user_id, building["npc"]))
        self.add_item(ExitBuildingButton(user_id))


class TalkToNPCButton(discord.ui.Button):
    def __init__(self, user_id: int, npc_id: str):
        npc   = get_npc(npc_id)
        label = f"Talk to {npc['name']}" if npc else "Talk"
        super().__init__(label=label, emoji="💬", style=discord.ButtonStyle.primary)
        self.user_id = user_id
        self.npc_id  = npc_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        npc = get_npc(self.npc_id)
        if not npc:
            return await interaction.response.send_message("NPC not found.", ephemeral=True)
        async with get_session() as session:
            await get_or_create_relationship(self.user_id, self.npc_id, session)
        embed = dialogue_opening_embed(npc)
        view  = DialogueView(self.user_id, self.npc_id, _default_suggestions(self.npc_id))
        await interaction.response.edit_message(embed=embed, view=view)


class OpenShopButton(discord.ui.Button):
    def __init__(self, user_id: int, shop_id: str):
        super().__init__(label="Browse Shop", emoji="🛒", style=discord.ButtonStyle.success)
        self.user_id = user_id
        self.shop_id = shop_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        shop = SHOPS.get(self.shop_id)
        if not shop:
            return await interaction.response.send_message("No stock.", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        embed = shop_embed(shop, player.progression.zet_wallet)
        view  = ShopView(self.user_id, shop, player.progression.zet_wallet)
        await interaction.response.edit_message(embed=embed, view=view)


class HealButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Get Treatment (50Ƶ)", emoji="⚕️", style=discord.ButtonStyle.success)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            if not await deduct_zet(self.user_id, 50, session):
                return await interaction.response.send_message("Not enough Ƶ.", ephemeral=True)
            await full_heal_player(self.user_id, session)
            player = await get_full_player(self.user_id, session)
        await interaction.response.send_message(
            f"✅ Treated. HP restored ({player.stats.vit*5}/{player.stats.vit*5}). -50 Ƶ.", ephemeral=True)


class RestButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Rest (20Ƶ)", emoji="🛏️", style=discord.ButtonStyle.success)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            if not await deduct_zet(self.user_id, 20, session):
                return await interaction.response.send_message("Not enough Ƶ.", ephemeral=True)
            await full_heal_player(self.user_id, session)
            player = await get_full_player(self.user_id, session)
        await interaction.response.send_message(
            f"🛏️ Rested. HP restored ({player.stats.vit*5}/{player.stats.vit*5}). -20 Ƶ.", ephemeral=True)


class TrainButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Train (30Ƶ, +50 XP)", emoji="🥋", style=discord.ButtonStyle.primary)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            if not await deduct_zet(self.user_id, 30, session):
                return await interaction.response.send_message("Not enough Ƶ.", ephemeral=True)
            result = await add_xp(self.user_id, 50, session)
        msg = "🥋 Training complete. +50 XP."
        if result.get("leveled_up"):
            msg += f" **Level up! You're now level {result['new_level']}.**"
        await interaction.response.send_message(msg, ephemeral=True)


class OpenGuildButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="View Contracts", emoji="📋", style=discord.ButtonStyle.primary)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        embed = guild_embed()
        view  = GuildBuildingView(self.user_id)
        await interaction.response.edit_message(embed=embed, view=view)


class OpenAuctionButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Open Market", emoji="🏷️", style=discord.ButtonStyle.primary)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        embed = market_browse_embed([], {}, "all", "recent", 0, 0, self.user_id)
        view  = AuctionHouseView(self.user_id)
        await interaction.response.edit_message(embed=embed, view=view)


class OpenSellButton(discord.ui.Button):
    def __init__(self, user_id: int, npc_id: str):
        super().__init__(label="Sell Items", emoji="💰", style=discord.ButtonStyle.success)
        self.user_id = user_id
        self.npc_id  = npc_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            from game.market import get_sellable_inventory
            sellable = await get_sellable_inventory(self.user_id, self.npc_id, session)
            player   = await get_full_player(self.user_id, session)
        npc   = get_npc(self.npc_id)
        embed = npc_sell_embed(sellable, npc, player.progression.zet_wallet)
        view  = NPCSellView(self.user_id, self.npc_id, sellable, player.progression.zet_wallet)
        await interaction.response.edit_message(embed=embed, view=view)


class ExitBuildingButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Exit", emoji="🚪", style=discord.ButtonStyle.secondary)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        zone_id   = player.progression.current_zone_id
        zone_data = get_zone(zone_id)
        embed     = visit_embed(zone_data)
        view      = VisitView(self.user_id, zone_data, get_buildings_in_zone(zone_id), get_npcs_in_zone(zone_id))
        await interaction.response.edit_message(embed=embed, view=view)


# =============================================================================
# TRAVEL
# =============================================================================

class TravelButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Travel", emoji="🗺️", style=discord.ButtonStyle.secondary, row=0)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        zone_id   = player.progression.current_zone_id
        zone_data = get_zone(zone_id)
        connected = zone_data.get("connected_to", [])
        if not connected:
            return await interaction.response.send_message("No exits here.", ephemeral=True)
        embed = exits_embed(zone_data)
        view  = TravelView(self.user_id, zone_data, connected)
        await interaction.response.edit_message(embed=embed, view=view)


class TravelView(discord.ui.View):
    def __init__(self, user_id: int, current_zone: dict, connected_ids: list):
        super().__init__(timeout=120)
        self.user_id = user_id
        for i, zone_id in enumerate(connected_ids[:4]):
            z = ZONES.get(zone_id)
            if z:
                self.add_item(ZoneTravelButton(user_id, current_zone, z, row=0 if i < 3 else 1))
        self.add_item(BackToWalkButton(user_id))


class ZoneTravelButton(discord.ui.Button):
    def __init__(self, user_id: int, from_zone: dict, to_zone: dict, row: int = 0):
        super().__init__(label=to_zone["name"], emoji=to_zone.get("emoji","🗺️"),
                         style=discord.ButtonStyle.secondary, row=row)
        self.user_id   = user_id
        self.from_zone = from_zone
        self.to_zone   = to_zone

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        min_level = self.to_zone.get("level_requirement", 1)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
            if player.progression.level < min_level:
                return await interaction.response.send_message(
                    f"You need to be level {min_level} to enter {self.to_zone['name']}.", ephemeral=True)
            await update_player_zone(self.user_id, self.to_zone["id"], session)
            from game.quests import record_zone_visit
            await record_zone_visit(self.user_id, self.to_zone["id"], session)
            player = await get_full_player(self.user_id, session)
        travel_line = get_travel_line(self.from_zone["id"], self.to_zone["id"])
        embed = travel_embed(player, self.from_zone, self.to_zone, travel_line)
        view  = ArrivalView(self.user_id, player, self.to_zone)
        await interaction.response.edit_message(embed=embed, view=view)


class ArrivalView(discord.ui.View):
    def __init__(self, user_id: int, player, zone_data: dict):
        super().__init__(timeout=300)
        self.user_id   = user_id
        self.player    = player
        self.zone_data = zone_data

    @discord.ui.button(label="Start Exploring", emoji="🚶", style=discord.ButtonStyle.success)
    async def explore(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        embed = zone_embed(player, self.zone_data)
        view  = MainZoneView(self.user_id, player, self.zone_data)
        await interaction.response.edit_message(embed=embed, view=view)


# =============================================================================
# DIALOGUE
# =============================================================================

class NPCButton(discord.ui.Button):
    def __init__(self, user_id: int, npc: dict, row: int = 0):
        super().__init__(label=npc["name"], emoji=npc["emoji"], style=discord.ButtonStyle.primary, row=row)
        self.user_id = user_id
        self.npc_id  = npc["id"]
        self.npc     = npc

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            await get_or_create_relationship(self.user_id, self.npc_id, session)
        embed = dialogue_opening_embed(self.npc)
        view  = DialogueView(self.user_id, self.npc_id, _default_suggestions(self.npc_id))
        await interaction.response.edit_message(embed=embed, view=view)


_DEFAULT_SUGGESTIONS_FALLBACK = [
    "How are things in Ironhaven?",
    "What do you know about Mercer?",
    "Anything I should know about this city?",
]

_NPC_SUGGESTIONS: dict[str, list[str]] = {
    "old_tomas":    ["How's business lately?", "Tell me about your son.", "What was Ironhaven like before Mercer?"],
    "maren":        ["What moves through this port?", "Tell me about the night shipments.", "How long have you worked the docks?"],
    "nurse_hana":   ["What injuries are you seeing lately?", "Have you treated workers from the forest?", "What do you know about the black ore?"],
    "captain_rel":  ["What's happening in this city?", "Tell me about your past.", "What should I watch out for?"],
    "vex":          ["What cards do you have?", "How did you end up in Ironhaven?", "What do you know about the ruins symbol?"],
    "bora":         ["What do people talk about in here?", "What have the soldiers been saying?", "Tell me about Ironhaven."],
    "shade":        ["Who are you?", "What are you doing in the ruins?", "What do you know about Mercer?"],
    "old_grull":    ["How's the fishing?", "What's changed near the caves?", "Tell me about the cove."],
}


def _default_suggestions(npc_id: str) -> list[str]:
    return _NPC_SUGGESTIONS.get(npc_id, _DEFAULT_SUGGESTIONS_FALLBACK)


class DialogueView(discord.ui.View):
    def __init__(self, user_id: int, npc_id: str, suggestions: list[str]):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.npc_id  = npc_id
        for suggestion in suggestions[:3]:
            self.add_item(SuggestionButton(user_id, npc_id, suggestion, row=0))
        self.add_item(TypeFreelyButton(user_id, npc_id))
        self.add_item(LeaveDialogueButton(user_id))


class SuggestionButton(discord.ui.Button):
    def __init__(self, user_id: int, npc_id: str, suggestion: str, row: int = 0):
        super().__init__(label=suggestion[:80], style=discord.ButtonStyle.secondary, row=row)
        self.user_id    = user_id
        self.npc_id     = npc_id
        self.suggestion = suggestion

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        await interaction.response.defer()
        await _send_dialogue_message(interaction, self.user_id, self.npc_id, self.suggestion)


class TypeFreelyButton(discord.ui.Button):
    def __init__(self, user_id: int, npc_id: str):
        super().__init__(label="Type freely...", emoji="✏️", style=discord.ButtonStyle.primary, row=1)
        self.user_id = user_id
        self.npc_id  = npc_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        await interaction.response.send_modal(DialogueReplyModal(self.user_id, self.npc_id))


class LeaveDialogueButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Leave", emoji="🚪", style=discord.ButtonStyle.danger, row=1)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        zone  = get_zone(player.progression.current_zone_id)
        embed = zone_embed(player, zone)
        view  = MainZoneView(self.user_id, player, zone)
        await interaction.response.edit_message(embed=embed, view=view)


class DialogueReplyModal(discord.ui.Modal, title="Speak"):
    message_input = discord.ui.TextInput(
        label="Your message", placeholder="What do you say?",
        style=discord.TextStyle.paragraph, max_length=200,
    )

    def __init__(self, user_id: int, npc_id: str):
        super().__init__()
        self.user_id = user_id
        self.npc_id  = npc_id

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
        except discord.errors.NotFound:
            return
        await _send_dialogue_message(interaction, self.user_id, self.npc_id, self.message_input.value.strip())


async def _send_dialogue_message(interaction, user_id, npc_id, player_message):
    from ai.npc import get_dialogue_suggestions, get_npc_reply
    from game.quests import (
        apply_quest_relationship_gain, complete_quest,
        get_available_quest, has_ready_to_complete, record_npc_interaction,
    )
    npc = get_npc(npc_id)
    if not npc:
        return
    try:
        async with get_session() as session:
            player = await get_full_player(user_id, session)
            rel    = await get_or_create_relationship(user_id, npc_id, session)
            ready_quest = await has_ready_to_complete(user_id, npc_id, session)

            # Check milestone scenes before quest/AI
            from game.npc_scenes import get_milestone_scene
            milestone = await get_milestone_scene(user_id, npc_id, rel.relationship_score, session)
            if milestone:
                embed = milestone_scene_embed(npc, milestone)
                view  = DialogueView(user_id, npc_id, _default_suggestions(npc_id))
                return await interaction.edit_original_response(embed=embed, view=view)

            if ready_quest:
                result = await complete_quest(user_id, ready_quest["id"], session)
                await apply_quest_relationship_gain(user_id, npc_id, ready_quest.get("relationship_gain", 0), session)
                embed = quest_complete_embed(npc, ready_quest, result)
                view  = QuestCompleteView(user_id, npc_id)
                return await interaction.edit_original_response(embed=embed, view=view)
            await record_npc_interaction(user_id, npc_id, session)
            from core.models import PlayerQuest as _PQ
            from sqlalchemy import select as _sel
            _any_inprogress = await session.execute(
                _sel(_PQ).where(_PQ.user_id == user_id, _PQ.npc_id == npc_id, _PQ.status.in_(["offered", "active"]))
            )
            has_inprogress = _any_inprogress.scalar_one_or_none() is not None
            if not has_inprogress:
                available = await get_available_quest(user_id, npc_id, rel.relationship_score, session)
                if available:
                    embed = quest_offer_embed(npc, available)
                    view  = QuestOfferView(user_id, npc_id, available)
                    return await interaction.edit_original_response(embed=embed, view=view)
            reply = await get_npc_reply(
                npc_id=npc_id, user_id=user_id,
                player_message=player_message, player_name=player.character_name, session=session,
            )
        suggestions = await get_dialogue_suggestions(
            npc_id=npc_id, last_reply=reply, player_name=player.character_name, relationship=rel,
        )
        embed = dialogue_embed(npc, rel, reply, player.character_name, player_message)
        view  = DialogueView(user_id, npc_id, suggestions)
        await interaction.edit_original_response(embed=embed, view=view)
    except Exception as e:
        import traceback
        print(f"[Dialogue Error] {e}")
        traceback.print_exc()
        try:
            await interaction.edit_original_response(
                embed=error_embed("Something went wrong. Try again."),
                view=DialogueView(user_id, npc_id, _default_suggestions(npc_id)),
            )
        except Exception:
            pass


# =============================================================================
# QUEST VIEWS
# =============================================================================

class QuestOfferView(discord.ui.View):
    def __init__(self, user_id: int, npc_id: str, quest: dict):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.npc_id  = npc_id
        self.quest   = quest

    @discord.ui.button(label="Accept", emoji="✅", style=discord.ButtonStyle.success, row=0)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        from game.quests import offer_quest, accept_quest
        async with get_session() as session:
            await offer_quest(self.user_id, self.quest, session)
            await session.flush()
            await accept_quest(self.user_id, self.quest["id"], session)
        npc      = get_npc(self.npc_id)
        progress = {}
        for zone_id in self.quest.get("zone_targets", []):
            progress[f"zone:{zone_id}"] = False
        for npc_target in self.quest.get("npc_targets", []):
            progress[f"npc:{npc_target}"] = False
        embed = quest_active_embed(npc, self.quest, progress)
        view  = QuestActiveView(self.user_id, self.npc_id, self.quest)
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Not now", emoji="⏸️", style=discord.ButtonStyle.secondary, row=0)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        npc   = get_npc(self.npc_id)
        embed = dialogue_opening_embed(npc)
        view  = DialogueView(self.user_id, self.npc_id, _default_suggestions(self.npc_id))
        await interaction.response.edit_message(embed=embed, view=view)


class QuestActiveView(discord.ui.View):
    def __init__(self, user_id: int, npc_id: str, quest: dict):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.npc_id  = npc_id
        self.quest   = quest

    @discord.ui.button(label="Back to talking", emoji="💬", style=discord.ButtonStyle.secondary, row=0)
    async def back_to_dialogue(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        npc   = get_npc(self.npc_id)
        embed = dialogue_opening_embed(npc)
        view  = DialogueView(self.user_id, self.npc_id, _default_suggestions(self.npc_id))
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Leave", emoji="🚪", style=discord.ButtonStyle.danger, row=0)
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        zone  = get_zone(player.progression.current_zone_id)
        embed = zone_embed(player, zone)
        view  = MainZoneView(self.user_id, player, zone)
        await interaction.response.edit_message(embed=embed, view=view)


class QuestCompleteView(discord.ui.View):
    def __init__(self, user_id: int, npc_id: str):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.npc_id  = npc_id
        self.add_item(BackButton(user_id))


class QuestLogButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Quests", emoji="📋", style=discord.ButtonStyle.secondary, row=2)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            from game.quests import get_quest_log
            quest_log = await get_quest_log(self.user_id, session)
            player    = await get_full_player(self.user_id, session)
        embed = quest_log_embed(quest_log, player)
        view  = QuestLogView(self.user_id, quest_log["active"])
        await interaction.response.edit_message(embed=embed, view=view)


class QuestLogView(discord.ui.View):
    def __init__(self, user_id: int, active_quests: list = None):
        super().__init__(timeout=180)
        self.user_id = user_id
        for quest_data, quest_row in (active_quests or [])[:4]:
            npc = NPCS.get(quest_data.get("giver_npc", ""), {})
            self.add_item(QuestDetailButton(user_id, quest_data, quest_row, npc))
        self.add_item(BackButton(user_id))


class QuestDetailButton(discord.ui.Button):
    def __init__(self, user_id: int, quest_data: dict, quest_row, npc: dict):
        super().__init__(label=quest_data["title"][:80], emoji=npc.get("emoji", "📋"), style=discord.ButtonStyle.secondary)
        self.user_id    = user_id
        self.quest_data = quest_data
        self.quest_row  = quest_row
        self.npc        = npc

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        embed = quest_detail_embed(self.npc, self.quest_data, self.quest_row.progress)
        view  = QuestDetailView(self.user_id, self.quest_data, self.quest_row, self.npc)
        await interaction.response.edit_message(embed=embed, view=view)


class QuestDetailView(discord.ui.View):
    def __init__(self, user_id: int, quest_data: dict, quest_row, npc: dict):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.add_item(BackToQuestLogButton(user_id))


class BackToQuestLogButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Back to Quest Log", emoji="◀️", style=discord.ButtonStyle.secondary)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            from game.quests import get_quest_log
            quest_log = await get_quest_log(self.user_id, session)
            player    = await get_full_player(self.user_id, session)
        embed = quest_log_embed(quest_log, player)
        view  = QuestLogView(self.user_id, quest_log["active"])
        await interaction.response.edit_message(embed=embed, view=view)


# =============================================================================
# BATTLE
# =============================================================================

async def _start_battle(interaction: discord.Interaction, user_id: int, enemy_id: str):
    async with get_session() as session:
        player      = await get_full_player(user_id, session)
        deck        = await get_deck_list(user_id, session)
        card_levels = await get_card_collection_levels(user_id, session)
    if not deck:
        return await interaction.response.send_message("Your deck is empty!", ephemeral=True)
    stats  = player.stats.to_dict()
    max_hp = player.stats.vit * 5
    state  = build_initial_battle_state(
        user_id=user_id, enemy_id=enemy_id,
        player_stats=stats, player_deck=deck,
        player_hp=player.progression.current_hp, player_max_hp=max_hp,
        card_levels=card_levels,
    )
    state["player_name"] = player.character_name
    if player.race_id == "skyborn":
        state["next_card_discount"] = 999
    await set_battle_state(user_id, state)
    try:
        await interaction.edit_original_response(embed=battle_embed(state, []), view=BattleView(user_id, state))
    except Exception:
        await interaction.response.edit_message(embed=battle_embed(state, []), view=BattleView(user_id, state))


class BattleView(discord.ui.View):
    def __init__(self, user_id: int, battle_state: dict):
        super().__init__(timeout=None)
        self.user_id = user_id
        hand   = battle_state.get("hand", [])
        energy = battle_state.get("energy", 0)
        for i, card_id in enumerate(hand[:4]):
            card = get_card(card_id)
            if card:
                self.add_item(CardButton(user_id, i, card, card["cost"] <= energy, row=0))
        self.add_item(PassButton(user_id))
        self.add_item(BattleFleeButton(user_id))


class CardButton(discord.ui.Button):
    def __init__(self, user_id: int, hand_index: int, card: dict, can_afford: bool, row: int = 0):
        super().__init__(
            label=f"{card['name']} {card['cost']}⚡", emoji=card["emoji"],
            style=discord.ButtonStyle.primary if can_afford else discord.ButtonStyle.secondary,
            disabled=not can_afford, row=row,
        )
        self.user_id    = user_id
        self.hand_index = hand_index
        self.card_id    = card["id"]

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your battle!", ephemeral=True)
        state = await get_battle_state(self.user_id)
        if not state:
            return await interaction.response.send_message("No active battle.", ephemeral=True)
        hand = state.get("hand", [])
        if self.hand_index >= len(hand) or hand[self.hand_index] != self.card_id:
            return await interaction.response.send_message("Card no longer in hand.", ephemeral=True)

        state   = resolve_card(self.card_id, state, self.hand_index)
        outcome = check_battle_outcome(state)
        if outcome == "win":
            await _handle_battle_win(interaction, self.user_id, state); return
        if outcome == "lose":
            await _handle_battle_loss(interaction, self.user_id, state); return

        # Enemy does NOT attack after each card — only on Pass Turn
        await set_battle_state(self.user_id, state)
        await interaction.response.edit_message(embed=battle_embed(state, []), view=BattleView(self.user_id, state))


class PassButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Pass Turn", emoji="⏭️", style=discord.ButtonStyle.secondary, row=1)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your battle!", ephemeral=True)
        try:
            await interaction.response.defer()
        except discord.errors.NotFound:
            return
        state = await get_battle_state(self.user_id)
        if not state:
            return await interaction.edit_original_response(embed=error_embed("No active battle found."), view=None)
        state   = resolve_enemy_turn(state)
        outcome = check_battle_outcome(state)
        if outcome == "lose":
            await _handle_battle_loss(interaction, self.user_id, state); return
        state = tick_start_of_player_turn(state)
        await set_battle_state(self.user_id, state)
        await interaction.edit_original_response(embed=battle_embed(state, []), view=BattleView(self.user_id, state))


class BattleFleeButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Flee", emoji="🏃", style=discord.ButtonStyle.danger, row=1)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your battle!", ephemeral=True)
        try:
            await interaction.response.defer()
        except discord.errors.NotFound:
            return
        await clear_battle_state(self.user_id)
        async with get_session() as session:
            await deduct_zet(self.user_id, 10, session)
            player = await get_full_player(self.user_id, session)
        zone  = get_zone(player.progression.current_zone_id)
        embed = zone_embed(player, zone)
        embed.add_field(name="🏃 Fled!", value="Escaped. Lost 10 Ƶ.", inline=False)
        await interaction.edit_original_response(embed=embed, view=MainZoneView(self.user_id, player, zone))


async def _handle_battle_win(interaction, user_id, state):
    enemy_id   = state["enemy_id"]
    enemy_name = state["enemy_name"]
    await clear_battle_state(user_id)
    async with get_session() as session:
        player    = await get_full_player(user_id, session)
        zone_id   = player.progression.current_zone_id
        drops     = generate_drops(enemy_id, player.stats.lck)
        if drops.get("zet"):
            await add_zet(user_id, drops["zet"], session)
        for card_id in drops.get("cards", []):
            await add_card_to_collection(user_id, card_id, session)
            await add_card_to_deck(user_id, card_id, session)
        for item_id in drops.get("items", []):
            await add_item(user_id, item_id, 1, session)
        xp_reward = ENEMIES.get(enemy_id, {}).get("xp_reward", 10)
        xp_result = await add_xp(user_id, xp_reward, session)
        xp_result["xp_gained"] = xp_reward
        await update_player_hp(user_id, max(1, state["player_hp"]), session)

    # Phase 3: handle mini-boss defeat OR record regular kill for respawn timer
    enemy_data = ENEMIES.get(enemy_id, {})
    if enemy_data.get("is_miniboss"):
        from game.respawn import handle_miniboss_defeat
        defeat_data = await handle_miniboss_defeat(zone_id, player.character_name)
        embed = miniboss_defeat_embed(player, enemy_data, drops, xp_result, defeat_data["announce"])
    else:
        from game.respawn import record_enemy_kill
        await record_enemy_kill(user_id, zone_id)
        embed = battle_result_embed(True, drops, xp_result, enemy_name)

    view = BackToZoneView(user_id)
    await interaction.response.edit_message(embed=embed, view=view)


async def _handle_battle_loss(interaction, user_id, state):
    enemy_name = state["enemy_name"]
    await clear_battle_state(user_id)
    async with get_session() as session:
        player = await get_full_player(user_id, session)
        max_hp = player.stats.vit * 5
        await update_player_hp(user_id, max(1, int(max_hp * 0.25)), session)
        await update_player_zone(user_id, "town_square", session)
        await deduct_zet(user_id, 10, session)
    embed = battle_result_embed(False, {}, {}, enemy_name)
    view  = BackToZoneView(user_id)
    # Fixed: use edit_original_response after defer (not response.edit_message)
    await interaction.edit_original_response(embed=embed, view=view)


# =============================================================================
# INVENTORY
# =============================================================================

class BagButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Bag", emoji="🎒", style=discord.ButtonStyle.secondary, row=1)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            inv        = await get_inventory(self.user_id, session)
            from game.world import get_bag_capacity, get_bag_slot_count
            capacity   = await get_bag_capacity(self.user_id, session)
            slot_count = await get_bag_slot_count(self.user_id, session)
        embed = inventory_embed(inv, 0, capacity=capacity, slot_count=slot_count)
        view  = InventoryView(self.user_id, inv, 0, capacity=capacity, slot_count=slot_count)
        await interaction.response.edit_message(embed=embed, view=view)


class InventoryView(discord.ui.View):
    def __init__(self, user_id: int, inventory: list[dict], page: int = 0,
                 capacity: int = 20, slot_count: int = 0):
        super().__init__(timeout=180)
        self.user_id    = user_id
        self.capacity   = capacity
        self.slot_count = slot_count
        total_pages     = max(1, -(-len(inventory) // 8))
        page_items      = inventory[page * 8:(page + 1) * 8]
        from game.data import get_item as _get_item

        consumable_count = 0
        for entry in page_items:
            item = _get_item(entry.get("item_id", ""))
            if not item:
                continue
            if item.get("type") == "bag_upgrade":
                self.add_item(UseBagUpgradeButton(user_id, entry["item_id"], item))
            elif item.get("type") == "consumable" and consumable_count < 4:
                self.add_item(UseItemButton(user_id, entry["item_id"], item))
                consumable_count += 1
            elif item.get("type") == "tool":
                self.add_item(EquipToolButton(user_id, entry["item_id"], item))

        if page > 0:
            self.add_item(_PageBtn(user_id, page - 1, "◀ Prev", capacity, slot_count))
        if page < total_pages - 1:
            self.add_item(_PageBtn(user_id, page + 1, "Next ▶", capacity, slot_count))
        self.add_item(BackButton(user_id))


class UseItemButton(discord.ui.Button):
    """Use a consumable item from the bag (outside battle)."""
    def __init__(self, user_id: int, item_id: str, item: dict):
        super().__init__(
            label=f"Use {item['name'][:22]}",
            emoji=item.get("emoji", "🧪"),
            style=discord.ButtonStyle.success,
        )
        self.user_id = user_id
        self.item_id = item_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            result     = await use_consumable(self.user_id, self.item_id, session)
            inv        = await get_inventory(self.user_id, session)
            from game.world import get_bag_capacity, get_bag_slot_count
            capacity   = await get_bag_capacity(self.user_id, session)
            slot_count = await get_bag_slot_count(self.user_id, session)
        embed = inventory_embed(inv, 0, capacity=capacity, slot_count=slot_count)
        embed.add_field(name="✅" if result["success"] else "❌", value=result["message"], inline=False)
        view = InventoryView(self.user_id, inv, 0, capacity=capacity, slot_count=slot_count)
        await interaction.response.edit_message(embed=embed, view=view)


class UseBagUpgradeButton(discord.ui.Button):
    def __init__(self, user_id: int, item_id: str, item: dict):
        super().__init__(label=f"Use {item['name']}", emoji=item.get("emoji", "🎒"), style=discord.ButtonStyle.success)
        self.user_id = user_id
        self.item_id = item_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            from game.world import use_bag_upgrade_item, get_bag_capacity, get_bag_slot_count
            success, msg = await use_bag_upgrade_item(self.user_id, self.item_id, session)
            inv        = await get_inventory(self.user_id, session)
            capacity   = await get_bag_capacity(self.user_id, session)
            slot_count = await get_bag_slot_count(self.user_id, session)
        embed = inventory_embed(inv, 0, capacity=capacity, slot_count=slot_count)
        embed.add_field(name="✅" if success else "❌", value=msg, inline=False)
        view = InventoryView(self.user_id, inv, 0, capacity=capacity, slot_count=slot_count)
        await interaction.response.edit_message(embed=embed, view=view)


class _PageBtn(discord.ui.Button):
    def __init__(self, user_id: int, target_page: int, label: str, capacity: int = 20, slot_count: int = 0):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.user_id     = user_id
        self.target_page = target_page
        self.capacity    = capacity
        self.slot_count  = slot_count

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            inv        = await get_inventory(self.user_id, session)
            from game.world import get_bag_capacity, get_bag_slot_count
            capacity   = await get_bag_capacity(self.user_id, session)
            slot_count = await get_bag_slot_count(self.user_id, session)
        embed = inventory_embed(inv, self.target_page, capacity=capacity, slot_count=slot_count)
        view  = InventoryView(self.user_id, inv, self.target_page, capacity=capacity, slot_count=slot_count)
        await interaction.response.edit_message(embed=embed, view=view)


# =============================================================================
# PROFILE + MAP + CARDS
# =============================================================================

class ProfileButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Profile", emoji="👤", style=discord.ButtonStyle.secondary, row=1)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        embed = profile_embed(player)
        view  = ProfileView(self.user_id, player)
        await interaction.response.edit_message(embed=embed, view=view)


class ProfileView(discord.ui.View):
    def __init__(self, user_id: int, player):
        super().__init__(timeout=180)
        self.user_id = user_id
        if player.stats.unspent_points > 0:
            self.add_item(AllocateStatsButton(user_id))
        self.add_item(CardsButton(user_id))
        self.add_item(BackButton(user_id))


class AllocateStatsButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Allocate Stat Points", emoji="⚡", style=discord.ButtonStyle.primary)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        embed = stat_allocation_embed(player)
        view  = StatAllocationView(self.user_id, player)
        await interaction.response.edit_message(embed=embed, view=view)


class CardsButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Cards", emoji="🃏", style=discord.ButtonStyle.secondary)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            collection = await get_card_collection(self.user_id, session)
        embed = card_collection_embed(collection, 0)
        view  = CardCollectionView(self.user_id, collection, 0)
        await interaction.response.edit_message(embed=embed, view=view)


class CardCollectionView(discord.ui.View):
    def __init__(self, user_id: int, collection: list, page: int = 0):
        super().__init__(timeout=180)
        self.user_id = user_id
        items_per_page = 6
        total_pages    = max(1, -(-len(collection) // items_per_page))
        if page > 0:
            self.add_item(_CardPageBtn(user_id, collection, page - 1, "◀ Prev"))
        if page < total_pages - 1:
            self.add_item(_CardPageBtn(user_id, collection, page + 1, "Next ▶"))
        self.add_item(BackToProfileButton(user_id))


class _CardPageBtn(discord.ui.Button):
    def __init__(self, user_id: int, collection: list, target_page: int, label: str):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.user_id     = user_id
        self.collection  = collection
        self.target_page = target_page

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        embed = card_collection_embed(self.collection, self.target_page)
        view  = CardCollectionView(self.user_id, self.collection, self.target_page)
        await interaction.response.edit_message(embed=embed, view=view)


class MapButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Map", emoji="🗺️", style=discord.ButtonStyle.secondary, row=1)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        embed = map_embed(player)
        view  = BackToZoneView(self.user_id)
        await interaction.response.edit_message(embed=embed, view=view)


# =============================================================================
# SHOP
# =============================================================================

class ShopView(discord.ui.View):
    def __init__(self, user_id: int, shop: dict, player_zet: int):
        super().__init__(timeout=180)
        self.user_id = user_id
        for entry in shop.get("stock", [])[:4]:
            self.add_item(BuyButton(user_id, shop, entry, player_zet))
        self.add_item(BackButton(user_id))


class BuyButton(discord.ui.Button):
    def __init__(self, user_id: int, shop: dict, entry: dict, player_zet: int):
        self.user_id  = user_id
        self.shop     = shop
        self.entry    = entry
        price         = entry.get("price", 0)
        self.price    = price
        can_afford    = player_zet >= price
        if "item_id" in entry:
            item          = get_item(entry["item_id"])
            label         = f"{item['name']} ({price:,}Ƶ)" if item else "Buy"
            self.buy_type = "item"
            self.buy_id   = entry["item_id"]
        else:
            card          = get_card(entry.get("card_id", ""))
            label         = f"{card['name']} ({price:,}Ƶ)" if card else "Buy Card"
            self.buy_type = "card"
            self.buy_id   = entry.get("card_id", "")
        super().__init__(label=label[:80], style=discord.ButtonStyle.success if can_afford else discord.ButtonStyle.secondary, disabled=not can_afford)

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            if not await deduct_zet(self.user_id, self.price, session):
                return await interaction.response.send_message("Insufficient funds!", ephemeral=True)
            if self.buy_type == "item":
                await add_item(self.user_id, self.buy_id, 1, session)
                msg = f"Purchased **{get_item(self.buy_id)['name']}**!"
            else:
                await add_card_to_collection(self.user_id, self.buy_id, session)
                await add_card_to_deck(self.user_id, self.buy_id, session)
                msg = f"Purchased **{get_card(self.buy_id)['name']}**! Added to deck."
            player = await get_full_player(self.user_id, session)
        embed = shop_embed(self.shop, player.progression.zet_wallet)
        embed.add_field(name="✅", value=msg, inline=False)
        view  = ShopView(self.user_id, self.shop, player.progression.zet_wallet)
        await interaction.response.edit_message(embed=embed, view=view)


# =============================================================================
# STORYLET
# =============================================================================

class StoryletView(discord.ui.View):
    def __init__(self, user_id: int, storylet: dict):
        super().__init__(timeout=300)
        self.user_id = user_id
        for choice in storylet.get("choices", []):
            self.add_item(StoryletChoiceButton(user_id, storylet, choice))


class StoryletChoiceButton(discord.ui.Button):
    def __init__(self, user_id: int, storylet: dict, choice: dict):
        super().__init__(label=choice["label"], style=discord.ButtonStyle.primary)
        self.user_id   = user_id
        self.storylet  = storylet
        self.choice_id = choice["id"]

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            from game.storylets import complete_storylet
            from game.world_state import get_zone_state_description_async
            outcome = await complete_storylet(
                self.user_id, self.storylet["id"], self.choice_id, session
            )
            player = await get_full_player(self.user_id, session)
            zone_id = player.progression.current_zone_id
            world_override = await get_zone_state_description_async(zone_id, self.user_id, session)
        zone  = get_zone(zone_id)
        embed = zone_embed(player, zone, world_override=world_override)
        embed.add_field(name="📜 Outcome", value=outcome.get("message", "You made your choice."), inline=False)
        view  = MainZoneView(self.user_id, player, zone)
        await interaction.response.edit_message(embed=embed, view=view)


# =============================================================================
# REUSABLE BUTTONS
# =============================================================================

class StatAllocationView(discord.ui.View):
    def __init__(self, user_id: int, player):
        super().__init__(timeout=180)
        self.user_id = user_id
        if player.stats.unspent_points > 0:
            stats = [
                ("STR", "strength", "⚔️"), ("DEF", "defense", "🛡️"), ("AGI", "agility", "💨"),
                ("INT", "intel", "🔮"), ("VIT", "vit", "💚"), ("LCK", "lck", "🍀"),
            ]
            for i, (label, stat_key, emoji) in enumerate(stats):
                self.add_item(StatButton(user_id, label, stat_key, emoji, row=0 if i < 3 else 1))
        self.add_item(BackToProfileButton(user_id))


class StatButton(discord.ui.Button):
    def __init__(self, user_id: int, label: str, stat_key: str, emoji: str, row: int):
        super().__init__(label=f"+1 {label}", emoji=emoji, style=discord.ButtonStyle.secondary, row=row)
        self.user_id    = user_id
        self.stat_key   = stat_key
        self.label_name = label

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
            stats  = player.stats
            if stats.unspent_points <= 0:
                return await interaction.response.send_message("No unspent points left.", ephemeral=True)
            current = getattr(stats, self.stat_key, 0)
            setattr(stats, self.stat_key, current + 1)
            stats.unspent_points -= 1
            player = await get_full_player(self.user_id, session)
        msg = f"✅ **+1 {self.label_name}** applied."
        if self.stat_key == "vit":
            msg += f" Max HP is now **{player.stats.vit * 5}**."
        embed = stat_allocation_embed(player, message=msg)
        view  = StatAllocationView(self.user_id, player)
        await interaction.response.edit_message(embed=embed, view=view)


class BackToProfileButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Back to Profile", emoji="👤", style=discord.ButtonStyle.secondary, row=2)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        embed = profile_embed(player)
        view  = ProfileView(self.user_id, player)
        await interaction.response.edit_message(embed=embed, view=view)


class BackButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Back", emoji="◀️", style=discord.ButtonStyle.secondary)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            from game.world_state import get_zone_state_description_async
            player = await get_full_player(self.user_id, session)
            zone_id = player.progression.current_zone_id
            world_override = await get_zone_state_description_async(zone_id, self.user_id, session)
        zone  = get_zone(zone_id)
        embed = zone_embed(player, zone, world_override=world_override)
        view  = MainZoneView(self.user_id, player, zone)
        await interaction.response.edit_message(embed=embed, view=view)


class BackToWalkButton(discord.ui.Button):
    def __init__(self, user_id: int, row: int = 2):
        super().__init__(label="Back", emoji="◀️", style=discord.ButtonStyle.secondary, row=row)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        zone  = get_zone(player.progression.current_zone_id)
        embed = zone_embed(player, zone)
        view  = MainZoneView(self.user_id, player, zone)
        await interaction.response.edit_message(embed=embed, view=view)


class BackToZoneView(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.add_item(BackButton(user_id))


# =============================================================================
# MINI-BOSS ENCOUNTER VIEW  (Phase 3)
# =============================================================================

class MiniBossEncounterView(discord.ui.View):
    def __init__(self, user_id: int, enemy_id: str, zone_id: str):
        super().__init__(timeout=300)
        self.user_id  = user_id
        self.add_item(MiniBossFightButton(user_id, enemy_id, zone_id))
        self.add_item(MiniBossFleeButton(user_id, zone_id))


class MiniBossFightButton(discord.ui.Button):
    def __init__(self, user_id: int, enemy_id: str, zone_id: str):
        super().__init__(label="Fight", emoji="⚔️", style=discord.ButtonStyle.danger, row=0)
        self.user_id  = user_id
        self.enemy_id = enemy_id
        self.zone_id  = zone_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        await interaction.response.defer()
        await _start_battle(interaction, self.user_id, self.enemy_id)


class MiniBossFleeButton(discord.ui.Button):
    def __init__(self, user_id: int, zone_id: str):
        super().__init__(label="Flee", emoji="🏃", style=discord.ButtonStyle.secondary, row=0)
        self.user_id = user_id
        self.zone_id = zone_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            await deduct_zet(self.user_id, 5, session)
            player = await get_full_player(self.user_id, session)
        zone  = get_zone(self.zone_id)
        embed = zone_embed(player, zone)
        embed.add_field(name="🏃 Fled", value="You slipped away. -5 Ƶ.", inline=False)
        view  = WalkingView(self.user_id)
        await interaction.response.edit_message(embed=embed, view=view)


# =============================================================================
# GATHERING VIEWS
# =============================================================================

class GatheringNodeView(discord.ui.View):
    def __init__(self, user_id: int, node_id: str, zone_id: str):
        super().__init__(timeout=120)
        self.user_id = user_id
        self.add_item(GatherButton(user_id, node_id, zone_id))
        self.add_item(SkipGatherButton(user_id))


class GatherButton(discord.ui.Button):
    def __init__(self, user_id: int, node_id: str, zone_id: str):
        super().__init__(label="Gather", emoji="⚒️", style=discord.ButtonStyle.success)
        self.user_id = user_id
        self.node_id = node_id
        self.zone_id = zone_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        try:
            await interaction.response.defer()
        except discord.errors.NotFound:
            return
        from game.gathering import get_node, process_gather
        node = get_node(self.node_id)
        if not node:
            return await interaction.edit_original_response(
                embed=error_embed("Node no longer available."),
                view=WalkingView(self.user_id),
            )
        async with get_session() as session:
            result = await process_gather(self.user_id, self.node_id, session)
            player = await get_full_player(self.user_id, session)
        embed = gathering_result_embed(player, node, result)
        view  = WalkingView(self.user_id)
        await interaction.edit_original_response(embed=embed, view=view)


class SkipGatherButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Keep Walking", emoji="🚶", style=discord.ButtonStyle.secondary)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        zone  = get_zone(player.progression.current_zone_id)
        embed = zone_embed(player, zone)
        view  = WalkingView(self.user_id)
        await interaction.response.edit_message(embed=embed, view=view)


class EquipToolButton(discord.ui.Button):
    """Equip a tool from the bag into its gathering slot."""
    def __init__(self, user_id: int, item_id: str, item: dict):
        super().__init__(
            label=f"Equip {item['name'][:20]}",
            emoji=item.get("emoji", "⚒️"),
            style=discord.ButtonStyle.primary,
        )
        self.user_id = user_id
        self.item_id = item_id
        self.slot    = item.get("slot", "")

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            from game.gathering import equip_tool
            from game.world import get_bag_capacity, get_bag_slot_count
            success, msg = await equip_tool(self.user_id, self.slot, self.item_id, session)
            inv        = await get_inventory(self.user_id, session)
            capacity   = await get_bag_capacity(self.user_id, session)
            slot_count = await get_bag_slot_count(self.user_id, session)
        embed = inventory_embed(inv, 0, capacity=capacity, slot_count=slot_count)
        embed.add_field(name="✅" if success else "❌", value=msg, inline=False)
        view  = InventoryView(self.user_id, inv, 0, capacity=capacity, slot_count=slot_count)
        await interaction.response.edit_message(embed=embed, view=view)


# =============================================================================
# ADVENTURER'S GUILD VIEWS
# =============================================================================

class GuildBuildingView(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=180)
        self.user_id = user_id

    @discord.ui.button(label="Daily Contracts", emoji="📋", style=discord.ButtonStyle.primary)
    async def contracts(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            from game.guild import get_daily_contracts, get_player_contracts
            daily  = await get_daily_contracts(session)
            player = await get_player_contracts(self.user_id, session)
        embed = guild_contracts_embed(daily, player)
        view  = GuildContractsView(self.user_id, daily, player)
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Leaderboard", emoji="🏆", style=discord.ButtonStyle.secondary)
    async def leaderboard(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            from game.guild import get_leaderboard
            rows = await get_leaderboard(session)
        embed = guild_leaderboard_embed(rows)
        view  = GuildLeaderboardView(self.user_id)
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Back", emoji="◀️", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        zone  = get_zone(player.progression.current_zone_id)
        embed = zone_embed(player, zone)
        view  = MainZoneView(self.user_id, player, zone)
        await interaction.response.edit_message(embed=embed, view=view)


class GuildContractsView(discord.ui.View):
    def __init__(self, user_id: int, daily_contracts: list, player_contracts: list):
        super().__init__(timeout=180)
        self.user_id = user_id
        player_map = {row.contract_id: row for row, _ in player_contracts}
        for contract in daily_contracts:
            player_c = player_map.get(contract.id)
            if player_c is None:
                self.add_item(AcceptContractButton(user_id, contract))
            elif player_c.status == "completed":
                self.add_item(ClaimContractButton(user_id, contract, player_c))
        self.add_item(GuildBackButton(user_id))


class AcceptContractButton(discord.ui.Button):
    def __init__(self, user_id: int, contract):
        from game.guild import TIER_CONFIG
        tier = TIER_CONFIG[contract.tier]
        super().__init__(label=f"Accept {contract.tier.title()}", emoji=tier["emoji"], style=discord.ButtonStyle.success)
        self.user_id     = user_id
        self.contract_id = contract.id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            from game.guild import accept_contract, get_daily_contracts, get_player_contracts
            success, msg = await accept_contract(self.user_id, self.contract_id, session)
            daily  = await get_daily_contracts(session)
            player = await get_player_contracts(self.user_id, session)
        embed = guild_contracts_embed(daily, player)
        embed.add_field(name="✅" if success else "❌", value=msg, inline=False)
        view  = GuildContractsView(self.user_id, daily, player)
        await interaction.response.edit_message(embed=embed, view=view)


class ClaimContractButton(discord.ui.Button):
    def __init__(self, user_id: int, contract, player_contract):
        from game.guild import TIER_CONFIG
        tier = TIER_CONFIG[contract.tier]
        super().__init__(label=f"Claim {contract.tier.title()}", emoji="🎁", style=discord.ButtonStyle.primary)
        self.user_id     = user_id
        self.contract_id = contract.id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            from game.guild import claim_contract, get_daily_contracts, get_player_contracts
            success, msg, rewards = await claim_contract(self.user_id, self.contract_id, session)
            daily  = await get_daily_contracts(session)
            player = await get_player_contracts(self.user_id, session)
        embed = guild_contracts_embed(daily, player)
        embed.add_field(name="✅ Claimed!" if success else "❌", value=msg, inline=False)
        view  = GuildContractsView(self.user_id, daily, player)
        await interaction.response.edit_message(embed=embed, view=view)


class GuildLeaderboardView(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.add_item(GuildBackButton(user_id))


class GuildBackButton(discord.ui.Button):
    def __init__(self, user_id: int):
        super().__init__(label="Back", emoji="◀️", style=discord.ButtonStyle.secondary)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        embed = guild_embed()
        view  = GuildBuildingView(self.user_id)
        await interaction.response.edit_message(embed=embed, view=view)


# =============================================================================
# AUCTION HOUSE / MARKET VIEWS
# =============================================================================

class BuyByIdModal(discord.ui.Modal, title="Buy Listing by ID"):
    listing_id_input = discord.ui.TextInput(
        label="Listing ID", placeholder="Enter the listing # shown in the market (e.g. 42)",
        min_length=1, max_length=6,
    )

    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
        except discord.errors.NotFound:
            return
        try:
            listing_id = int(self.listing_id_input.value.strip())
        except ValueError:
            return await interaction.edit_original_response(
                embed=error_embed("That's not a valid listing ID. Use the number shown after # in the market."),
                view=AuctionHouseView(self.user_id),
            )
        async with get_session() as session:
            from game.market import buy_listing, get_seller_names
            from core.models import MarketListing
            from sqlalchemy import select as _sel
            result  = await session.execute(_sel(MarketListing).where(MarketListing.id == listing_id))
            listing = result.scalar_one_or_none()
            if not listing or listing.status != "active":
                return await interaction.edit_original_response(
                    embed=error_embed(f"Listing **#{listing_id}** not found or no longer available."),
                    view=AuctionHouseView(self.user_id),
                )
            if listing.seller_id == self.user_id:
                return await interaction.edit_original_response(
                    embed=error_embed("That's your own listing. You can't buy it."),
                    view=AuctionHouseView(self.user_id),
                )
            item       = get_item(listing.item_id) if listing.item_id else None
            item_name  = item["name"]  if item else (listing.item_id or "Unknown")
            item_emoji = item["emoji"] if item else "📦"
            seller_names = await get_seller_names([listing], session)
            seller     = seller_names.get(listing.seller_id, "Unknown")
            price_per  = listing.price // max(listing.quantity, 1)
            success, msg = await buy_listing(self.user_id, listing_id, session)
            player = await get_full_player(self.user_id, session)
        if success:
            embed = discord.Embed(
                title="✅  Purchase Complete",
                description=(
                    f"Bought **{listing.quantity}× {item_emoji} {item_name}** from **{seller}**\n"
                    f"Paid: **{listing.price:,} Ƶ** ({price_per:,} Ƶ each)\n"
                    f"Remaining wallet: **{player.progression.zet_wallet:,} Ƶ**"
                ),
                color=0x57B05E,
            )
        else:
            embed = error_embed(msg)
        view = AuctionHouseView(self.user_id)
        await interaction.edit_original_response(embed=embed, view=view)


class AuctionHouseView(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=180)
        self.user_id = user_id

    @discord.ui.button(label="Browse Market", emoji="🔍", style=discord.ButtonStyle.primary)
    async def browse(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        await interaction.response.defer()
        async with get_session() as session:
            from game.market import get_active_listings, get_seller_names
            listings, total = await get_active_listings(session, "all", "recent", 0)
            seller_names    = await get_seller_names(listings, session)
        embed = market_browse_embed(listings, seller_names, "all", "recent", 0, total, self.user_id)
        view  = MarketBrowseView(self.user_id, listings, seller_names, "all", "recent", 0, total)
        await interaction.edit_original_response(embed=embed, view=view)

    @discord.ui.button(label="Buy by ID #", emoji="🎯", style=discord.ButtonStyle.success)
    async def buy_by_id(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        await interaction.response.send_modal(BuyByIdModal(self.user_id))

    @discord.ui.button(label="List Item", emoji="📋", style=discord.ButtonStyle.success)
    async def list_item(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            inv    = await get_inventory(self.user_id, session)
            player = await get_full_player(self.user_id, session)
        embed = market_list_item_embed(inv, player.progression.zet_wallet)
        view  = MarketListItemView(self.user_id, inv, player.progression.zet_wallet)
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="My Listings", emoji="📦", style=discord.ButtonStyle.secondary)
    async def my_listings(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            from game.market import get_player_listings
            listings = await get_player_listings(self.user_id, session)
            player   = await get_full_player(self.user_id, session)
        embed = market_my_listings_embed(listings, player.progression.zet_wallet)
        view  = MarketMyListingsView(self.user_id, listings)
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Back", emoji="◀️", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            player = await get_full_player(self.user_id, session)
        zone  = get_zone(player.progression.current_zone_id)
        embed = zone_embed(player, zone)
        view  = MainZoneView(self.user_id, player, zone)
        await interaction.response.edit_message(embed=embed, view=view)


class MarketBrowseView(discord.ui.View):
    def __init__(self, user_id, listings, seller_names, current_filter, current_sort, page, total):
        super().__init__(timeout=180)
        self.user_id        = user_id
        self.listings       = listings
        self.seller_names   = seller_names
        self.current_filter = current_filter
        self.current_sort   = current_sort
        self.page           = page
        self.total          = total
        for label, ftype in [("All","all"),("🧪 Potion","consumable"),("🪨 Material","material"),("🌿 Craft","crafting")]:
            self.add_item(MarketFilterBtn(user_id, ftype, label, ftype == current_filter))
        for label, stype in [("🆕 Recent","recent"),("💰 Cheapest","cheapest"),("⏳ Expiring","expiring")]:
            self.add_item(MarketSortBtn(user_id, stype, label, stype == current_sort, current_filter))
        from game.market import PAGE_SIZE
        shown = 0
        for listing in listings:
            if shown >= 3:
                break
            if listing.seller_id != user_id:
                self.add_item(BuyListingButton(user_id, listing, row=2))
                shown += 1
        total_pages = max(1, -(-total // PAGE_SIZE))
        if page > 0:
            self.add_item(MarketNavBtn(user_id, current_filter, current_sort, page - 1, "◀ Prev", row=3))
        self.add_item(MarketNavBtn(user_id, current_filter, current_sort, page + 1, "Next ▶", row=3, disabled=page >= total_pages - 1))
        self.add_item(MarketBackButton(user_id, row=3))


class MarketFilterBtn(discord.ui.Button):
    def __init__(self, user_id, ftype, label, active):
        super().__init__(label=label, style=discord.ButtonStyle.primary if active else discord.ButtonStyle.secondary, row=0)
        self.user_id = user_id
        self.ftype   = ftype

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        await interaction.response.defer()
        async with get_session() as session:
            from game.market import get_active_listings, get_seller_names
            listings, total = await get_active_listings(session, self.ftype, "recent", 0)
            seller_names    = await get_seller_names(listings, session)
        embed = market_browse_embed(listings, seller_names, self.ftype, "recent", 0, total, self.user_id)
        view  = MarketBrowseView(self.user_id, listings, seller_names, self.ftype, "recent", 0, total)
        await interaction.edit_original_response(embed=embed, view=view)


class MarketSortBtn(discord.ui.Button):
    def __init__(self, user_id, stype, label, active, current_filter):
        super().__init__(label=label, style=discord.ButtonStyle.primary if active else discord.ButtonStyle.secondary, row=1)
        self.user_id        = user_id
        self.stype          = stype
        self.current_filter = current_filter

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        await interaction.response.defer()
        async with get_session() as session:
            from game.market import get_active_listings, get_seller_names
            listings, total = await get_active_listings(session, self.current_filter, self.stype, 0)
            seller_names    = await get_seller_names(listings, session)
        embed = market_browse_embed(listings, seller_names, self.current_filter, self.stype, 0, total, self.user_id)
        view  = MarketBrowseView(self.user_id, listings, seller_names, self.current_filter, self.stype, 0, total)
        await interaction.edit_original_response(embed=embed, view=view)


class MarketNavBtn(discord.ui.Button):
    def __init__(self, user_id, ftype, stype, target_page, label, row=3, disabled=False):
        super().__init__(label=label, style=discord.ButtonStyle.secondary, row=row, disabled=disabled)
        self.user_id     = user_id
        self.ftype       = ftype
        self.stype       = stype
        self.target_page = target_page

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        await interaction.response.defer()
        async with get_session() as session:
            from game.market import get_active_listings, get_seller_names
            listings, total = await get_active_listings(session, self.ftype, self.stype, self.target_page)
            seller_names    = await get_seller_names(listings, session)
        embed = market_browse_embed(listings, seller_names, self.ftype, self.stype, self.target_page, total, self.user_id)
        view  = MarketBrowseView(self.user_id, listings, seller_names, self.ftype, self.stype, self.target_page, total)
        await interaction.edit_original_response(embed=embed, view=view)


class BuyListingButton(discord.ui.Button):
    def __init__(self, user_id, listing, row=2):
        item  = get_item(listing.item_id) if listing.item_id else None
        emoji = item["emoji"] if item else "📦"
        name  = (item["name"] if item else (listing.item_id or "Item"))[:15]
        super().__init__(label=f"Buy {name} — {listing.price:,}Ƶ", emoji=emoji, style=discord.ButtonStyle.success, row=row)
        self.user_id    = user_id
        self.listing_id = listing.id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            from game.market import buy_listing, get_active_listings, get_seller_names
            success, msg    = await buy_listing(self.user_id, self.listing_id, session)
            listings, total = await get_active_listings(session, "all", "recent", 0)
            seller_names    = await get_seller_names(listings, session)
        embed = market_browse_embed(listings, seller_names, "all", "recent", 0, total, self.user_id)
        embed.add_field(name="✅" if success else "❌", value=msg, inline=False)
        view  = MarketBrowseView(self.user_id, listings, seller_names, "all", "recent", 0, total)
        await interaction.response.edit_message(embed=embed, view=view)


class MarketListItemView(discord.ui.View):
    def __init__(self, user_id, inventory, player_zet):
        super().__init__(timeout=180)
        self.user_id    = user_id
        self.player_zet = player_zet
        from game.market import UNLISTED_ITEM_TYPES
        listable = [e for e in inventory if (get_item(e["item_id"]) or {}).get("type") not in UNLISTED_ITEM_TYPES]
        for entry in listable[:4]:
            item = get_item(entry["item_id"])
            if item:
                self.add_item(SelectListItemButton(user_id, entry, item))
        self.add_item(MarketBackButton(user_id))


class SelectListItemButton(discord.ui.Button):
    def __init__(self, user_id, entry, item):
        super().__init__(label=f"{item['name']} ×{entry['quantity']}", emoji=item["emoji"], style=discord.ButtonStyle.secondary)
        self.user_id = user_id
        self.item_id = entry["item_id"]
        self.max_qty = entry["quantity"]
        self.item    = item

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        await interaction.response.send_modal(SetPriceModal(self.user_id, self.item_id, self.item, self.max_qty))


class SetPriceModal(discord.ui.Modal, title="List Item for Sale"):
    quantity_input = discord.ui.TextInput(label="Quantity", placeholder="How many to sell?", min_length=1, max_length=4, default="1")
    price_input    = discord.ui.TextInput(label="Price per unit (Ƶ)", placeholder="e.g. 50", min_length=1, max_length=6)

    def __init__(self, user_id, item_id, item, max_qty):
        super().__init__()
        self.user_id = user_id
        self.item_id = item_id
        self.item    = item
        self.max_qty = max_qty

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
        except discord.errors.NotFound:
            return
        try:
            qty   = int(self.quantity_input.value.strip())
            price = int(self.price_input.value.strip())
        except ValueError:
            return await interaction.edit_original_response(
                embed=error_embed("Quantity and price must be numbers."),
                view=MarketBackButton(self.user_id),
            )
        async with get_session() as session:
            from game.market import create_listing
            success, msg = await create_listing(self.user_id, self.item_id, qty, price, session)
            inv    = await get_inventory(self.user_id, session)
            player = await get_full_player(self.user_id, session)
        embed = market_list_item_embed(inv, player.progression.zet_wallet)
        embed.add_field(name="✅" if success else "❌", value=msg, inline=False)
        view  = MarketListItemView(self.user_id, inv, player.progression.zet_wallet)
        await interaction.edit_original_response(embed=embed, view=view)


class MarketMyListingsView(discord.ui.View):
    def __init__(self, user_id, listings):
        super().__init__(timeout=180)
        self.user_id = user_id
        for listing in listings[:4]:
            self.add_item(CancelListingButton(user_id, listing))
        self.add_item(MarketBackButton(user_id))


class CancelListingButton(discord.ui.Button):
    def __init__(self, user_id, listing):
        item = get_item(listing.item_id)
        name = (item["name"] if item else listing.item_id)[:15]
        super().__init__(label=f"Cancel {name}", emoji="❌", style=discord.ButtonStyle.danger)
        self.user_id    = user_id
        self.listing_id = listing.id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            from game.market import cancel_listing, get_player_listings
            success, msg = await cancel_listing(self.user_id, self.listing_id, session)
            listings = await get_player_listings(self.user_id, session)
            player   = await get_full_player(self.user_id, session)
        embed = market_my_listings_embed(listings, player.progression.zet_wallet)
        embed.add_field(name="✅" if success else "❌", value=msg, inline=False)
        view  = MarketMyListingsView(self.user_id, listings)
        await interaction.response.edit_message(embed=embed, view=view)


class MarketBackButton(discord.ui.Button):
    def __init__(self, user_id, row=3):
        super().__init__(label="Back", emoji="◀️", style=discord.ButtonStyle.secondary, row=row)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        embed = market_browse_embed([], {}, "all", "recent", 0, 0, self.user_id)
        view  = AuctionHouseView(self.user_id)
        await interaction.response.edit_message(embed=embed, view=view)


# =============================================================================
# NPC SELL VIEWS
# =============================================================================

class NPCSellView(discord.ui.View):
    def __init__(self, user_id, npc_id, sellable, player_zet):
        super().__init__(timeout=180)
        self.user_id    = user_id
        self.npc_id     = npc_id
        self.player_zet = player_zet
        for entry in sellable[:5]:
            item = get_item(entry["item_id"])
            if item:
                self.add_item(SellToNPCButton(user_id, npc_id, entry, item))
        self.add_item(BackButton(user_id))


class SellToNPCButton(discord.ui.Button):
    def __init__(self, user_id, npc_id, entry, item):
        total = entry["buy_price"] * entry["quantity"]
        super().__init__(label=f"Sell all {item['name']} (+{total:,}Ƶ)", emoji=item["emoji"], style=discord.ButtonStyle.success)
        self.user_id  = user_id
        self.npc_id   = npc_id
        self.item_id  = entry["item_id"]
        self.quantity = entry["quantity"]

    async def callback(self, interaction: discord.Interaction):
        if _not_your_game(interaction, self.user_id):
            return await interaction.response.send_message("Not your game!", ephemeral=True)
        async with get_session() as session:
            from game.market import get_sellable_inventory, sell_to_npc
            success, msg = await sell_to_npc(self.user_id, self.item_id, self.quantity, self.npc_id, session)
            sellable = await get_sellable_inventory(self.user_id, self.npc_id, session)
            player   = await get_full_player(self.user_id, session)
        npc   = get_npc(self.npc_id)
        embed = npc_sell_embed(sellable, npc, player.progression.zet_wallet)
        embed.add_field(name="✅" if success else "❌", value=msg, inline=False)
        view  = NPCSellView(self.user_id, self.npc_id, sellable, player.progression.zet_wallet)
        await interaction.edit_original_response(embed=embed, view=view)