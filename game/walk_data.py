# =============================================================================
# WALK SYSTEM DATA
# Add this to the bottom of your game/data.py file
# =============================================================================

# ---------------------------------------------------------------------------
# TRAVEL LINES
# Short atmospheric lines shown when moving between zones.
# Key format: "from_zone_id:to_zone_id"
# ---------------------------------------------------------------------------

TRAVEL_LINES: dict[str, list[str]] = {
    "town_square:port_district": [
        "You head downhill toward the water. The smell of salt reaches you before the sea does.",
        "The streets narrow as you approach the port. Fewer Council badges down here.",
        "A cart loaded with crates rumbles past you toward the docks. The driver doesn't look at you.",
    ],
    "town_square:market_quarter": [
        "The market noise finds you before the stalls do. Someone is arguing about a price.",
        "You pass the eastern gate. A tax collector stands at the corner with a clipboard.",
        "The smell of fresh bread and old fish. The Market Quarter's particular perfume.",
    ],
    "town_square:farmlands": [
        "The city thins out. Buildings give way to fences. Fences give way to fields.",
        "A farmer passes you going the other way, shoulders set like someone carrying more than they're holding.",
        "Open sky. You'd forgotten what that looked like without buildings cutting it up.",
    ],
    "town_square:residential_ward": [
        "Quieter here. Every door has something posted on it. You don't read them.",
        "Children playing in the street go quiet when you pass, then start up again when you're gone.",
        "The houses are modest and close together. People here know each other's business.",
    ],
    "port_district:harbour_docks": [
        "The dock road is slick. Someone's been moving cargo in the wet.",
        "You hear the harbour before you see it. Ropes, water, the creak of wood under weight.",
        "A tax collector walking the other direction writes something in a ledger without breaking stride.",
    ],
    "port_district:town_square": [
        "Uphill. The Council buildings get taller as you go.",
        "You pass a poster for something. Someone has drawn on it. You keep walking.",
        "The port noise fades behind you. The city noise replaces it.",
    ],
    "port_district:smugglers_trail": [
        "You take the back road. It's not on any official map.",
        "The path is narrow and deliberately unclear. Someone maintains it without wanting to be known for it.",
        "Quieter than it should be for a route this well-worn.",
    ],
    "harbour_docks:fishermans_cove": [
        "Past the official docks, the path gets rougher. Nobody bothers paving what the Council doesn't claim.",
        "The boats here are older. More honest, somehow.",
        "The smell changes — less cargo, more fish. The real working waterfront.",
    ],
    "harbour_docks:port_district": [
        "Back up the dock road. Your boots are damp.",
        "The official harbour gives way to the port district. More eyes here.",
        "A Council soldier gives you a second look. You give them nothing back.",
    ],
    "farmlands:ashwood_forest": [
        "The fields end at the treeline. The trees are old and the light changes when you step under them.",
        "Someone has cleared the brush near the entrance. Recently. Deliberately.",
        "The forest takes the sound away. Birds, wind, then nothing but your footsteps.",
    ],
    "farmlands:town_square": [
        "Back toward the city. The fields shrink behind you.",
        "A rent collector on horseback passes you going the other way. You step aside.",
        "The smell of soil gives way to stone and smoke.",
    ],
    "ashwood_forest:farmlands": [
        "You come out of the trees into open air. The light hits differently out here.",
        "The forest releases you. Or lets you go.",
        "Fields again. The forest feels closer than the distance suggests.",
    ],
    "ashwood_forest:smugglers_trail": [
        "The trail cuts through the forest at an angle that doesn't match any official road.",
        "Cart tracks here. Heavy ones. Going somewhere they shouldn't.",
        "You follow the path that someone tried not to make obvious.",
    ],
    "ashwood_forest:ancient_ruins": [
        "Deeper in. The trees get older. The path gets less like a path.",
        "You find the ruins the way you find things that don't want to be found — by looking for something else.",
        "Old stone through the trees. Whatever this place was, it was here before the forest.",
    ],
    "ashwood_forest:cursed_grove": [
        "The grove announces itself before you reach it. The trees go wrong at the edges.",
        "Something in the light here. Not darkness exactly. More like light that's forgotten what it's for.",
        "You feel it before you see it. The air is different. Wrong temperature.",
    ],
    "smugglers_trail:port_district": [
        "You come out near the port. Nobody saw you come from that direction. Probably.",
        "The back route deposits you into the port district like it was never there.",
        "Official road again. You adjust your expression accordingly.",
    ],
    "smugglers_trail:ashwood_forest": [
        "The trail leads into the trees. The trees close behind you.",
        "Into the forest. The cart tracks are fresher here.",
        "You follow the path nobody's supposed to know about.",
    ],
    "fishermans_cove:harbour_docks": [
        "Back up the coast road toward the official docks.",
        "The cove falls behind you. Older boats. Older debts.",
        "The path from the cove is worn but not maintained. Fishermen don't ask for much.",
    ],
    "fishermans_cove:sea_caves": [
        "Down to the waterline. The tide is out. The caves are open.",
        "The rocks are slippery. The cave entrance breathes cold air.",
        "You time it between waves. The caves go deep.",
    ],
    "ancient_ruins:ashwood_forest": [
        "Back through the trees. The ruins watch you leave.",
        "The forest between you and the ruins feels shorter on the way back.",
        "You retrace your steps. The path looks different going the other way.",
    ],
    "ancient_ruins:cursed_grove": [
        "The grove is close to the ruins. Whatever happened here, it spread.",
        "From old stone to black trees. The corruption has a direction.",
        "You walk the border between what was built and what went wrong.",
    ],
    "ancient_ruins:shadow_den": [
        "Deeper into the ruins. You know where you're going now.",
        "The mercenary compound sits in what was once something else. They didn't clean it up. Just occupied it.",
        "You've been here before. The guards remember faces.",
    ],
    "cursed_grove:ashwood_forest": [
        "Out of the grove. The normal forest feels almost warm by comparison.",
        "The light normalises as you leave. You hadn't noticed how wrong it was until it was right again.",
        "Back into the ordinary dark of the forest.",
    ],
    "cursed_grove:ancient_ruins": [
        "The ruins are visible from the grove's edge. Both are old. Both are wrong, differently.",
        "From black trees to cracked stone.",
        "You walk the broken ground between the grove and the ruins.",
    ],
    "sea_caves:fishermans_cove": [
        "Back out through the cave mouth. The tide is coming in. You move quickly.",
        "The caves release you into the open air. Salt and light.",
        "Out of the dark. The cove is bright after the caves.",
    ],
    "shadow_den:ancient_ruins": [
        "Back through the ruins. The mercenaries watch you leave. That's fine.",
        "Out of the compound. The ruins feel quieter without armed men in them.",
        "You retrace the path through cracked stone and old silence.",
    ],
    "residential_ward:town_square": [
        "Back toward the center. The residential ward falls quiet behind you.",
        "The main streets again. More noise. More Council presence.",
        "From the quiet streets to the square. Different kind of watched.",
    ],
}

# Default travel line if specific route not defined
DEFAULT_TRAVEL_LINES = [
    "You make your way through Ironhaven.",
    "The city moves around you as you walk.",
    "One foot in front of the other. Ironhaven doesn't care where you're going.",
    "You navigate the streets by instinct now.",
]


def get_travel_line(from_zone: str, to_zone: str) -> str:
    import random
    key = f"{from_zone}:{to_zone}"
    lines = TRAVEL_LINES.get(key, DEFAULT_TRAVEL_LINES)
    return random.choice(lines)


# ---------------------------------------------------------------------------
# WALK ATMOSPHERE POOLS
# What players see when they tap Walk.
# Each zone has: atmosphere lines, npc_moments, discoveries, quotes
# ---------------------------------------------------------------------------

WALK_DATA: dict[str, dict] = {
    "town_square": {
        "atmosphere": [
            "A Council soldier leans against the fountain, watching the square. Not looking for anything specific. Just watching.",
            "The Adventurer's Guild board has new contracts posted this morning. Someone has already torn one down.",
            "A child runs past you chasing a cat. Their parent calls after them from a doorway. Normal life, performed.",
            "Mercer's portrait watches from the eastern wall. Someone has drawn a small fish beneath it in chalk.",
            "Two merchants argue in lowered voices near the guild steps. They stop when they notice you.",
            "The morning crowd moves with the particular rhythm of people who've learned not to dawdle near guards.",
            "A street sweeper works the cobblestones slowly, methodically. They've been doing this for thirty years.",
            "The fountain in the center hasn't been cleaned recently. The water is slightly green.",
            "A notice has been pinned to the guild board: 'OUTSTANDING DEBT — SEE COUNCIL HALL.' The name is torn off.",
            "The square smells like bread from the inn and something chemical from the direction of the docks.",
            "A pair of guards do a slow circuit of the square. They walk like men who aren't expecting trouble but wouldn't mind some.",
            "An old woman feeds pigeons near the fountain. She's been doing it every morning for as long as anyone can remember.",
            "The Council Hall doors are open. No one is going in. No one is coming out.",
            "Someone has left a bouquet of flowers at the base of Mercer's portrait. They're wilting.",
            "A boy is selling newspapers near the guild steps. The headline is about improved shipping efficiencies.",
        ],
        "npc_moments": [
            {"npc": "captain_rel", "line": "Captain Rel crosses the square at a measured pace, eyes moving. They nod at you once. A professional acknowledgment."},
            {"npc": "captain_rel", "line": "Rel is watching the Council Hall from the training ground entrance. They don't look at you, but they speak anyway. 'Place like this teaches you what to watch for. Most people never learn.'"},
            {"npc": "captain_rel", "line": "You pass Rel drilling alone in the training yard. They don't pause. 'Discipline isn't about the days you feel like it,' they say, to no one in particular."},
        ],
        "discoveries": [
            {"text": "Behind the Guild notice board you find a scrap of paper wedged in the wood. A list of names. One is circled. You don't recognise any of them yet.", "item": None},
            {"text": "Near the fountain base: a coin that's been filed down on one side. Not Ironhaven currency. Not from anywhere you recognise.", "item": "unknown_coin"},
            {"text": "A notice on the Council Hall door that wasn't there yesterday. 'ZONE 7 ACCESS RESTRICTED — COUNCIL AUTHORITY.' Zone 7 doesn't appear on any public map.", "item": None},
            {"text": "In the gap between two paving stones, something glints. A small brass button with a bird emblem you've seen somewhere before.", "item": None},
        ],
        "quotes": [
            ("\"The debt doesn't forgive. Neither does the sea.\"", "Old Ironhaven proverb"),
            ("\"Before Mercer, the square had a market on Sundays. Real one, not sanctioned.\"", "Unnamed resident"),
            ("\"Keep your head down and your papers current. That's the advice.\"", "Dockworker, overheard"),
            ("\"The portrait wasn't always there. That's all I'll say.\"", "Old woman, feeding pigeons"),
            ("\"Opportunity looks like patience. Most people mistake the two.\"", "Captain Rel"),
        ],
        "lore": [
            "📖 Town Square is High Security — guards patrol constantly. PvP is disabled here.",
            "📖 The Adventurer's Guild offers daily contracts. Check the board for repeatable quests.",
            "📖 Mercer's Bank charges interest on all deposited funds. But it's safer than carrying Zet.",
            "📖 The Council Hall processes citizenship and debt documentation. Wanted levels can be cleared here.",
            "📖 The clinic offers full HP restoration for a fee — cheaper than potions in a long run.",
        ],
    },

    "market_quarter": {
        "atmosphere": [
            "Shopkeepers smile at precisely the right moments. You've started noticing the timing.",
            "A tax collector walks the market row with a clipboard, pausing at each stall. The merchants produce their papers without being asked.",
            "The smell of fresh bread, salted fish, and something sweet from the tailor's shop.",
            "Prices are posted clearly at every stall. Mercer sets them. The merchants add nothing.",
            "Two sailors argue over a card at the card shop entrance. Vex watches from inside without expression.",
            "A customer leaves the general store with less than they came in with. Tomás waves them off warmly.",
            "The equipment shop has a new display in the window. Functional, not decorative. Everything here is functional.",
            "Market noise: bartering, footsteps, the specific creak of a cart wheel that needs oil.",
            "A child tries to steal an apple from a fruit stall. The merchant sees them. Lets it go. The apple was going to bruise anyway.",
            "The auction house board has seventeen active listings. You scan them without stopping.",
            "Nurse Hana's shop is meticulously clean, visible through the window. Everything labeled. Everything in its place.",
            "Old Tomás talks to every customer the same way — like they're the most interesting person he's seen all week.",
        ],
        "npc_moments": [
            {"npc": "old_tomas", "line": "Tomás spots you from his doorway and raises a hand. 'Ah! I was just thinking — do you need anything? I have fresh stock.' He pauses. 'The pastries are from this morning.'"},
            {"npc": "nurse_hana", "line": "Hana steps out of her shop for a moment, looks up at the sky, then goes back in. She didn't see you. Or pretended not to."},
            {"npc": "vex", "line": "You pass the card shop. Vex is in the window, arranging cards. They look up at you for exactly one second, then back down. That one second felt like an assessment."},
            {"npc": "old_tomas", "line": "Tomás is moving things around in his window display that don't need moving. He's been in there since early morning. The pastry plate is untouched."},
        ],
        "discoveries": [
            {"text": "Under the auction house notice board, half-buried under a loose cobblestone: a small sealed envelope with no name on it.", "item": None},
            {"text": "The equipment shop has a card in the corner of its display that isn't for sale. A handwritten tag: 'NOT STOCK. DO NOT PRICE.' The card has no class marking.", "item": None},
            {"text": "Tomás's shop has a closed sign on a day when it should be open. It's only for an hour. He's in the back. You can hear him, very quiet.", "item": None},
        ],
        "quotes": [
            ("\"Good prices mean the man setting them controls the market. Remember that.\"", "Merchant, unnamed"),
            ("\"I keep everything labeled. It's the one thing I can control.\"", "Nurse Hana"),
            ("\"The cards you need aren't always the cards you want.\"", "Vex"),
            ("\"My son used to help me on the buying days.\"", "Old Tomás, to no one"),
            ("\"Every transaction is a relationship. Some are just shorter than others.\"", "Vex"),
        ],
        "lore": [
            "📖 The Gilded Draw sells rare cards that rotate weekly. Check Vex's stock regularly.",
            "📖 The Auction House charges a 2% listing fee and 5% on successful sales.",
            "📖 Nurse Hana's Potion Emporium stocks Smelling Salts — the only way to survive lethal damage.",
            "📖 Old Tomás gives small discounts to regulars. Visit him often.",
            "📖 The Market Quarter is High Security — no PvP, no enemy spawns.",
        ],
    },

    "port_district": {
        "atmosphere": [
            "Salt air and the creak of rigging from the harbour below.",
            "A sailor argues loudly about cargo weight with a dock official. Nobody else pays attention.",
            "The guard patrol here is lazy. Two men, slow circuit, long pauses at the tavern.",
            "Ships from everywhere. A Fishman crew unloads crates without speaking.",
            "The harbour office light is on late. Maren never seems to leave.",
            "Smell of tar and rope and something chemical that might be preservative.",
            "A drunk sailor sleeps against the tavern wall. Someone has put a hat over his face. Kind gesture.",
            "Three men in Mercer's badges stand near the dock road watching the water. They're not dock workers.",
            "The evening crowd in the port is different from the day crowd. Quieter. More purposeful.",
            "Bora's tavern is full. You can hear it from here. Laughter, then a cheer, then more laughter.",
            "A wanted notice has been posted on the harbour office wall. The drawing doesn't look like anyone. They never do.",
            "The smell of the port changes at high tide. More immediate. More honest.",
        ],
        "npc_moments": [
            {"npc": "maren", "line": "Maren passes you on the dock road with a ledger under her arm and the expression of someone doing math. She acknowledges you with a nod that says she noticed but doesn't have time."},
            {"npc": "bora", "line": "Bora leans out of the tavern door to dump a bucket of something and spots you. 'Come in when you're done wandering! I'll remember your order eventually!'"},
            {"npc": "maren", "line": "You see Maren at the edge of the dock, looking at the water. She's not working. She's just standing there. When she notices you she picks up her clipboard immediately."},
        ],
        "discoveries": [
            {"text": "Between two dock warehouses: a crate with a manifest tag that doesn't match the standard Council format. Different ink, different seal.", "item": None},
            {"text": "A sailor presses something into your hand without making eye contact and walks on. A folded note. It says: 'Don't take the night ferry. Don't ask why.'", "item": None},
            {"text": "Near the harbour office steps: a dropped cargo token stamped with a marking you've seen somewhere in the Ashwood forest reports.", "item": None},
        ],
        "quotes": [
            ("\"The port doesn't move faster because you're watching it.\"", "Maren"),
            ("\"Ships come and go. The debts stay.\"", "Dockworker"),
            ("\"Everyone who walks through that door has a story. I collect them.\"", "Bora"),
            ("\"Cargo doesn't lie. Manifests do.\"", "Maren"),
            ("\"You know what the soldiers complain about when they're drunk? The ore schedule.\"", "Bora, quietly"),
        ],
        "lore": [
            "📖 The Port District is Medium Security — some enemy spawns, lighter guard presence.",
            "📖 Maren's relationship is key to Arc 1. Visit her harbour office regularly.",
            "📖 Bora at the Sailors' Tavern remembers everything. The more you visit, the more she shares.",
            "📖 Smuggler's Trail connects the port to Ashwood Forest. It's not on official maps.",
            "📖 PvP is disabled in the Port District but enabled in Harbour Docks.",
        ],
    },

    "harbour_docks": {
        "atmosphere": [
            "Crates stacked six high along the dock road. Most are labeled. Some aren't.",
            "The tide is going out. The smell changes when that happens.",
            "A tax collector with a clipboard walks the dockside at a pace that suggests they've found something.",
            "Four men unload a ship in practiced silence. The cargo is heavy. They don't look at each other.",
            "The water here is darker than it should be. Probably the runoff from the ore processing.",
            "A gull lands on the nearest crate and immediately flies off. Even the birds don't linger.",
            "A night shift supervisor counts crates by lamplight, lips moving silently.",
            "The docks at this hour are quieter. The work doesn't stop but the people doing it try to be invisible.",
            "One of the dock workers has a dark stain on their hands that isn't standard cargo residue.",
        ],
        "npc_moments": [],
        "discoveries": [
            {"text": "Behind a stack of marked crates: an unmarked one. Warm to the touch. The wood around the seams is slightly discoloured.", "item": None},
            {"text": "A dropped manifest page in the dock water gap. Partly soaked but readable. The destination column has been edited.", "item": None},
        ],
        "quotes": [
            ("\"Count twice. Report once. Forget the rest.\"", "Dock supervisor"),
            ("\"The cargo doesn't ask where it's going.\"", "Dockworker"),
            ("\"Things move through this harbour that the manifest doesn't mention.\"", "Sailor, drunk"),
        ],
        "lore": [
            "📖 Harbour Docks has Medium Security with enemy spawns — Bandit Scouts and Port Pickpockets.",
            "📖 Connected to Fisherman's Cove — continue south for Low Security zones.",
            "📖 Rare drops from dock enemies sometimes include cargo manifests — story items.",
        ],
    },

    "farmlands": {
        "atmosphere": [
            "The harvest looks good. That means the collectors will be here soon.",
            "A farmer watches you from their field without waving. Not hostile. Just tired.",
            "Forty percent. That's what Mercer takes from every harvest. Before the farmer touches a grain.",
            "Wind across the fields. The crops move. The people working them don't, much.",
            "A rent collector rides past on horseback going toward town. The farmers don't look up.",
            "Open sky. You keep forgetting Ironhaven has this much of it.",
            "A child runs between the rows of crops playing something. The parents are too tired to call them back.",
            "The road through the farmlands is well-maintained. Council maintained. They need it clear for collection days.",
            "A dog barks twice at you from behind a fence. Fence is in good repair. The barn behind it isn't.",
            "Someone has marked the edge of their plot with small stones. Boundary dispute, probably. There are always boundary disputes.",
        ],
        "npc_moments": [],
        "discoveries": [
            {"text": "In the ditch beside the farm road: a broken cart wheel and scattered grain. Recent. The grain is still dry.", "item": None},
            {"text": "Near the forest edge, hidden under a loose fence post: a small tin box. Inside: three carved wooden figures and a folded letter.", "item": None},
        ],
        "quotes": [
            ("\"Good land. Not our land, but good land.\"", "Farmer, unnamed"),
            ("\"The forty percent doesn't leave room for a bad season.\"", "Farmworker"),
            ("\"Before Mercer, we sold at the Sunday market. Made enough. Not anymore.\"", "Older farmer"),
        ],
        "lore": [
            "📖 Farmlands is Medium Security — Bandit Scout spawns at the forest edge.",
            "📖 Gathering nodes here yield crops and seeds. Sell at market or use for daily quests.",
            "📖 The forest border is where Bandit activity begins. Stay alert near the treeline.",
        ],
    },

    "ashwood_forest": {
        "atmosphere": [
            "The trees close in. Sound behaves differently in here.",
            "Something moved at the edge of your vision. When you look, nothing.",
            "Cart tracks on a path that isn't on any official map. Heavy cargo, recently.",
            "The light is wrong in here. Has been for a while, people say. You're starting to understand what they mean.",
            "A bird call you don't recognise. Then silence. Then nothing at all.",
            "The trees are old. Older than Ironhaven. They remember something the city has forgotten.",
            "You find a snapped torch handle half-buried in the undergrowth. The burn end is recent.",
            "The undergrowth here has been cleared in places. Deliberately. A corridor, almost.",
            "The forest smell: pine, earth, and underneath that, something mineral. Iron, maybe.",
            "A marker tied to a tree at eye height. Not a trail marker. Different shape, different knot.",
            "Your footsteps are louder here than they should be. The forest absorbs other sounds but not yours.",
            "The path splits. Both directions look equally unused. One of them is lying.",
        ],
        "npc_moments": [],
        "discoveries": [
            {"text": "Between two old oaks: a rope tied at chest height across the path. Trip wire. Freshly set.", "item": None},
            {"text": "A campsite, cold. Three bedrolls, a fire pit, empty ration tins. They left quickly and didn't want to be found.", "item": None},
            {"text": "Nailed to a tree where you almost miss it: a torn piece of canvas with coordinates written in charcoal. The numbers mean something to someone.", "item": None},
            {"text": "Black ore, naturally occurring, pushing through the rock face beside the path. This vein is unregistered. Mercer doesn't know it's here. Yet.", "item": "black_ore_fragment"},
        ],
        "quotes": [
            ("\"The forest was declared protected. Nobody asked what it was being protected from.\"", "Unnamed farmworker"),
            ("\"I've heard cart wheels in there at night. Official carts don't run at night.\"", "Farmer near the treeline"),
            ("\"Don't follow the cart tracks. I mean it.\"", "Maren, quietly"),
            ("\"The trees hear things. I know that sounds wrong. I don't care.\"", "Old Grull"),
        ],
        "lore": [
            "📖 Ashwood Forest is Low Security — Bandit Warriors, Archers, and Dire Wolves spawn here.",
            "📖 PvP is enabled. Other players can challenge you in this zone.",
            "📖 The forest connects to Smuggler's Trail, Ancient Ruins, and Cursed Grove.",
            "📖 Black ore fragments drop from Corrupted enemies and can also be found while walking.",
            "📖 Enemy level range: 8-15. Recommended player level: 8-14.",
        ],
    },

    "cursed_grove": {
        "atmosphere": [
            "The trees have gone black at the roots. Not burned. Something else.",
            "An animal watches you from the shadows. Its eyes catch light that isn't there.",
            "The air temperature drops two degrees when you step into the grove. You feel it immediately.",
            "The ground here doesn't crunch underfoot. It gives, slightly, like something underneath it is soft.",
            "Insects but no birds. Insects don't seem to mind what's happened here.",
            "The black color on the trees moves upward from the roots. A progression. It started somewhere.",
            "You hear something that might be breathing that isn't yours.",
            "The ore deposits here are larger than in the forest. Exposed. Wrong.",
            "A path through the grove, pressed flat by passage. Something moves through here regularly.",
            "The light here is dim but sourceless. No shadows point in a consistent direction.",
        ],
        "npc_moments": [
            {"npc": "the_watcher", "line": "Something is watching you from between the black-barked trees. When you look directly, it's gone. When you look away, it's closer."},
        ],
        "discoveries": [
            {"text": "A wolf, dead, half-buried in corrupted earth. Its fur has the same dark staining as the tree roots. Whatever happened here, it's spreading.", "item": None},
            {"text": "At the center of the grove: a ring of stones arranged deliberately. Inside the ring, the corruption is heaviest. This was where it started.", "item": None},
            {"text": "A black ore fragment lying exposed on the surface. It's warm. Much warmer than the air temperature explains.", "item": "black_ore_fragment"},
        ],
        "quotes": [
            ("\"The grove was normal forest six months ago. I watched it change.\"", "The Watcher"),
            ("\"Don't take the ore. It takes something back.\"", "Unknown"),
            ("\"Whatever the ore does to animals, it does it faster now.\"", "Ranger, unnamed"),
        ],
        "lore": [
            "📖 The Cursed Grove is Null Security — no law, full PvP, Corrupted Wolves and Forest Witch spawn.",
            "📖 Corrupted enemies drop Black Ore Fragments — a key story item for Arc 1.",
            "📖 The Watcher can be found here. Their relationship mechanics work differently from other NPCs.",
            "📖 Enemy level range: 15-25. Do not enter below level 14.",
        ],
    },

    "ancient_ruins": {
        "atmosphere": [
            "No wind. The silence feels deliberate.",
            "Footprints in the dust that aren't yours. Recent.",
            "Old stone remembers. You can't say how you know that.",
            "Whatever this place was, it was built by people who expected it to last.",
            "The carvings on the walls are in a script you don't recognise. Nobody does.",
            "Your voice, if you used it, would echo longer than the space explains.",
            "Something has been moved recently. A stone block, shifted. Fresh scrape marks.",
            "The ruins sit in a clearing. The forest doesn't grow right up to the edge. As if it's keeping distance.",
            "A fire pit, cold. Someone camps here. Keeps it small. Careful.",
            "The stonework is finer than anything in Ironhaven. Older. Different hands, different tools.",
        ],
        "npc_moments": [
            {"npc": "shade", "line": "Shade is here somewhere. You can tell without seeing them. The quality of the silence is different when someone trained is in it."},
            {"npc": "shade", "line": "You glimpse Shade at the far end of the plaza — they're looking at one of the carved walls. Not reading it. Remembering something."},
        ],
        "discoveries": [
            {"text": "A sealed chamber you hadn't noticed before. The seal is recent — the dust is disturbed and something was taken, or left.", "item": None},
            {"text": "Scratched into the base of a pillar: a list of names, twelve in total, with dates. The last entry is eight years ago. None of the names match anyone in Ironhaven. Yet.", "item": None},
            {"text": "Hidden in a crack in the wall: a small glass vial, sealed, containing a dark liquid. Not ore. Something refined from it.", "item": None},
        ],
        "quotes": [
            ("\"This place had a different name, before. People came here to meet in secret.\"", "Shade"),
            ("\"Old stone keeps old things. You have to know how to ask.\"", "The Watcher"),
            ("\"Eight years ago this was the safest place in Ironhaven. Funny how things change.\"", "Shade"),
        ],
        "lore": [
            "📖 The Ancient Ruins are Null Security — full PvP, Ruins Sentinels and Cursed Knights spawn.",
            "📖 Shade can be found here. Their questline is central to Arc 1's resolution.",
            "📖 The Ruins connect to Shadow Den — requires level 16+ to enter.",
            "📖 Enemy level range: 20-30. Bring potions.",
        ],
    },

    "fishermans_cove": {
        "atmosphere": [
            "The sea is the only thing Mercer hasn't found a way to tax. Yet.",
            "Old boats, older debts. The fishermen own neither.",
            "The smell here is pure fish. The real working waterfront.",
            "Three fishermen mend nets without speaking. The work knows its own rhythm.",
            "A child runs along the dock edge. Their parent doesn't call them back. They grew up here. They know the edge.",
            "The water near the cave entrance has a different color. Faint. You'd miss it if you weren't looking.",
            "Old Grull's shack has smoke coming from the chimney. He's up early or up late.",
            "The cove is independent from the official docks. Deliberately. The fishermen here never registered.",
            "Seagulls fight over something on the beach. Whatever it is, they've already torn it apart.",
            "The tide marks on the cave cliffs show the water reaches higher than it used to. Something upstream has changed.",
        ],
        "npc_moments": [
            {"npc": "old_grull", "line": "Old Grull walks the dock edge checking his lines without looking at them. Decades of muscle memory. He glances at you. 'You fish?' That's the whole sentence."},
            {"npc": "old_grull", "line": "Grull is sitting at the end of the dock looking at the water near the caves. He doesn't say anything. But he's watching something specific."},
        ],
        "discoveries": [
            {"text": "Caught in the net of one of the abandoned boats: a piece of cargo crate stamped with a mark you've seen on the Ashwood operation manifests.", "item": None},
            {"text": "The water near the sea cave entrance has a dark discoloration today. A thin film on the surface. Old Grull sees you looking at it. 'Three months,' he says, then goes back inside.", "item": None},
        ],
        "quotes": [
            ("\"Sea doesn't care about Mercer. That's why I live here.\"", "Old Grull"),
            ("\"The fish near the caves taste different now. Nobody buys them anymore.\"", "Fisherman"),
            ("\"Independent? Sure. Independent until the collectors come. Then we're same as everyone.\"", "Fisherman, older"),
        ],
        "lore": [
            "📖 Fisherman's Cove is Low Security — Bandit Warriors spawn, PvP enabled.",
            "📖 Fishing is available here and in the Sea Caves. Requires a rod and bait.",
            "📖 Old Grull's relationship unlocks fishing spot locations and rare catch chances.",
            "📖 The Sea Caves are accessible from here at low tide.",
        ],
    },

    "sea_caves": {
        "atmosphere": [
            "The tide is low. The cave breathes cold air.",
            "Sound travels strangely in here. Your footsteps come back wrong.",
            "The walls are wet. Not from the tide — from something seeping through the rock.",
            "Bioluminescent patches on the cave ceiling. Natural, probably. Probably.",
            "The dark here is complete when you're away from the entrance. Your eyes don't adjust enough.",
            "Water sounds from deeper in. Not waves. Something else moving.",
            "The black ore veins in the cave walls are larger than the ones in the forest. Older. Or more concentrated.",
            "The smell changes the deeper you go. Less salt. More metal.",
            "Something large moves in the water channel to your right. You don't see it. You feel the displacement.",
        ],
        "npc_moments": [],
        "discoveries": [
            {"text": "A rope line anchored to the cave wall, leading down into the underwater channel. Recently placed. Someone dives here.", "item": None},
            {"text": "A carved alcove in the cave wall, deliberately shaped. Whatever was stored here is gone. The marks are old but the space was used recently.", "item": None},
            {"text": "A cluster of black ore crystals growing from the cave floor in a formation that looks, in the wrong light, deliberate.", "item": "black_ore_fragment"},
        ],
        "quotes": [
            ("\"The caves go further than anyone's mapped. I've checked.\"", "Unknown"),
            ("\"Fishmen can go where you can't in there. Keep that in mind.\"", "Old Grull"),
            ("\"The serpent doesn't come to the surface. You have to go down to it.\"", "Sailor, nervous"),
        ],
        "lore": [
            "📖 Sea Caves are Null Security — Sea Serpent and Corrupted Wolves spawn here.",
            "📖 Fishman players have a swim advantage in flooded sections — special passages available.",
            "📖 Enemy level range: 22-32. High risk, high reward.",
            "📖 Only accessible from Fisherman's Cove.",
        ],
    },

    "smugglers_trail": {
        "atmosphere": [
            "The path isn't on any official map. Someone maintains it anyway.",
            "Fresh wheel ruts. Heavy cargo, recently. Going away from the port.",
            "Mercer's private mercenaries use this route. Not the Council's men. His.",
            "Move quietly. The trail rewards the quiet.",
            "The brush on either side has been cut back just enough. Someone knows what they need.",
            "A marker on a tree that you almost walk past. Not a trail marker. A signal of some kind.",
            "The trail runs between two worlds: the controlled city and the lawless forest. Neither claims it.",
            "At the midpoint, you can see both Ironhaven's towers and the Ashwood's canopy. Two different problems.",
        ],
        "npc_moments": [],
        "discoveries": [
            {"text": "A cached supply drop behind a marked boulder. Rations, rope, a sealed jar of something. Left for someone. Not you. But here.", "item": None},
            {"text": "The ruts here are from multiple trips. Consistent spacing, consistent depth. This isn't occasional smuggling. This is a supply line.", "item": None},
        ],
        "quotes": [
            ("\"The trail exists because official routes ask questions.\"", "Unknown"),
            ("\"Watch the ruts. They tell you more than the cargo manifests.\"", "Maren"),
            ("\"Mercer's men move ore this way because they don't want the dockworkers to see how much.\"", "Resistance contact, unnamed"),
        ],
        "lore": [
            "📖 Smuggler's Trail is Low Security — Mercer Mercenaries and Bandit Archers spawn here.",
            "📖 PvP is enabled. High chance of player encounters from both factions.",
            "📖 Connects Port District to Ashwood Forest without going through the city.",
            "📖 Enemy level range: 10-18.",
        ],
    },

    "residential_ward": {
        "atmosphere": [
            "Every door has a debt notice on it. Some have two.",
            "A child watches you from a window upstairs. They don't wave.",
            "The ward is quiet in the way that means people have learned to be quiet.",
            "Washing lines between buildings. Life is still happening here, despite everything.",
            "Someone is cooking. The smell reaches the street. Basic ingredients, stretched.",
            "Three neighbours talk in lowered voices at a corner. They stop when they notice you. Start again when you're past.",
            "The streets are clean. People here take care of what they have, because they know what losing it feels like.",
            "A dog sleeps in a doorway. The owner is at work. They've been at work since before sunrise.",
            "A child's drawing chalked on the pavement: a fish, a boat, an island. Something they've been told about but never seen.",
        ],
        "npc_moments": [],
        "discoveries": [
            {"text": "A debt notice on a door, torn down and left in the gutter. Someone got angry. Someone else probably put a new one up.", "item": None},
            {"text": "In the gap between two houses, a small vegetable garden. Unofficial. Not registered. Completely illegal under the new agricultural licensing. Nobody has reported it.", "item": None},
        ],
        "quotes": [
            ("\"Keep your head down. Pay on time. That's the life.\"", "Resident, unnamed"),
            ("\"The ward used to have a market too. Sunday mornings. Not anymore.\"", "Older resident"),
            ("\"My kids don't ask why things are the way they are. I taught them not to.\"", "Parent, unnamed"),
        ],
        "lore": [
            "📖 Residential Ward is High Security — no enemies, no PvP.",
            "📖 Connected only to Town Square.",
            "📖 Rest at the inn in Town Square to restore full HP for 20 Ƶ.",
        ],
    },

    "shadow_den": {
        "atmosphere": [
            "Armed. Professional. Expensive. Mercer doesn't hire cheap.",
            "This is where people end up when they stop being useful. Or start being too useful.",
            "Nobody comes here by accident. The mercenaries know that, and they act accordingly.",
            "The compound is built into the ruins. They didn't restore anything. Just occupied it.",
            "Two guards at every entrance. One watching, one watching the other watch.",
            "The equipment here is better than Council standard. Custom. Someone is paying above rate.",
            "Commander Voss runs this place like a military operation. Because it is one.",
            "The air here is colder than the ruins outside. The compound is underground in parts.",
        ],
        "npc_moments": [],
        "discoveries": [
            {"text": "A shipping manifest tacked to the compound wall. The ore destination is listed. It's not Ironhaven. It's not any city you know.", "item": None},
            {"text": "A crate marked with the Sovereignty symbol — you've seen it once before, in a document you weren't supposed to read.", "item": None},
        ],
        "quotes": [
            ("\"Professional. That's the word. We're professional.\"", "Mercenary, Shadow Den"),
            ("\"Commander Voss doesn't explain orders. You follow them or you leave.\"", "Guard"),
            ("\"The ore goes somewhere. I don't ask where. That's the job.\"", "Elite mercenary"),
        ],
        "lore": [
            "📖 Shadow Den is Bumpyard — the most dangerous zone on Island 1.",
            "📖 Requires level 16+ to enter from Ancient Ruins.",
            "📖 Shadow Den Guards and Elite Mercenaries spawn here. Bring a full deck and max potions.",
            "📖 Enemy level range: 30-40.",
        ],
    },
}


def get_walk_data(zone_id: str) -> dict:
    """Get walk data for a zone — merges base WALK_DATA with WALK_EXTRAS + quirky events."""
    base = WALK_DATA.get(zone_id, {
        "atmosphere": ["You move through the area."],
        "npc_moments": [],
        "discoveries": [],
        "quotes": [],
        "lore": [],
    })
    extras  = WALK_EXTRAS.get(zone_id, {})
    quirky  = QUIRKY_EVENTS.get(zone_id, [])
    zet_rng = ZET_DROP_RANGES.get(zone_id, (1, 10))
    extended  = WALK_EXTENDED.get(zone_id, [])
    extended2 = WALK_EXTENDED_2.get(zone_id, [])
    merged    = {**base, **extras}
    merged["atmosphere"] = (
        merged.get("atmosphere", []) + quirky + extended + extended2
    )
    merged["zet_drop_range"] = zet_rng
    return merged


# =============================================================================
# EXPANDED WALK EVENT POOLS
# Added to each zone's WALK_DATA dict via WALK_EXTRAS below.
# Merged at runtime in get_walk_data().
# =============================================================================

WALK_EXTRAS: dict[str, dict] = {

    "town_square": {
        "item_finds": [
            {"item_id": "copper_coin",      "weight": 50, "text": "A coin on the cobblestones. Someone dropped it in a hurry."},
            {"item_id": "council_pamphlet", "weight": 30, "text": "A Council notice on the ground, half-trampled. Approved price schedules for next month."},
            {"item_id": "guild_notice",     "weight": 20, "text": "A torn contract notice from the Guild board. Someone ripped it down."},
        ],
        "overheard": [
            "Two merchants in lowered voices: *\"The portrait went up three years ago. Nobody asked us. Nobody asks us anything anymore.\"*",
            "A woman to her companion, passing quickly: *\"Tomás's boy hasn't written. Three months. He won't say anything but I can see it.\"*",
            "A soldier, off duty, to another: *\"Night runs to the forest again. Third time this week. Not our unit.\"*",
            "An old man feeding pigeons, to no one: *\"Used to be a market here on Sundays. Real one. Before.\"*",
            "Two dock workers passing through: *\"The manifests don't match again. They never match. We just sign anyway.\"*",
        ],
        "rumours": [
            "Someone mentions that workers from the forest operation have been turning up at Hana's clinic with injuries they won't explain.",
            "A guild member says three contracts went unaccepted this week — the ones that involved the eastern forest road.",
            "A child tells another that their uncle stopped writing letters. The second child says their father too. They go back to playing.",
            "A merchant says Mercer's tax rate is going up next quarter. A bystander says it's always going up next quarter.",
        ],
        "lore_fragments": [
            "📖 The Adventurer's Guild processes contracts but has no authority over Council operations. Anything happening in the forest is outside their jurisdiction.",
            "📖 Ironhaven's debt system: when a loan is restructured three times, a labour addendum can be attached without the original borrower's signature. This is technically legal.",
            "📖 Mercer has been in Ironhaven for eleven years. The portrait appeared in year three. Nobody voted on it.",
        ],
    },

    "market_quarter": {
        "item_finds": [
            {"item_id": "bruised_herb",   "weight": 40, "text": "A bunch of herbs dropped near Hana's doorstep. Still usable."},
            {"item_id": "bread_roll",     "weight": 35, "text": "A wrapped roll on the counter of Tomás's shop — he waves it away when you look at it. 'Take it.'"},
            {"item_id": "playing_card",   "weight": 25, "text": "A card face-down near the Gilded Draw entrance. Not from any deck you recognise."},
        ],
        "overheard": [
            "Tomás to a customer, voice slightly too steady: *\"He's working out east. Good money. Good work. He says it's fine.\"*",
            "Hana to herself, checking a ledger: *\"Three more this week. Same presentation. Same denial.\"*",
            "A customer leaving Tomás's shop: *\"He made too many pastries again. He always makes too many when something's wrong.\"*",
            "Two women at the market stalls: *\"Vex at the card shop knows more than he says. Always has. The cards are just the front.\"*",
            "A fisherman buying supplies: *\"The catch near the caves tastes wrong now. We don't sell it. We don't talk about why.\"*",
        ],
        "rumours": [
            "Someone says the black ore that occasionally shows up in the market is immediately bought by a specific agent — same person every time, never identified themselves.",
            "A regular customer mentions Hana has been working late most nights. She's never worked late before.",
            "Word is that Tomás closed his shop for an hour last week. Middle of a business day. Nobody saw where he went.",
        ],
        "lore_fragments": [
            "📖 Hana's clinic operates under a medical confidentiality oath. She cannot report what patients tell her without their consent.",
            "📖 Vex opened the Gilded Draw eight months ago. Before that, the space was empty for three years. Nobody remembers who owned it.",
            "📖 Tomás has operated his shop for thirty years. He extended a business loan eighteen months ago. The terms have never been disclosed.",
        ],
    },

    "port_district": {
        "item_finds": [
            {"item_id": "rope_scrap",    "weight": 40, "text": "Good rope, cut end still clean. Someone left it in a hurry."},
            {"item_id": "ship_token",    "weight": 35, "text": "A brass dock entry token. Unmarked. Not from any registered vessel."},
            {"item_id": "damp_letter",   "weight": 25, "text": "A letter on the dock road, water-damaged. Only two words are legible: 'don't come'."},
        ],
        "overheard": [
            "A dockworker to another, quietly: *\"Third time this month the manifest says one thing and the hold says another. I sign it. I don't ask.\"*",
            "Maren, on her way somewhere, to herself: *\"Forty-seven. Forty-seven shipments.\"* She doesn't elaborate.",
            "A sailor drinking outside the tavern: *\"You know what the soldiers complain about when they're drunk? The ore schedule. Always behind. Always pushing.\"*",
            "Bora to a customer: *\"He had six drinks and talked about extraction quotas for twenty minutes. I write everything down.\"*",
            "Two port officials: *\"Night boats again. Third bell. Same crew, different boat. I stopped logging it.\"*",
        ],
        "rumours": [
            "The sailors talk about a ship that comes in every two weeks without a registered port of origin. It leaves lighter than it arrives.",
            "Someone at the tavern says Maren has been copying manifests by hand. Every single one that passes her desk.",
            "Word from the docks: the night crew isn't Council soldiers. Different badges. Nobody's seen that insignia before.",
        ],
        "lore_fragments": [
            "📖 Port manifests are public record — except the ones processed through Mercer's private dock office, which uses a separate logging system.",
            "📖 The Sovereignty seal — a closed eye over scales — has appeared on six of the forty-seven night shipment manifests. All from the earliest runs.",
            "📖 Maren held a master maritime license before her ship was seized. Under Ironhaven law, a seized vessel's logs are sealed for seven years.",
        ],
    },

    "harbour_docks": {
        "item_finds": [
            {"item_id": "cargo_tag",     "weight": 45, "text": "A crate tag on the dock road. The destination code doesn't match any registered port."},
            {"item_id": "iron_bolt",     "weight": 35, "text": "A heavy iron bolt, freshly machined. Not for wood — too thick. For something industrial."},
            {"item_id": "dock_receipt",  "weight": 20, "text": "A dock receipt, partially burned. The cargo listed is 'raw industrial material.' The weight is circled twice."},
        ],
        "overheard": [
            "A night shift worker, end of shift: *\"Heavy night. Six crates. They don't let us see inside but the weight's always the same.\"*",
            "Two workers: *\"You count them?\"* *\"No. You?\"* *\"No.\"* Silence.",
            "A dock official, alone on a smoke break: *\"I've been here twelve years. I've never seen a cargo manifest with that stamp before last year.\"*",
        ],
        "rumours": [
            "The ore from the forest operation doesn't come through the main docks. Workers say it goes through the Smuggler's Trail to a separate loading point at the south cove.",
            "Someone saw a Sovereignty-stamped crate two weeks ago. They reported it. The next day the report was gone and so was the crate.",
        ],
        "lore_fragments": [
            "📖 Harbour Docks operates on a shift system. The night shift logs are filed separately and processed through Mercer's private office, not the public record.",
            "📖 Black ore is significantly heavier than standard iron ore. A trained docker can tell the difference by how a crate settles.",
        ],
    },

    "farmlands": {
        "item_finds": [
            {"item_id": "wild_herbs",    "weight": 45, "text": "Herbs growing at the field edge — medicinal, if you know what to do with them."},
            {"item_id": "grain_sack",    "weight": 35, "text": "A small sack of grain, left by the road. Someone's portion, set aside. You take it."},
            {"item_id": "fence_nail",    "weight": 20, "text": "Iron nails, scattered near a broken fence. Someone's been busy repairing things that keep breaking."},
        ],
        "overheard": [
            "A farmer to their child, voice flat: *\"Forty percent. Before we eat. Every month.\"*",
            "Two farmworkers: *\"Cart tracks again last night. Heavy ones. Going toward the forest.\"* *\"I didn't hear anything.\"* *\"No. Neither did I.\"*",
            "An older farmer to a younger one: *\"Before Mercer, there was a Sunday market. Proper one. We kept what we grew.\"*",
            "A rent collector's horse passes. Every farmer stops working and doesn't look up until it's gone.",
        ],
        "rumours": [
            "Workers from the forest operation have been seen on the farm roads after dark — heading back toward town. They don't stop to talk.",
            "A farmer says the eastern fields near the forest have been acting strange — soil's discoloured near the treeline. Has been for months.",
        ],
        "lore_fragments": [
            "📖 Under current Council law, agricultural yields are taxed at the point of harvest, not sale. Mercer's office sets the yield assessment — always higher than actual.",
            "📖 The Farmlands connect directly to Ashwood Forest. The official boundary is marked. The unofficial activity ignores it.",
        ],
    },

    "ashwood_forest": {
        "item_finds": [
            {"item_id": "wolfsbane",          "weight": 35, "text": "Wolfsbane growing in the root shadow of a large oak. Hana would want this."},
            {"item_id": "pine_resin",         "weight": 30, "text": "Pine resin, freshly tapped. Someone's been through here collecting."},
            {"item_id": "black_ore_fragment", "weight": 25, "text": "A black ore fragment at the base of the rock face. Warm to the touch. Unregistered vein."},
            {"item_id": "snapped_torch",      "weight": 10, "text": "A torch handle, snapped, burn end still warm. Someone was here recently and left fast."},
        ],
        "overheard": [
            "A distant voice, source unclear: *\"...three more wagons tonight. Move.\"* Then nothing.",
            "Wind, then something that might be cart wheels on stone. Then silence again.",
            "A bird alarm call that goes on longer than it should, then stops all at once.",
        ],
        "rumours": [
            "Workers from the forest operation have been seen with dark staining on their hands — up to the wrists. Not standard mining residue.",
            "Someone left markers on the trees leading deeper into the forest. Not trail markers — different shape, different knot. Recent.",
            "The cart tracks here go in both directions. The laden tracks going out are significantly deeper than the empty ones coming in.",
        ],
        "lore_fragments": [
            "📖 The Ashwood Forest was declared protected by the old Council twelve years ago. The protection was quietly revoked in Mercer's first year.",
            "📖 Black ore has been found in three locations: the forest operation, the Cursed Grove, and the Sea Caves. All three are unregistered extraction sites.",
            "📖 Workers exposed to black ore for extended periods develop progressive mineral deposits in the skin. Nurse Hana has documented this in twelve patients.",
        ],
    },

    "cursed_grove": {
        "item_finds": [
            {"item_id": "black_ore_fragment", "weight": 50, "text": "A black ore crystal lying exposed on the surface. It's warm — much warmer than the air around it."},
            {"item_id": "corrupted_bark",     "weight": 30, "text": "Bark from one of the blackened trees. The discolouration goes all the way through."},
            {"item_id": "cold_stone",         "weight": 20, "text": "A stone from inside the ring at the grove center. You pick it up before you decide if you should."},
        ],
        "overheard": [
            "Nothing. The grove is completely silent. That's the wrong kind of quiet.",
            "A sound like something moving through the undergrowth. You look. Nothing is there.",
            "The trees creak without wind.",
        ],
        "rumours": [
            "Animals avoid the grove center entirely now. Six months ago they just seemed wary. Now there are none at all.",
            "A ranger passing through said the corruption is spreading — the black border on the trees moved another meter outward this month.",
        ],
        "lore_fragments": [
            "📖 The Cursed Grove was normal forest eight months ago. The corruption began at the center ring — a deliberate formation of stones — and spread outward.",
            "📖 The ore in the grove and the ore at the forest operation test as the same compound at different concentrations. The grove is older.",
            "📖 Animals exposed to the grove show the same progressive changes as human workers — skin hardening, behavioral shifts — but faster.",
        ],
    },

    "ancient_ruins": {
        "item_finds": [
            {"item_id": "ancient_coin",     "weight": 40, "text": "A coin pressed flat in the stonework. The markings predate anything in the city's records."},
            {"item_id": "carved_fragment",  "weight": 35, "text": "A piece of carved stone with part of the closed-eye symbol. It matches the full carving on the north wall."},
            {"item_id": "cracked_seal",     "weight": 25, "text": "A wax seal, cracked, with an insignia you've seen on Sovereignty documents. Someone was here."},
        ],
        "overheard": [
            "Nothing. Then — a footstep that isn't yours. Then nothing again.",
            "Shade's voice, from somewhere in the ruins: *\"Whoever built this knew it would still be standing. They planned for a long time.\"* You can't see him.",
            "Wind through the carved archways makes a sound almost like words.",
        ],
        "rumours": [
            "The symbol on the ruins wall — closed eye over scales — appears on the back of six specific cards in Vex's shop. He priced them higher than anything else.",
            "Someone has been making rubbings of the wall carvings at night. The fresh chalk marks are visible in the morning.",
            "Shade has been seen here consistently for eight months. He's not excavating. He's waiting for something.",
        ],
        "lore_fragments": [
            "📖 The ruins predate Ironhaven by at least three hundred years. The language on the walls has never been successfully translated.",
            "📖 The closed-eye-over-scales symbol appears in the ruins, on Sovereignty documents, and on certain pre-Ironhaven artifacts. It predates the Sovereignty.",
            "📖 The carvings on the north wall are navigation instructions — not maps, but instructions. The ore deposits form the reference points.",
        ],
    },

    "fishermans_cove": {
        "item_finds": [
            {"item_id": "dried_kelp",  "weight": 40, "text": "Dried kelp, high quality. Grull's probably, left out by accident."},
            {"item_id": "fish_hook",   "weight": 35, "text": "A fishing hook, hand-forged. Better than anything sold in the Market Quarter."},
            {"item_id": "sea_glass",   "weight": 25, "text": "A piece of sea glass, unusually dark. Not the usual colour. From deeper water, maybe."},
        ],
        "overheard": [
            "Old Grull, looking at the water near the caves: *\"Three months.\"* That's all he says.",
            "A fisherman to his partner: *\"Don't fish the eastern channel anymore. I don't care about the catch.\"*",
            "Two fishermen mending nets: *\"You see the colour of the water near the caves?\"* *\"I stopped looking.\"*",
        ],
        "rumours": [
            "The fish near the cave entrance have been tasting different for three months. The fishermen stopped selling them. They don't explain why to anyone who asks.",
            "Old Grull has a boat shed he keeps empty. Has for three years. He's been quietly stocking it — food, water, blankets.",
        ],
        "lore_fragments": [
            "📖 Fisherman's Cove is unregistered with the official dock authority. The fishermen never registered. Mercer's office has attempted to license them twice. They've refused both times.",
            "📖 The water discolouration near the Sea Caves started three months ago. It correlates with increased activity at the forest operation.",
        ],
    },

    "sea_caves": {
        "item_finds": [
            {"item_id": "black_ore_fragment", "weight": 40, "text": "A cluster of ore crystals growing from the cave floor. Formation looks almost deliberate."},
            {"item_id": "cave_crystal",       "weight": 35, "text": "A clear crystal from the cave wall, the kind that forms over decades. This one has something dark at its center."},
            {"item_id": "salt_rock",          "weight": 25, "text": "Salt rock, naturally formed. The mineral content smells wrong."},
        ],
        "overheard": [
            "Water sounds from deeper in the cave. Not waves. Something moving with purpose.",
            "Dripping. Then a sound like breathing that's too slow to be human.",
            "Your own footsteps echo back wrong — a half-second delayed, from a direction that doesn't make sense.",
        ],
        "rumours": [
            "A diver who went into the cave's flooded passages says the ore veins go much deeper than the surface formations suggest. He didn't go back.",
            "The bioluminescent patches on the ceiling are growing. They weren't there last season.",
        ],
        "lore_fragments": [
            "📖 The Sea Caves connect to an underwater channel that hasn't been fully mapped. Fishman players can access passages that are inaccessible to other races.",
            "📖 The black ore in the caves is the same compound as the forest operation and the Cursed Grove, but older. Possibly the original source.",
        ],
    },

    "smugglers_trail": {
        "item_finds": [
            {"item_id": "dropped_manifest",  "weight": 40, "text": "A cargo manifest, dropped in the brush. The destination column has been crossed out and rewritten."},
            {"item_id": "oil_cloth",         "weight": 35, "text": "Oilcloth wrapping, the kind used to waterproof cargo. Fresh. The ore smell is unmistakable."},
            {"item_id": "iron_ring",         "weight": 25, "text": "A ring used to lash cargo to carts. Still has rope fibres in the groove — recent use."},
        ],
        "overheard": [
            "Cart wheels on stone, ahead. You stop. They stop. After a long moment, they continue.",
            "Two voices ahead, very low. You can't make out words. They stop talking when you get close.",
            "The sound of something being dragged. Then silence. Then nothing where the sound was.",
        ],
        "rumours": [
            "Mercer's private mercenaries use this trail for the night runs. They're not Council soldiers — different pay, different orders, different loyalty.",
            "The trail has been used at least forty times in the last eight months based on the rut depth. That's more than occasional smuggling. That's a supply line.",
        ],
        "lore_fragments": [
            "📖 The Smuggler's Trail appears on no official map. Someone maintains it without wanting to be known for it.",
            "📖 The ore shipments travel: forest operation → Smuggler's Trail → Harbour Docks night loading → unregistered boat → unknown destination.",
        ],
    },

    "residential_ward": {
        "item_finds": [
            {"item_id": "debt_notice",   "weight": 40, "text": "A debt notice, torn down from a door and left in the gutter. Someone got angry. A new one will be up tomorrow."},
            {"item_id": "child_drawing", "weight": 35, "text": "A child's drawing on paper — a fish, a boat, an island. Something they were told about but have never seen."},
            {"item_id": "copper_coin",   "weight": 25, "text": "A coin in the gutter. Small. Someone needed it and dropped it anyway."},
        ],
        "overheard": [
            "A parent to a child, very quiet: *\"You don't ask about the forest. You understand? You don't ask.\"*",
            "Two neighbours at a door, voice low: *\"His letters stopped. Two months.\"* *\"I know. Mine too.\"*",
            "An older woman, sitting outside: *\"The ward used to have a market on Sunday mornings. We knew everyone. Now we know not to look.\"*",
            "A child to another: *\"My dad works in the forest. He said he'd be back in three months.\"* Pause. *\"When was that?\"* *\"I don't know.\"*",
        ],
        "rumours": [
            "Three families in the ward have members working at the forest operation. None of them have had a letter in over two months.",
            "Bora from the tavern has been quietly leaving food at certain doors in the ward. She doesn't knock. She doesn't tell anyone.",
            "Rel's training ground gets late-night visitors from the residential ward. People asking to learn something. Rel doesn't turn anyone away.",
        ],
        "lore_fragments": [
            "📖 The residential ward houses approximately three hundred families. Forty percent of household income goes to debt servicing on Mercer-structured loans.",
            "📖 Several ward residents have family members at the forest operation. Most stopped receiving letters two to three months ago.",
        ],
    },

    "shadow_den": {
        "item_finds": [
            {"item_id": "guard_token",        "weight": 40, "text": "A mercenary access token, dropped near the entrance. Still valid."},
            {"item_id": "mercenary_badge",    "weight": 35, "text": "A Shadow Den unit badge. The insignia is Mercer's private company, not the Council's."},
            {"item_id": "sovereignty_seal",   "weight": 25, "text": "A wax seal with the closed-eye symbol, broken. From a document that's already been opened."},
        ],
        "overheard": [
            "Two guards: *\"Third shipment this week. Where does it go?\"* *\"You're not paid to ask that.\"*",
            "A mercenary, quietly: *\"I've been here four months. I still don't know what's in the crates.\"*",
            "Commander Voss, somewhere in the compound: *\"On schedule. Tell them on schedule.\"*",
        ],
        "rumours": [
            "The Shadow Den mercenaries are paid three times the standard Council rate. Nobody asks where the money comes from.",
            "Commander Voss reports directly to someone in Ironhaven who isn't Mercer. Nobody knows who.",
            "The crates from the forest operation that pass through Shadow Den weigh more going out than coming in. Something is being added.",
        ],
        "lore_fragments": [
            "📖 Shadow Den was established eight months ago in the Ancient Ruins. The mercenaries displaced a small resistance cell that had been using the site.",
            "📖 Commander Voss's unit answers to a private contract, not the Council. The contract holder is listed only as 'SVT Holdings' — an offshore entity.",
            "📖 The Sovereignty's decommission timeline for Ironhaven is eighteen months from the date of the third letter in Mercer's private archive.",
        ],
    },
}


# =============================================================================
# QUIRKY EVENTS — zone-specific funny/dry walk moments
# Mixed into quiet steps for variety. Tone: wry, dark, Ironhaven-specific.
# =============================================================================

QUIRKY_EVENTS: dict[str, list[str]] = {
    "town_square": [
        "A man is passionately arguing with a pigeon about property rights. The pigeon is winning.",
        "A Council soldier drops his clipboard. Every page is the same form. He picks it up without looking at you.",
        "You find a coin. Then another. Then a third. Then a fourth. You stop finding coins.",
        "A child offers you a pebble. You take it. It is just a pebble. The child looks satisfied.",
        "A seagull steals someone's pastry directly from their hands. Nobody helps. Everyone has seen this before.",
        "A tax collector trips on a cobblestone. Nobody helps him up. He gets up eventually.",
        "A man in a very official-looking coat is writing in a ledger. He looks at you, makes a note, looks away. You were just assessed.",
        "Someone has drawn a small mustache on the bottom corner of Mercer's portrait. It will be painted over by tomorrow. Someone will draw another one.",
        "A merchant loudly declares his prices are 'the fairest in Ironhaven.' They are not the fairest in Ironhaven. He knows this.",
        "You step on a loose cobblestone. It makes an embarrassing sound. Three people look. Two pretend they didn't.",
    ],
    "market_quarter": [
        "Tomás waves at you from his shop window. He was going to say something. He thinks better of it. He waves again.",
        "A customer haggles for eleven minutes over a three-Ƶ price difference. They lose. They always lose.",
        "Someone drops an entire jar of something. Everyone in the market stops. Nobody moves. Then everyone moves at once.",
        "A man is trying to sell 'authentic pre-Mercer artifacts.' They are clearly just rocks. He has sold four today.",
        "Hana's shop window has a sign: 'No, I cannot cure that. No, not that either. Please stop asking about the forest.' It is new.",
        "A cat sits in the exact center of the market road. Three carts have rerouted. The cat is aware of this.",
        "Two merchants compare notes on Mercer's price regulations. One of them is taking notes. It is unclear why. It is very clear why.",
        "Someone is selling 'premium river water' in labeled bottles. It is selling well. This is not encouraging.",
    ],
    "port_district": [
        "A sailor describes the largest fish he has ever caught. It is larger than the one he described yesterday. Tomorrow it will be larger still.",
        "Two dock workers play a game where they guess which crates are labeled correctly. They are very good at this game. Nobody taught it to them.",
        "A man runs past you yelling something about a boat. Several people run after him. The boat is probably fine.",
        "Bora waves from the tavern door. 'You look like you need a drink,' she says. You do not need a drink. She is correct anyway.",
        "A sailor tries to explain something complicated using only his hands. His companion nods continuously. Neither of them are listening.",
        "A gull lands on a Sovereignty-stamped crate and immediately flies away. You understand the feeling.",
        "Someone has labeled a perfectly ordinary barrel 'ABSOLUTELY NOT ORE.' It is almost certainly ore.",
    ],
    "harbour_docks": [
        "A dockworker counts crates for the third time. His count is different each time. He writes down the middle number.",
        "You help someone carry a box. It is much heavier than it looks. You do not ask what is in it. They do not tell you. This is fine.",
        "A man with a clipboard looks at you, looks at his clipboard, looks at you again, makes a note, walks away. You are now in a ledger somewhere.",
        "Two inspectors argue about which of them is supposed to be inspecting this section. Neither of them inspects it.",
        "A crane operator is eating lunch forty feet in the air. He waves at you. You wave back. This is a normal interaction.",
    ],
    "farmlands": [
        "A farmer stares at the horizon for a very long time. You follow their gaze. There is nothing there. You look back. They are still staring.",
        "A goat has escaped its pen. Three children are chasing it. The goat is faster than the children. The goat will always be faster than the children.",
        "A rent collector's horse sneezes on him. He does not react. This is not the first time. It is not the worst thing that has happened today.",
        "Someone has written 'MERCER EATS DIRT' on a fence post in very small letters. Someone else has tried to cross it out. You can still read it.",
        "A scarecrow has been dressed in a tax collector's hat. The farmer who did this is pretending to have no idea who did this.",
        "A child is very carefully counting seeds. They lose count at thirty-seven every time. They start again. They will figure it out.",
    ],
    "ashwood_forest": [
        "A bird alarm call rings out. Something startled it. You hear nothing else. This is not as reassuring as it should be.",
        "A squirrel watches you for a very long time. You watch it back. It leaves first. You feel you have passed some kind of test.",
        "You find a boot. Just one boot. It is in good condition. You leave it. Someone will come back for it. Probably.",
        "The forest is completely silent for exactly three seconds. Then everything starts again. You do not know what to do with that.",
        "Someone has tied a piece of cloth to a branch as a trail marker. Below it, someone else has tied a different cloth. They point in different directions.",
        "You hear cart wheels on stone ahead. You stop. The wheels stop. After a long moment, you continue. The wheels continue. You walk faster.",
    ],
    "residential_ward": [
        "A child has drawn an extremely detailed map of the ward in chalk on the pavement. Several streets are labeled 'HERE BE MERCER.' They are not wrong.",
        "Two neighbors argue loudly about a fence for ten minutes, then share a meal through the same fence immediately after.",
        "A dog is sitting in a doorway looking profoundly disappointed in everything. You know the feeling.",
        "Someone's laundry has fallen off the line. A stranger picks it up, folds it neatly, puts it on the doorstep, and walks away. Nobody acknowledges this.",
        "A grandmother yells at a pigeon for twelve uninterrupted seconds. The pigeon does not move. She runs out of things to say. The pigeon wins.",
        "Three different debt notices are pinned to one door. Someone has organized them by date. Someone is trying to stay on top of things.",
    ],
    "fishermans_cove": [
        "Old Grull looks at the sea for a long time. 'Something's different,' he says. He walks back inside. He does not elaborate.",
        "A crab has claimed a small patch of dock as its own. Two fishermen are routing around it. It has been there for a week. Nobody challenges the crab.",
        "Someone's fishing line comes back with a boot on it. They examine it. They throw it back. They seem unsurprised.",
        "A child is trying to fish with a stick and no hook. They are very focused. Several adult fishermen are watching with genuine respect.",
        "A seagull and a fisherman have been in a standoff over a fish for four minutes. You arrive at minute five. You leave before it's resolved.",
    ],
    "ancient_ruins": [
        "A stone shifts under your foot. Below it is another stone. Below that is another stone. It is stones all the way down.",
        "You hear footsteps that are not yours. When you stop, they stop. When you walk, they walk. You choose not to run. You choose not to stop.",
        "Shade is sitting on a ruined wall reading something. He closes it when he notices you. 'Old maps,' he says. You did not ask.",
        "Someone has left a fresh candle in the ruins. It was lit recently. It is not lit now. This happened between now and a few hours ago.",
        "You find a coin older than Ironhaven. You put it in your pocket. Something about that feels important. You can't say why.",
    ],
    "smugglers_trail": [
        "You hear someone whistling ahead. When you round the bend, nobody is there. The whistling was recent. The path is empty.",
        "Fresh wheel ruts. Loaded cart, going east. They're not on any map. They don't need to be.",
        "A marker on a tree. Not a trail marker — wrong shape, wrong knot. Someone knows this path who doesn't want it on a map.",
        "You hear two men talking ahead. You can't make out the words. They stop talking when you get close. You walk past. Nobody makes eye contact.",
    ],
    "cursed_grove": [
        "A bird lands on a branch nearby. It stares at you. It does not blink. It has not blinked in some time. You keep walking.",
        "The air smells like iron. Not blood — just metal. You have not walked past anything metal. The smell is coming from the ground.",
        "A small animal runs across your path. You cannot identify what kind. It is moving slightly wrong. You keep walking.",
        "The silence here is not the absence of sound. It is the presence of something that has eaten all the sound. You find this distinction important.",
    ],
    "sea_caves": [
        "The cave drips in a rhythm. Steady. Too steady. Water does not naturally drip this steadily. You keep walking.",
        "Your torch flickers. There is no wind. You check behind you. Nothing. You look forward. The torch steadies. You keep going.",
        "Something large moves in the water channel to your right. You do not look directly at it. This is a decision you are comfortable with.",
        "The bioluminescent patches on the ceiling spell nothing. You check twice. They spell nothing. You feel relieved and then immediately suspicious of the relief.",
    ],
    "shadow_den": [
        "Two mercenaries are playing cards. One of them is cheating obviously. The other knows. They are seeing how long this goes before someone says something.",
        "A guard nods at you. You nod back. You are both pretending this is a normal interaction. It is not a normal interaction. It goes fine.",
        "Someone has written 'PAY IS LATE AGAIN' inside a supply crate in very small letters. You close the crate.",
        "Commander Voss walks past without looking at you. His footsteps are exactly the same every time. You have timed them. This is not reassuring.",
    ],
}

# ---------------------------------------------------------------------------
# ZET DROP RANGES per zone (min, max) — chance is handled in walk.py
# ---------------------------------------------------------------------------

ZET_DROP_RANGES: dict[str, tuple[int, int]] = {
    "town_square":     (2, 12),
    "market_quarter":  (3, 15),
    "residential_ward":(1, 8),
    "port_district":   (5, 20),
    "harbour_docks":   (5, 25),
    "farmlands":       (3, 15),
    "fishermans_cove": (5, 20),
    "ashwood_forest":  (8, 30),
    "smugglers_trail": (10, 40),
    "cursed_grove":    (15, 50),
    "ancient_ruins":   (15, 45),
    "sea_caves":       (20, 60),
    "shadow_den":      (30, 80),
}


# =============================================================================
# WALK_EXTENDED — Massive atmosphere expansion
# Adds 30-50 new lines per zone across all 10 content types.
# Blended into atmosphere pool via get_walk_data().
# =============================================================================

WALK_EXTENDED: dict[str, list[str]] = {

    "town_square": [
        # Sensory
        "The square smells of bread in the morning and something chemical by evening. Nobody mentions this.",
        "Cobblestones slick from last night's rain. The gutters run with something that used to be someone's dinner.",
        "The afternoon light hits the square at a low angle and everything looks better than it is for about twenty minutes.",
        "A bell somewhere counts the hour. You count along. It rings one more time than it should. You check. It does not do it again.",
        "The fountain has been turned off for maintenance for six weeks. Maintenance has not started.",
        "Cold today. The kind of cold that makes people walk faster and look at the ground.",
        "Wind from the port. Salt, rope, and something industrial that has been here long enough to become familiar.",
        # Slice of life
        "A man is reading a notice on the board. He reads it again. He reads it a third time. He walks away without copying it down. He will regret this.",
        "Two strangers reach for the same dropped coin at the same moment. They both let go. The coin sits there.",
        "A woman is explaining something very complicated to a very small child using a stick and some dirt. The child nods seriously. They both seem satisfied.",
        "An old man sits on the fountain edge every day at the same time. Today he is not there. You notice. You don't know why you notice.",
        "A courier arrives, delivers something, and leaves so fast you're not sure you saw it. Whatever was delivered, someone was waiting for it.",
        "Three people are standing in a triangle formation near the guild steps having a conversation where none of them are facing each other directly.",
        "A woman eats her lunch alone on the guild steps and reads a book. She looks like the happiest person in Ironhaven. She probably is.",
        # Quirky/Absurd
        "A man walks past carrying an enormous fish. He is not a fisherman. He has no explanation. He offers none.",
        "A dog has been standing in exactly the same spot for two hours. You've passed it three times. It has not moved. You check. It is fine. You don't understand.",
        "Someone has attached a very small flag to a very small stick and planted it in a crack in the cobblestones. The flag says nothing. It is just a flag.",
        "A child runs past you, stops, looks at you very seriously, says 'you'll figure it out,' and runs away. You have no idea what they meant. It helped somehow.",
        "You find a note on the ground. It reads: 'If you're reading this, put it back.' You put it back.",
        "A man is explaining something at great length to someone who has clearly stopped listening. He has not noticed. He will not notice for some time.",
        # Dark observation
        "Every building on this block has a debt notice. Some have two. One has four. Whoever lives there is very organized about their debt.",
        "The Adventurer's Guild board has a new contract posted. Someone has already torn it down. It is not clear if they accepted it or refused it.",
        "'UNDER NEW MANAGEMENT' signs on three shops in a row. The management changed after debt restructuring. The sign is the only thing that changed.",
        "Mercer's portrait watches from every wall. From this angle, the eyes catch the light wrong. You keep walking.",
        "The Council soldier on the corner has been standing in the same spot for four hours. His expression has not changed once.",
        # Story hints
        "Cart tracks cut deep into the alley mud. Heavy cargo, recent. Heading away from the registered docks.",
        "Someone has chalked the word 'CORMORANT' on the harbour office wall. It's been scrubbed half away. The letters are still visible.",
        "You catch a word — 'extraction' — from a conversation that stops the moment you get close enough to hear more.",
        "A posting on the board is blank except for the Sovereignty seal at the bottom. The message has been removed. The seal was left as a point.",
        # Character quotes
        "'The thing about Mercer,' says someone behind you, 'is that he's never wrong about the math.' You don't turn to see who said it.",
        "'Forty percent,' a farmer mutters, as if saying it again will make it make sense. It doesn't make more sense.",
        "An old woman: 'I've seen three different kinds of terrible run this city. This one is the most polite about it.'",
        "'You want to know what Ironhaven was like before?' A pause. 'Why, do you think it would help?'",
        # Found objects
        "A notice: 'LOST — one grey cat, answers to nothing, please do not approach.' Below it, someone has written: 'found it. it is fine. it does not want to come back.'",
        "On the guild board: 'OUTSTANDING DEBT — SEE COUNCIL HALL.' The name has been torn off. What's left is the seal.",
        "A list posted near the fountain: 'THINGS THE COUNCIL HAS APPROVED THIS WEEK.' Below the heading: nothing. The list has been there for two weeks.",
        "A handwritten sign in a shop window: 'YES WE ACCEPT MERCER NOTES. NO WE DON'T PREFER THEM. YES WE KNOW.'",
        # Animal
        "A cat sits on the guild steps distributing its time equally between judging everyone who enters and judging everyone who leaves.",
        "Two pigeons are having a disagreement near the fountain. It has been going on for a while. Neither is gaining ground.",
        # Memory/History
        "This part of the square used to have market stalls on Sundays. Twelve years ago. The stones are still worn differently where the stalls stood.",
        "The second building on the left used to be a meeting hall. Community meetings, open agenda. It became a tax processing office in year two of Mercer's tenure.",
        # Weather
        "Rain starting. Everyone who was sitting stands up. Everyone who was standing starts walking. The square reorganizes itself in about thirty seconds.",
        "A rare clear evening. Stars visible. A few people stop to look up. Most don't.",
    ],

    "market_quarter": [
        # Sensory
        "The market smells of fresh bread, old wood, herbs from Hana's shop, and underneath it all: ink and ledgers.",
        "Noise here is layered — bartering on top, footsteps below, and underneath both: the scratch of a clerk's pen in every second doorway.",
        "Late afternoon: the shadows from the buildings cross the market road and you walk through alternating bands of warmth and shade.",
        "It rained an hour ago. The market smells clean for another hour before the usual smells come back.",
        "The equipment shop's window display changed this morning. Everything new, same prices. The old display is in the alley. Someone will buy it for less.",
        # Slice of life
        "Two people are arguing about the price of rope. They have been arguing long enough that a small audience has formed. The audience is enjoying this.",
        "A very young apprentice is sweeping the apothecary steps for the third time. The steps are clean. The sweeping is not about the steps.",
        "Tomás is telling someone a story. You catch the end: '— and that's why I don't keep the good cheese on the bottom shelf anymore.' The customer nods seriously.",
        "A woman haggles something from 40 Ƶ down to 38 Ƶ over eleven minutes. The merchant looks tired. She looks satisfied. Forty Ƶ was a fair price.",
        "An elderly merchant closes his stall at exactly the same time every day regardless of whether anything has sold. Routine is its own kind of profit.",
        "Someone's cart wheel has come off right in front of the general store. Five strangers are helping fix it. Nobody asked them to. Tomás brought tea.",
        # Quirky/Absurd
        "A man is attempting to sell 'artisanal Ironhaven air' in sealed jars. He has made one sale. This has encouraged him enormously.",
        "Vex is standing outside the Gilded Draw watching people walk past with the focused attention of someone doing research. You don't know what the research is for.",
        "A merchant has fallen asleep standing up behind his stall. His goods are fine. A passing child adjusts his hat so the sun isn't in his eyes. The child keeps walking.",
        "Someone's pet ferret has escaped inside the general store. Tomás is unconcerned. The ferret has been here before. They have an arrangement.",
        "A man argues that his exotic spice is worth more because it 'came a very long way.' The buyer points out everything came a long way. The argument continues.",
        "A sign in the tailor's window: 'WE DO NOT ACCEPT MERCER BANK NOTES. THIS IS NOT A POLITICAL STATEMENT. WE JUST DON'T HAVE CHANGE.'",
        # Dark
        "Every shopkeeper smiles when a Council official walks past and stops smiling when they're gone. It happens in a wave, shop by shop.",
        "The price list outside the equipment shop has been updated. Everything is more expensive. Nobody looks surprised. The old list is still attached underneath.",
        "Hana's clinic has a queue that wraps around the corner. Most of the people in it are there for something they won't name out loud.",
        # Story hints
        "Vex's window display has changed. One card has been moved to a position where it's visible from the street, facing outward. It's a card you don't recognise.",
        "Tomás closed early yesterday. Nobody knows why. He's open again today. He's smiling more than usual, which is saying something.",
        "A wax seal on a folded note pushed under the door of the equipment shop. The insignia is not the Council's.",
        # Quotes
        "'The thing about Tomás,' someone says, 'is that he remembers everyone. Every single person who's ever bought something. Every one.'",
        "'Hana could leave,' the woman says. 'Good healer, she'd do fine anywhere. She stays. Make of that what you will.'",
        "'Vex has been here eight months,' an old merchant says. 'Before that, the space was empty three years. Before that—' He stops. 'Never mind.'",
        # Found objects
        "A card face-down in the gutter outside the Gilded Draw. You turn it over. The back is marked with a symbol you've seen in the ruins. You put it in your pocket.",
        "Posted on the equipment shop board: 'WILL TRADE: information for information. No names. No Mercer. Third alley left of the guild at third bell.'",
        "A price tag fallen off something expensive. The price is higher than the listed price by forty percent. The difference is listed as 'premium.' Nothing else.",
        # Weather
        "A brief rain. Every stall with an awning fills up. Strangers stand very close together under canvas listening to the rain and not talking.",
        # Animals
        "Three cats sit on three different stall roofs observing the market with administrative seriousness. They appear to be reviewing everything.",
    ],

    "residential_ward": [
        # Sensory
        "Laundry lines cross above the narrow street. Shirts and trousers wave in the wind like the street's own quiet flags.",
        "The ward smells of cooking oil and soap and, underneath, stone that has been cold for a long time.",
        "Children's voices from somewhere you can't see. Laughter, then someone counting. Then silence, then the laughter starts again.",
        "It's quiet here in a way that has a shape. Not absence — presence. People have learned the right kind of quiet.",
        "Every door on this street has a wreath or a symbol or something personal on it. Small declarations. We live here. This is ours.",
        # Slice of life
        "Two neighbors share a wall and a single power line. They've never spoken. They wave at exactly the same time every morning through separate windows.",
        "A child is very carefully filling a crack in the pavement with small stones. She has been doing this for a long time. The crack is nearly full.",
        "An old man sits outside his door every afternoon with a cup of something warm. He nods at everyone who passes. He has nodded at you three times today.",
        "A family is arguing about dinner, audible through the window, with the energy of a disagreement that has a history. It will be resolved. It always is.",
        "A woman hangs laundry on a line while simultaneously managing a conversation with two different neighbors and keeping an eye on a toddler. All three are proceeding fine.",
        "Someone is fixing a broken step. They've fixed it twice this month. It breaks because the foundation is wrong. They know. They fix the step anyway.",
        "Three children are playing a game with rules too complicated to understand from one viewing. One of them is definitely cheating. The other two know.",
        # Absurd/Quirky
        "A cat has been sitting in a window watching you walk past for three laps of the ward. It has not moved. It is tracking your progress.",
        "A man is practicing a speech. You can hear him through his door: '— and FURTHERMORE—' He stops. Starts again. '— and FURTHERMORE—' Not there yet.",
        "You find a shoe. One shoe. Good condition. On a doorstep, left obviously for collection. No one comes to collect it. You check back later. Still there.",
        "Two pigeons are fighting over a piece of bread that neither of them is large enough to carry. This has been going on for some time. Neither will win.",
        "'QUIET HOURS: ALL HOURS,' reads a sign on one door. Below it someone has added: 'this includes you, Garan.' Below that: 'understood. —Garan'",
        # Dark
        "Debt notices on every third door. On one door, four notices, stacked by date. Someone is very organized about this. Someone is trying to stay on top of it.",
        "A child draws on pavement with chalk. Fish. Boats. Islands. Things described to her. She has not seen the sea. The ward is two streets from the port.",
        "Three families on this street have sons working at the forest operation. None of the sons have written in two months. Nobody talks about this. Everyone knows.",
        "A woman puts food outside a door at dusk. Doesn't knock. Walks away. She does this three times a week. Nobody acknowledges it. It's acknowledged anyway.",
        # Story hints
        "Someone has drawn the Sovereignty symbol in chalk on a doorstep and then scuffed it half away. You can still see the closed eye.",
        "A conversation stops as you pass. Resumes when you're beyond earshot. The word you catch before it stops: 'network.'",
        "Rel's training ground is visible from here. Late at night, you've heard, people come and go from the ward to the grounds. Nobody official knows.",
        # Quotes
        "'My kids ask why we don't leave.' An older man, to no one. 'I don't have the answer I want to give them yet.'",
        "'The thing about Mercer,' a woman says to her neighbor, hanging laundry, 'is he came here planning to stay. Most people who ruin things are just passing through.'",
        "'You know what this street had before? A Sunday market. Proper one. We set up at dawn, packed down at dusk, ate together. Before.' She doesn't say before what.",
        # Animals
        "A dog who lives here greets every resident personally and inspects every stranger. It has inspected you twice now. Both times it found you acceptable.",
        "A chicken has escaped from somewhere and is walking the ward with great purpose. Where it is going is unclear. Its confidence is not.",
    ],

    "port_district": [
        # Sensory
        "The port smells of salt, tar, fish, rope, and something chemical that no one names. Layered like geology.",
        "Seagulls everywhere. Their cries are constant enough to become silence after a while. You notice when they stop.",
        "The wood of the dock buildings has been salt-bleached to grey. Everything here is grey or rust. It looks right somehow.",
        "Evening light turns the harbour water orange. For about ten minutes everything looks like a painting. Then it goes back to being a port.",
        "Rope everywhere. Coils, lines, ties. The port is held together by rope. If someone removed all the rope, the port would simply disperse.",
        # Slice of life
        "A sailor arrives from a long voyage and stands on the dock for five minutes just standing on solid ground. You recognize this face. You've made this face.",
        "Two dock workers eat lunch on a crate in companionable silence. They have been doing this for fifteen years. They have nothing left to say. They sit anyway.",
        "A harbour official is on his fourth attempt to explain something to a ship captain who speaks a different language. He is now using hand gestures. It is not helping.",
        "Someone is repairing a boat by themselves. They've been doing it for weeks. It is a one-person job being done by one person and it is taking the correct amount of time.",
        "A very old sailor is teaching a very young one how to tie a knot. The old sailor ties it once. The young one tries seventeen times. The old sailor ties it again.",
        # Absurd
        "A man runs past you carrying two chickens and looking behind him. Nobody is chasing him. The chickens seem resigned to this.",
        "A seagull has somehow acquired a captain's hat. It is wearing it correctly. It is navigating with more authority than the boats.",
        "Someone's entire cargo of something round has escaped and is rolling across the dock. Eight people are chasing it. The cargo is winning.",
        "A sailor is explaining to another sailor that the sea is 'actually not that wet when you think about it.' This conversation has been going for a while.",
        "A dog has been 'helping' unload cargo for four hours. Nobody asked it to help. It is very serious about this. Everyone is working around it.",
        # Dark
        "Three ships from different ports, all with cargo flags that don't match what's listed on the board. Maren's light is on. It is always on.",
        "'These manifests don't match,' a dockworker says quietly to another. A pause. 'They never match.' A longer pause. 'Sign it.' He signs it.",
        "A ship that arrived three weeks ago is still here. No one is loading or unloading. No one is visible aboard. It is just there.",
        "The night crew is different from the day crew. Different badges. You notice this. You're not supposed to notice this.",
        # Story hints
        "Night boat, third bell, no registration lights. You've seen it twice now. Same approach vector. Same nobody watching.",
        "Maren is copying manifests by hand into a second ledger. You can see her through the harbour office window. She doesn't see you.",
        "A dropped cargo tag. The destination code doesn't match any registered port in Ironhaven. You pocket it.",
        # Quotes
        "'Forty-seven,' Maren says, to herself, walking past. 'Forty-seven.' She doesn't explain. You don't ask.",
        "'I've worked this dock twelve years,' the foreman says. 'The night shipments started eight months ago. I haven't logged one of them.' He looks at his clipboard. 'I sign the blank.'",
        "A sailor, drunk, to no one: 'The ore smells wrong. I know ore. This is wrong ore.' Nobody is listening. He keeps talking anyway.",
        # Found objects
        "A dropped manifest. One column is crossed out and rewritten. The original destination is still legible. It's not a registered port.",
        "A cargo tag on the dock road. The weight listed is impossible for the container size. Someone did the math wrong, or someone did the math right and lied.",
    ],

    "ashwood_forest": [
        # Sensory
        "Pine resin and earth and something metallic underneath, faint but persistent. The forest has always smelled like this. It hasn't always smelled like this.",
        "Sound travels strangely between the trees. You hear something ahead, stop, and it's already behind you when you turn.",
        "The light filters through the canopy in columns. Dust and spores moving through each column. Everything slow here except the things you can't see.",
        "Birdsong for about thirty seconds. Then one alarm call, single and sharp. Then nothing. Then normal birdsong again as if it didn't happen.",
        "The path is clear. Too clear. Someone maintains this path. They don't want you to know the path is maintained.",
        # Slice of life
        "A forager stops when he sees you, relaxes slightly when you move on, resumes looking at plants. His basket is already full. He's cataloguing, not collecting.",
        "A ranger, alone, heading in from the east. She marks something on a folded map, re-folds it, sees you, puts it away. 'Afternoon,' she says. 'Afternoon,' you say. That's all.",
        # Absurd
        "A very large crow sits on a branch directly in your path and stares at you with the focused expression of someone who has been expecting you.",
        "You find a perfectly arranged circle of small stones in a clearing. They were arranged deliberately. The arrangement means something. You have no idea what.",
        "A squirrel drops something on your head from a branch. You look up. The squirrel looks down. This was intentional. The squirrel leaves.",
        "You hear whistling ahead. When you round the bend, there's nobody there. The whistling was recent. There's nowhere they could have gone.",
        # Dark
        "Cart tracks here. Heavy load. Going deeper, not toward the registered extraction sites. The brush has been pressed aside deliberately.",
        "Workers' gloves, left by the path. They have dark staining on the palms that doesn't wash out. You've seen this before. Hana sees this weekly.",
        "A snapped torch handle, burn end still warm. Someone was here recently and left in a hurry. Nobody leaves a torch by accident.",
        "The trees are older than Ironhaven. They remember when this was not a forest with a secret in it. The remembering doesn't help them.",
        "Markers on three consecutive trees. Not trail markers — different shape, different knot. Someone maintains a route here that isn't on any official path.",
        # Story hints
        "The ore vein exposed here shouldn't exist on this side of the ridge. The registered operation is two kilometers north. This vein is fresher.",
        "A fire pit, ash still warm. Three cups. Someone met here recently, discussed something, left. The cups are plain — no identifiers.",
        "Fresh wheel ruts going east toward the forest operation. The return ruts are lighter. Something heavy went in. Less came back.",
        # Quotes
        "'The forest protection status was revoked quietly,' Rel said once. 'Buried in a licensing amendment. Nobody voted. Nobody announced it. It just changed one day.'",
        "'Don't go toward the light at night,' old Grull said, and wouldn't explain what light. 'You'll see it. Don't go toward it.'",
        "A ranger's note pinned to a tree: 'If you find this, the route is compromised. Use the eastern ridge. —M' No other signature.",
        # Animals
        "A fox watches you from the undergrowth, unafraid. Foxes near industrial operations lose their fear first. Then everything else.",
        "No birds in the eastern section of the forest. Insects, yes. Wind, yes. No birds. You notice this after the fifth minute.",
        "A deer moves across your path, stops, and doesn't flee. It looks at you with the specific expression of an animal that has decided you are not the most dangerous thing here today.",
        # Weather
        "Rain on the canopy. None reaches you yet. The sound is very large overhead and very quiet around you.",
        "Fog in the lower parts of the forest. Everything below knee height disappears. You walk through visible nothing.",
    ],

    "harbour_docks": [
        "A dock receipt, partially burned. The cargo: 'raw industrial material.' The weight: circled twice in different inks.",
        "Crates stacked higher than they should be, given what they're supposed to contain. Either the labels are wrong or gravity is cooperating unusually.",
        "The night shift is starting. The day shift is leaving. There's a two-minute overlap where both are present. Nobody speaks. Everyone nods.",
        "A newly installed light on the south dock. It wasn't there last week. No official announcement. It illuminates the one area that was previously dark.",
        "Three dock workers are working a crate that should take two. The third worker is just watching the area around them. He's not watching the crate.",
        "'Standard cargo,' the manifest says. Everything listed is standard. The manifest is standard. The fact that everything is so extremely standard is unusual.",
        "A forklift operator eats his lunch without looking up. He has calculated that eating while watching the dock is worse for digestion than not watching.",
        "Someone has stacked the wrong crates together and whoever notices will have to explain why they know they're the wrong crates.",
        "An empty dock space. Something was here yesterday. The tie-offs are still attached to the dock with fresh rope burns.",
        "Four inspectors, one dock. They are inspecting different things. None of them are speaking to each other.",
    ],

    "farmlands": [
        "Open sky. You keep forgetting Ironhaven has this much of it. The port and the city take up all the attention.",
        "A hawk circles the eastern field. The mice in the eastern field are aware of the hawk. The hawk is aware of the mice. The system works.",
        "The soil here is good. You can tell even without knowing much about soil. Something about the color, the density underfoot.",
        "Forty percent. The crops are weighed at harvest and forty percent is taken before the farmer touches anything. The scales are Mercer's scales.",
        "Fence lines tell the history of who owned what before the debts. Some fences are new. Some are old boundaries now crossed by new realities.",
        "Workers move through the field at an efficient pace that isn't rushed. They've calculated exactly how much effort produces exactly the required output. No more.",
        "A child runs between the crop rows playing something. The game requires a lot of space. The farm has exactly this much space, and it was good for something.",
        "The rent collector's cart passes once a month on the first. Every farmer knows when to expect it. The roads are quiet that day in a particular way.",
        "An old irrigation channel runs diagonally through the field, not following the current property lines. The channel is older than the current arrangements.",
        "Evening birds moving over the fields. Hundreds of them, shifting direction as one, folding and unfolding across the sky. The farmers don't look up.",
    ],

    "fishermans_cove": [
        "Low tide. The smell changes completely. More honest. The sea presenting its actual self.",
        "Nets hung to dry catch the morning light. The mesh pattern makes overlapping shadows across the dock boards.",
        "An old boat needs a new hull. New boats cost money. Old boats can still go out with someone who knows them well enough. Old Grull knows his boat that well.",
        "The fishermen don't talk to strangers the way they used to. This happened gradually. You can ask but nobody will say exactly when.",
        "A child on the end of the dock fishing with a bent pin and string. She has caught nothing. She is extremely patient. The fish are not.",
        "Salt marks on every building at high-tide height from three years ago. The tide line has shifted. Old Grull has measured it.",
        "Grull looks at the water near the cave entrance for a long time every morning. He says nothing. He writes something in a small book. He closes the book.",
        "The fish from the eastern channel taste different now. The fishermen stopped selling them six months ago. They didn't announce this. They just stopped.",
        "Rope repairs, hull patches, net-mending — the maintenance of the cove is constant and unglamorous and keeping everything from sinking.",
        "'The sea has worse things in it than weather,' Grull said once, to nobody in particular, looking at the cave entrance.",
    ],

    "ancient_ruins": [
        "The stonework is finer than anything in Ironhaven. Different stone, different cutting. Someone knew what they were doing. They planned for the long term.",
        "Silence here has a different quality. Not the absence of sound. Something that came before sound and will be here after.",
        "Moss grows on specific stones and not others. The pattern follows something. You can't tell what. You keep looking at it.",
        "Footprints in the dust. Recent. More than one set. Heading toward the vault and back. Nothing in the vault is disturbed.",
        "A fire was lit here. The ash is cold now. The stones around it are scorched in a pattern that suggests not the first fire.",
        "The carved walls are consistent — same hand, same era, same script. Whatever built this, they knew they were building something that would outlast them.",
        "Shade sits sometimes. On the same stone each time. You can tell by the wear. Whatever he thinks about, sitting there, he keeps to himself.",
        "The echo here is strange. Your voice comes back from a direction that shouldn't produce an echo. Architecture you don't have the background to understand.",
        "Someone has taken rubbings of the wall carvings. Fresh chalk marks, paper residue. Recently. They were careful. They wanted the detail.",
        "An ancient coin pressed into a crack in the floor. Not dropped — placed. Intentionally. The markings predate any Ironhaven currency by centuries.",
    ],

    "sea_caves": [
        "The cave breathes. Cold air out during the day. Warmer air in at night. The cave is calibrated with the sea in a way you can feel.",
        "Your light catches the ore veins in the wall. They go deep. They go further than you can see. Whatever was here before the current operation found it first.",
        "Dripping water. But not random — rhythmic. Steady enough that it's probably just geology. Probably.",
        "The bioluminescence moves when you get close. Not toward you. Not away. It adjusts, like something accommodating your presence.",
        "Sound from deeper in the cave. Water, yes. Something else, under the water. You can't identify it. You could go deeper. You don't.",
        "Salt crystals on the cave floor. They form in geometric patterns. This is just chemistry. You keep reminding yourself this is just chemistry.",
        "The water is darker near the east passage. Not just depth — a different quality. The fishermen know about this. They don't fish east of the second rock.",
        "Your footsteps echo differently from ten paces into the cave. The geometry changes. There's more space than the entrance suggests.",
    ],

    "smugglers_trail": [
        "The path is invisible from twenty feet away. From the path itself, it's clear. Someone designed this.",
        "Wheel ruts, both directions. The laden ruts going east are twice as deep as the returning ones. Whatever goes in is heavier than what comes back.",
        "A trail marker at eye height. Not the official kind. Different shape, different color. Someone's private language, for private purposes.",
        "Midpoint: you can see Ironhaven's towers behind you and the forest canopy ahead. The trail connects two worlds that officially don't connect.",
        "Fresh brush cuts on either side. The path is maintained. The maintenance is invisible. Someone clears this regularly and doesn't leave a trace.",
        "Two sets of boot prints. They walked together for a while and then one set turned off into the undergrowth. The other continued. You continue.",
        "A dropped oil cloth, fresh, with a faint ore smell. Something was wrapped in this recently. Whatever it was, it moved through here.",
        "Voices ahead. Too far to make out words. When you're close enough, silence. When you're past, they start again.",
    ],

    "shadow_den": [
        "Efficient. Everything here is arranged for efficiency. The people, the equipment, the sightlines. Someone thought this through carefully.",
        "Two guards rotate on a schedule you've mapped. Fourteen minutes, three routes, two overlap points. You've had nothing else to do but watch.",
        "The equipment here is better than Council standard. Different supplier, different quality. Someone is paying significantly above government rate.",
        "Commander Voss walks the compound on a specific route at a specific time. The route has changed twice since you've been watching. She adapts it.",
        "A supply crate stamped 'SVT HOLDINGS.' Not a name you recognize. Not a company registered in Ironhaven.",
        "The mercenaries don't ask questions. This isn't loyalty — it's professionalism. You recognize the difference.",
        "Something changes hands between a mercenary and someone in civilian clothes. The civilian leaves via a different exit than they entered.",
        "The light inside the main compound is always on. Whatever they're working on, they work through the night.",
    ],
}


# =============================================================================
# WALK_EXTENDED_2 — Second pass. Fills thin zones + adds new event types.
# New types: inner thoughts, micro-stories, resistance hints,
# supernatural, economic detail, ultra-short punchy events.
# =============================================================================

WALK_EXTENDED_2: dict[str, list[str]] = {

    "town_square": [
        # Inner thoughts
        "You find yourself counting Mercer's portraits on this block. You lose count at seven and decide this is the correct response.",
        "You realize you've memorized the guard rotation without meaning to. You file this away under 'useful' without examining why.",
        "Something about the way the square is laid out bothers you. Too open. Designed to be watched from above. You look up. Two windows. Right angles.",
        "You walk the square's perimeter without meaning to. It takes exactly the same time every time. You've started timing it.",
        # Micro-stories
        "An old man drops his newspaper. A soldier picks it up for him. The old man thanks him. The soldier nods. They look at each other for half a second longer than necessary. The soldier walks away first.",
        "A boy sells newspapers at the guild steps. He's sold four today. He has fourteen left. He rearranges them by size. He rearranges them again. He eats his lunch.",
        "Two women stop in the middle of the square, embrace briefly, say nothing, and walk in opposite directions. They both look lighter after.",
        "A merchant packs up his stall two hours early. He counts his money. He recounts it. He packs it away. His expression does not change. He goes home.",
        # Resistance hints
        "Three people enter the guild separately, five minutes apart, and take the same table in the back. They arrived as strangers. They're not strangers.",
        "A chalk mark on the fountain base. Small. A circle with a line through it. It wasn't there yesterday. Tomorrow it won't be there either.",
        "The woman who delivers bread to the inn every morning has changed her route. She now passes the harbour office on the way. She's not delivering to the harbour office.",
        # Economic detail
        "A vendor's price board. Potatoes: 8Ƶ. Last month it was 6Ƶ. The month before: 5Ƶ. Nobody has increased wages.",
        "A shop door has two signs: 'MERCER BANK CERTIFIED' at the top, 'WE ACCEPT ALL CURRENCY' in smaller letters below. The contradiction is not noted by anyone.",
        "The guild posts daily wages for contract work. Three months ago there were twelve contracts posted. Today there are four. The wages have not changed.",
        # Punchy/absurd
        "You trip on nothing. You check. There is nothing. You walk away with dignity.",
        "A man waves at you. You wave back. You have never seen this man before. You will never see him again. The wave was sincere.",
        "You step on a squeaky cobblestone for the third time today. You will step on it again. You know this. You cannot prevent this.",
        "A seagull looks at you with contempt. You have done nothing wrong. The seagull doesn't care.",
        "Someone shouts 'HEY!' from across the square. You turn. They were shouting at someone behind you. You turn back. You resume walking.",
        "A child points at you and says something to another child. They both look at you. They look away. You will never know what was said.",
        "You make eye contact with someone going the same direction. You both slow down slightly to avoid walking together. You both speed up slightly. You're walking together now.",
    ],

    "market_quarter": [
        # Inner thoughts
        "You notice Hana's curtains are drawn. They're never drawn during business hours. You keep walking. You write it down in the part of your brain that notices things.",
        "The market has a rhythm. You've started to feel it — the surge at mid-morning, the quiet after lunch, the second surge before closing. You fit into it without meaning to.",
        "You find yourself automatically checking faces. Looking for patterns. When did that start.",
        # Micro-stories
        "A woman buys one apple. She holds it for a moment before putting it in her bag. Not examining it — just holding it. She walks away.",
        "Two old men play chess outside the auction house every day. Today one of them isn't there. The other sets up the board anyway and stares at the empty seat.",
        "A merchant offers a free sample of something. Nobody stops. He eats the sample himself. He makes a note. He adjusts the sign. He tries again.",
        "A young apprentice spills a full bottle of something expensive. He looks at the mess, then at the shop door, then at the mess again. He starts cleaning. He tells no one.",
        # Resistance hints
        "Vex turned a card in his window display to face outward. Just one. It has the closed eye on the back. You've seen that symbol before. Not here. In the ruins.",
        "Tomás leaves bread on the counter at closing and doesn't put it away. Someone collects it after dark. Tomás doesn't see them. This is the arrangement.",
        "A customer at Hana's gives her a folded paper with their purchase. She doesn't open it there. She slips it into her coat. 'Thank you for your business,' she says.",
        # Economic
        "The auction house board has twelve 'OUTSTANDING DEBTS' listed. Seven of them are for businesses. Four of those businesses are still open. Three are not.",
        "Hana's prices went up last month. She posted a notice explaining the increase was beyond her control. She underlined 'beyond her control' twice.",
        "A vendor's permit is posted in the window. It expires in a week. The renewal fee is listed at the bottom. It's twice what it was last year.",
        # Punchy
        "A dog sits outside the general store every day waiting for Tomás to give it something. Tomás gives it something. The dog leaves satisfied. This is the compact.",
        "You look at the prices at the equipment shop. You look at your wallet. You look at the prices again. The prices have not changed to account for your feelings about them.",
        "Vex looks up when you enter the Gilded Draw. Looks back down. This is high praise from Vex.",
        "You buy nothing. Several merchants watch you leave. Their expressions are professional. You feel judged anyway. You were judged anyway.",
    ],

    "residential_ward": [
        # Inner thoughts
        "There's a heaviness here that isn't sadness exactly. More like patience. Like people who've decided to stay put and see what happens next.",
        "You've walked this street six times. You know which door has the broken latch, which window has a plant in it, which corner smells of old pipe smoke. The ward is filing itself in your brain.",
        "You find yourself wondering about the letters that stopped. Whether there's a reason, or just a silence.",
        # Micro-stories
        "A woman repairs the same section of fence every week. It breaks because the post is rotted at the base. She can't afford a new post. She repairs the fence.",
        "Two boys are playing a game that involves a ball, two walls, and rules that seem to change when the rules become inconvenient. Both of them invented the current rules. Both of them are cheating.",
        "An elderly woman waters her windowsill flowers at the same time every morning. Today she's fifteen minutes late. She rushes through it. The flowers don't care. She does.",
        "A man comes out of his house, looks at the sky, goes back inside, comes back out with an umbrella, looks at the sky again, goes back inside. It does not rain.",
        # Resistance
        "Rel's training ground light was on until past midnight last night. People went in and came out at intervals. None of them together. All of them from this ward.",
        "A woman nods at you. Then looks at your hands. Then nods again, differently. You're not sure what you passed or failed. You passed something.",
        "Three different residents have the same mark on their doorframes. Small. Scratched into the wood at knee height. Same shape. Recent.",
        # Economic
        "The debt notices on this block are from six different creditors. All ultimately trace back to the same bank. Nobody on this street has ever been to the bank. The bank has always found them.",
        "A child counts coins on the doorstep. She's counting for a purpose. She finishes counting. She takes two coins back inside. The purpose was not met.",
        "A man examines his rent notice with the expression of someone who has examined it twenty times hoping the number will change. The number hasn't changed. He folds it carefully.",
        # Punchy
        "The ward's cats have a hierarchy. You don't know the full structure. You know you're not at the top.",
        "A door opens. A child looks out. Sees you. Closes the door. This was all the interaction either of you required.",
        "You find two coins in the gutter. This is the best thing that has happened here today. You are the one who found them. This was a good walk.",
        "'Excuse me,' says someone behind you. You move aside. They pass. They don't say thank you. You don't say anything. This is fine. This is how it is.",
    ],

    "port_district": [
        # Inner thoughts
        "The port at night is a different city. You've started to understand the difference between who the port shows during the day and who it actually is.",
        "You've counted twelve ships in the harbour. Seven have standard manifests. Three have altered ones. Two have no manifests posted at all. You know which two.",
        "Something about the tide schedule and the night ship schedule is the same. You haven't confirmed this yet. You're going to confirm this.",
        # Micro-stories
        "A sailor tells a story at a dock table to three people who are clearly not listening. He finishes. He laughs. They laugh. He pays for the round. He starts another story.",
        "A woman waits at the dock gate for an hour. The ship she's watching arrives. Someone comes off. They embrace. She cries. He doesn't. They walk away together.",
        "A dock worker counts something under his breath as crates are unloaded. He finishes counting. He writes a number. He crosses it out. He writes a different number. He pockets the paper.",
        # Resistance
        "Maren walks a specific route home every night. She stops at three places. Each stop is brief. Nothing changes hands. Except the nights she takes the other route. On those nights she stops at one place. Something changes hands.",
        "The harbour notice board has a standard post about cargo regulations. Below it, pinned with the same tack, is a blank piece of paper. Not blank — pale ink. You need the right light.",
        "Bora's tavern has a back room. The back room has a lock. The lock is new. The people who use the back room are regulars. New regulars.",
        # Economic
        "Export levies board: current rate is 23%. Last year: 18%. Year before: 15%. The rate increases every quarter. The goods that are taxed expands every quarter.",
        "Three different dock workers mention the same thing in passing, without connecting them: night cargo, no manifest, high pay, don't ask. They each think this is their job.",
        # Supernatural/mysterious
        "The water near the south dock glows faintly some nights. Not bioluminescence — wrong color, wrong pattern. The dock workers have stopped mentioning it.",
        "A ship that left port eleven days ago is back. The crew won't say where they went. The manifests are clean. Their hands are clean. Their eyes are tired in a specific way.",
        # Punchy
        "A gull steals a fish directly from a man's hand as he's about to eat it. He stares at his empty hand. He stares at the gull. The gull stares back. The gull wins.",
        "You get turned around in the dock maze of crates and end up where you started. Nobody saw. You walk with purpose.",
        "A sailor sneezes so hard he drops a rope. Three things go wrong at once. Everyone moves fast. It is resolved. Nobody speaks of it.",
    ],

    "harbour_docks": [
        # Inner thoughts
        "The docks operate on a logic you're starting to understand. The official layer and the real layer. You can tell them apart now by the sound.",
        "You've been watching the cargo flow for three days. The outbound and inbound don't balance. Something is moving that isn't being counted.",
        # Micro-stories
        "Two inspectors argue about jurisdiction for nine minutes. The cargo they're supposed to inspect is loaded onto a cart during this argument. The cart leaves. The argument continues.",
        "A docker carries a crate alone that should take two people. He doesn't ask for help. Nobody offers. He gets it done. His hands shake after.",
        "A night shift supervisor counts the same crates at the start and end of every shift. The numbers always match. He knows the numbers are wrong. He writes them down anyway.",
        # Resistance hints
        "The loading crane operator's booth has a small mirror angled outward. When certain ships arrive, the mirror catches the sun and flashes across the harbour. Nobody official knows it's a signal.",
        "A chalk mark on a support beam at dock level. Low, where a child or a crouched adult would see it. A date. Two days from now. A dock number.",
        # Economic
        "Mercer's private dock authority processes thirty percent of the cargo. It pays no taxes. It has no public mandate. It was established by regulatory footnote in year two.",
        "The dockers are paid by the crate. The crate definition changed this month. The average pay decreased fifteen percent. The work didn't change.",
        # Supernatural
        "Three dockers independently report the same smell from the same crate on three separate shifts. None of them file a report. The smell is not from anything listed on the manifest.",
        # Punchy
        "A seagull has nested in an inactive crane cab. The crane operator leaves it alone. There is a détente. Both parties seem satisfied.",
        "You count crates. You lose count at thirty-seven. You start again. You lose count at thirty-seven again. You stop counting crates.",
        "A forklift beeps twice. Nobody is near it. It beeps twice again. Nobody looks. The docks have decided this is fine.",
        "Heavy lifting all day. Someone drops something. Nothing breaks. Everyone exhales. Work continues. This was the highlight of the shift.",
        # Quotes
        "'You know what moves through these docks?' the foreman says to nobody in particular. 'Everything. And I mean that the way I say it.'",
        "'I've been logging cargo for twelve years,' the clerk says, stamping a form. 'Last eight months, I log what I'm told to log.' Stamp. 'Same thing, different list.'",
        # History
        "This section of dock was expanded five years ago. Before that, the water came up to where the second warehouse now stands. The old tide marks are still on the original wall.",
    ],

    "farmlands": [
        # Inner thoughts
        "The sky here is enormous. After the city's walls and tight streets, the open sky does something uncomfortable to your sense of proportion.",
        "You realize you've been thinking about the forty percent for ten minutes. What forty percent of everything looks like. Whether anyone ever stops noticing.",
        # Micro-stories
        "A farmer stops her work to drink water and stares at the horizon for exactly sixty seconds. She times it. She gets back to work.",
        "Two farmworkers eat lunch in comfortable silence. One offers the other half of something. The other shakes their head. First one shrugs. They eat in silence. This has never needed words.",
        "A boy tries to learn to whistle by copying the birds. The birds are not helpful. He sounds nothing like them. He sounds a little like them by the end of the afternoon.",
        "An old farmer examines his soil with the focused attention of a doctor reading a patient. He makes a sound — not quite satisfaction, not quite worry. He moves on.",
        # Resistance
        "A barn door has a symbol carved into it at shoulder height. The same symbol as the doorframes in the ward. New. The farmer who lives here is one of three whose son hasn't written.",
        "The old road east is officially disused. You find boot prints on it. More than one set. Regular intervals. Someone has been using it at night.",
        # Economic
        "The scales that weigh the harvest belong to Mercer's collection office. They are certified accurate annually by Mercer's certification office. Nobody else is authorized to certify them.",
        "Forty percent before harvest. Transport levy. Storage levy. If you use Mercer's granary: another three percent. If you don't: you find your own granary. There are no other granaries.",
        "A farming family's debt, posted on a board outside the collection office: four years of normal harvest to clear. That's four years of normal harvest with no other expenses.",
        # Supernatural
        "The eastern field grows differently from the western. Same seeds, same soil. But the eastern rows come up wrong colors. The farmers plant there anyway. They've stopped asking why.",
        # Punchy
        "A goat stares at you from behind a fence. You stare back. Neither of you blinks. You blink first. The goat continues staring.",
        "You walk through someone's field path and emerge on the wrong side. You retrace your steps. You emerge on the wrong side again. You take a third route. Correct side. You say nothing.",
        "A scarecrow is dressed better than most people you've met in the ward. This is a statement the farmer is making. It's not for the crows.",
        "You hear something large move in the crops. It stops. You stop. It moves again. It's a very fat pheasant. You both pretend this didn't happen.",
        # Quotes
        "'You know what good soil means here?' A farmer leans on his fence post. 'More to take. Better soil, bigger levy. We stopped improving the eastern field eight years ago.'",
        "'My grandfather built this farmhouse,' the man says, not to you, just says it. 'His name is not on the deed anymore.'",
    ],

    "ashwood_forest": [
        # Inner thoughts
        "You've been in the forest long enough that the sounds make sense now. Bird means nothing. No bird means something.",
        "The trees don't care about Mercer. They were here before and will be here after. This is either comforting or not depending on how long you've been walking.",
        "You find yourself moving differently here. Quieter. Watching the path and the treeline at the same time. When did that become automatic.",
        # Micro-stories
        "A forager picks specific plants and ignores others. She's been doing this for forty years. She can identify everything that grows here by smell alone. She picks quickly, quietly, and leaves no trace she was here.",
        "Two loggers sit at the edge of the conservation zone and eat in silence. They are not logging. They haven't logged in a week. They sit here anyway because this is where they go.",
        # Resistance
        "Three trees in a row marked with a specific cut. Not blaze marks — different angle, different tool. A trail marker system that isn't in any official guide.",
        "A hollow tree that shouldn't be hollow. Too regular. The hollow has been lined with something waterproof. It's empty now. It hasn't always been empty.",
        "A message scratched into a rock at ground level. Three words. You only catch two before someone approaches the path and you move on.",
        # Economic / Dark
        "The forest operation's sounds carry further at night. Metal on rock, cart wheels, voices. The official position is that night operations don't occur. The sounds continue.",
        "Forty-seven. You've counted forty-seven trips through the Smuggler's Trail since you started watching. That's not occasional extraction. That's a supply line.",
        # Supernatural
        "The grove where the trees are black is bigger than it was last month. You can tell because the trail marker you used last time is now inside the discolored area.",
        "A bird with feathers the wrong shade for any bird you know. It watches you from three different trees in sequence. Moving ahead of you. Not fleeing — directing.",
        "The compass behaves oddly near the eastern section. Not dramatically — just drifts. You reset it. It drifts again. You put it away and use the sun.",
        "At certain angles, the light through the canopy creates a pattern on the forest floor that looks deliberate. A shape you've seen somewhere. Not here.",
        # Punchy
        "A mosquito finds you despite everything. You've accepted this. Some things cannot be prevented. The mosquito feels no particular malice.",
        "You find a perfect walking stick on the path. You carry it for twenty minutes. You put it down when the path clears. You miss it immediately.",
        "The forest is doing the thing where it sounds empty and full simultaneously. You've named this. You call it 'the forest being the forest.'",
    ],

    "cursed_grove": [
        # Inner thoughts
        "You've been timing how long you can stay before the air feels wrong. Today: twelve minutes. Last week: eight. You're either adapting or you're being adapted.",
        "The grove has a center. You know where it is. You haven't gone to the center. You're not sure if you're being careful or being warned off.",
        "The corruption pattern spreads outward from the central stone formation. You've measured it three different ways. It's consistent. It's also growing.",
        # Micro-stories
        "An animal enters the grove perimeter, stops, turns around. Not fleeing — just deciding. The decision is the same every time.",
        "A researcher was here. You can tell from the disturbed soil, the small stakes, the notations scratched into a rock. She left quickly. The notations are unfinished.",
        # Supernatural
        "The black bark is warm to the touch even in cold weather. Not from the sun — the grove doesn't get direct sun. The warmth comes from inside the tree.",
        "You leave a stone at the grove's edge when you enter and find it moved when you come back. Six inches north. Consistent. Every time.",
        "The shadows in the grove don't match the light sources. Small discrepancy. You have to look carefully. Once you see it, you can't stop seeing it.",
        "A bird that was fine outside the grove enters it and immediately leaves. You watch it do this three times. It's trying to reach something inside. It can't make itself do it.",
        "The ground here gives slightly underfoot even where there's no soft soil. Like something hollow beneath. Not a void. Something with mass, but a different mass.",
        "Time passes differently in the grove. Not dramatically — minutes feel like minutes. But when you check how long you've been in, it's always more than you thought.",
        # Resistance hints
        "Someone has been in the grove recently who wasn't afraid of it. The footprints go all the way to the center ring and back. Confident stride. No hesitation.",
        "A symbol scratched into one of the black-bark trees. Not corrupted into the bark — scratched after. Recent. The same closed-eye symbol from the ruins.",
        # Dark
        "The center stone ring wasn't natural formation. Cut stone. Placed deliberately. Whatever placed it knew something about this spot before the ore was exposed.",
        "The corruption moves upward from the roots. Old trees show discoloration up to six feet. The newer afflicted trees show it two feet up. The rate is accelerating.",
        # Punchy
        "Complete silence. No wind. No birds. No insects. You sneeze. The sound is very loud. Nothing responds. The silence returns immediately.",
        "You step on a branch. It cracks. In the grove, this sounds enormous. You freeze. Nothing happens. You have now been afraid of a stick.",
        "The grove has decided you're not a threat. This is not the same as it deciding you're safe.",
    ],

    "sea_caves": [
        # Inner thoughts
        "You've started to understand the cave's rhythm. It's not random. The sounds, the temperature shifts, the light changes — they cycle. Something below is breathing.",
        "The maps of the cave that exist are wrong. Not by accident. Someone drew them wrong on purpose. You've been drawing your own.",
        # Micro-stories
        "A fisherman who comes here regularly has a route he doesn't deviate from. You've watched him. He knows exactly which stones to step on. He's been coming here for years. He stays on the route.",
        "A child from the cove found a cave crystal once and brought it home. Grull made her put it back. He didn't explain why. She put it back. She doesn't come to the caves now.",
        # Supernatural
        "The bioluminescent patches pulse. Not randomly — in a pattern. You've been timing it. Three-two-three-two. Whether this means something is a question you're not ready to answer.",
        "Your voice echoes in this section, but returns in a slightly different pitch. Same words. Different resonance. The cave is changing the sound somewhere between you and the wall.",
        "The water in the east channel glows at night. Not from any biological source the fishermen recognize. The glow started three months ago. The fish avoid that channel.",
        "You find the cave darker than it was last week. The bioluminescent sections have contracted. Something has changed in the cave's equilibrium.",
        "There's a section of wall where the ore veins spell something. You keep telling yourself they don't. You keep looking.",
        # Resistance
        "A supply cache in a dry alcove above the tide line. Carefully sealed. Provisions for several people. It's been here for at least a month. It hasn't been touched.",
        "A rope trail through the cave that isn't for navigation. It's been marked at regular intervals. Someone is preparing a route. Someone who plans to come through here in the dark.",
        # Dark
        "The water that drains from the cave runs into the fishing grounds. The fishermen know this. The fish know this. The fish are adapting to it in ways the fishermen are still documenting.",
        "The ore formation here is the oldest. Earlier than the forest operation. Earlier than Mercer. Someone found this before Mercer did. Mercer found whoever found this before him.",
        # Punchy
        "Your light goes out. You stand in complete darkness for three seconds. You relight it. The cave looks exactly the same as it did. You are fine. Your heart rate disagrees.",
        "Something brushes your ankle in the water channel. Just current. You know it's current. You step back anyway. You are a person of reason who stepped back from current.",
        "The dripping is exactly the same rhythm as a song you know. You hum it for a while. The cave doesn't care. This is fine.",
    ],

    "smugglers_trail": [
        # Inner thoughts
        "You've learned to read the trail by pressure. Soft grass means foot traffic. Compacted earth means cart traffic. The compacted sections all go east.",
        "Forty-seven trips. You've counted forty-seven trips. That's not occasional. That's a schedule. You're on someone's schedule without being on it.",
        # Micro-stories
        "A courier passes you going the opposite direction. Professional pace, no eye contact, small pack. Two minutes later, the sound of his footsteps is gone. The trail absorbed him.",
        "Two men ahead of you stop talking when they hear you. Resume when you're past. You catch: '—third time this week—' and then nothing.",
        # Resistance
        "The trail has two branches at the midpoint. One is on the map. One isn't. The one that isn't shows more use.",
        "A signal mark on a tree at the east fork. Green cloth, tied twice. It wasn't there this morning. Someone tied it in the last six hours.",
        "A message left in a hollow at the trail's halfway point. You're not the intended recipient. You memorize it and put it back. Someone will be back for it.",
        # Supernatural
        "On the trail at dusk, the shadows are wrong. Not dramatically — just angled differently from the light source. Like something else is casting them from somewhere you can't see.",
        # Dark
        "The cargo goes east full and comes back empty or lighter. Something is consumed at the destination. Or stored. Or someone takes ownership.",
        "You count footprints. Eleven pairs of boots going east. Seven pairs returning. Either four people are still there, or four people went east and didn't come back the normal way.",
        # Punchy
        "You step on every twig for thirty meters. The trail seems designed for this. You have announced your presence to every living thing within earshot.",
        "The trail ends at a tree. You circle the tree. The trail continues on the other side. The tree was on the trail. This is fine.",
        "You hear something behind you for three minutes. You stop. Silence. You walk. It follows. You stop. Silence. This continues. It is wind. You know it is wind.",
    ],

    "shadow_den": [
        # Inner thoughts
        "You've mapped the compound in your head. Three exits. Two locked. Eleven guards on rotation. You know this the way you know things you didn't intend to know.",
        "Shade moves through this place like he built it. He didn't. But he understands it the way a soldier understands a position — completely, clinically, including the exits.",
        # Micro-stories
        "Two mercenaries play dice off-shift. One is winning consistently. The other knows why. The other says nothing. The dice keep rolling.",
        "A guard writes something in a small notebook at the end of every shift. Personal log. He keeps it inside his uniform. He's been writing in it for four months. Nobody has asked what's in it.",
        "A young mercenary cleans her weapon with the focused attention of someone who was recently told to clean her weapon and is now thinking about why she was told to clean it now.",
        # Resistance
        "Commander Voss received a message this morning via courier. She read it twice. She burned it. She changed the watch rotation. Someone on the outside knows her rotation.",
        "One of the guards is not what she seems. You don't know which one. You know there is one. The way she watches the others doesn't match the way the others watch the area.",
        # Supernatural
        "The ruins beneath the compound are still active architecturally. The walls settle at night. Old stone finding new positions. The mercenaries have stopped reporting the sounds.",
        "A section of floor in the main compound has markings under a thin layer of new stone. The new stone was laid to cover them. The markings are visible from certain angles.",
        # Economic
        "'SVT Holdings' stamped on sixteen crates. You've confirmed: not a registered company in any of the six jurisdictions you've checked. It exists nowhere official. It owns everything here.",
        "The mercenaries are paid three times Council standard. The math of who funds this at this scale, sustained for eight months, leads to one answer.",
        # Punchy
        "You nod at a guard. He nods back. Both of you maintain expressions that communicate nothing. This is a successful interaction in this location.",
        "A crow lands on the compound wall and is immediately shooed off by two guards. It lands again on the same spot. This continues. The guards are losing.",
        "You've been here long enough to have a usual route. Having a usual route at Shadow Den is possibly a personality flaw.",
    ],

    "ancient_ruins": [
        # Inner thoughts
        "The ruins were built to last. Not optimistically — specifically. The architects knew what they were building and knew something would happen that required it to last. That's a different kind of building.",
        "Three hundred years minimum. Probably more. Whatever was happening three hundred years ago in this place, it mattered enough to build in stone.",
        "You've started to feel that the ruins are aware. Not literally. But the space pushes back in ways that spaces usually don't. You keep adjusting to it.",
        # Micro-stories
        "An archaeologist was here. Not recently. Ten years ago, by the look of the excavation. She started something in the north quadrant and stopped. Whatever she found, she left.",
        "Shade eats here sometimes. At the same stone. You can tell by the arrangement — not careless, not deliberate. Habitual. A person who's been eating at this stone long enough to have a system.",
        "Someone built a shelter in the ruins twenty years ago. Lived here a while. The materials have weathered, but the construction was careful, thoughtful. Someone who planned to stay.",
        # Resistance
        "The vault was used as a meeting point before Mercer came. The resistance that existed then held seven documented meetings here. The notes were hidden. Someone has been looking for the notes.",
        "Three new chalk marks on the vault wall. Initials. Not names — initials. Three different hands. A roll call of some kind.",
        # Supernatural
        "The north wall inscription changes depending on the light. Not the words — the meaning. At dawn it's directions. At noon it's a warning. At dusk, you're still working it out.",
        "An area of the ruins where the compass spins. Consistent. Always the same spot. You mark it on your map. The mark drifts slightly each time you return.",
        "Your reflection in the standing water at the ruins is half a second delayed. Just half a second. You've tested it four times. Half a second, every time.",
        "The symbols here appear in three other places you've found. The ruins, the ore veins, the Sovereignty seal. The same symbol predates all three. It belongs to something earlier.",
        # Punchy
        "You call out 'hello' into the vault to test the echo. It echoes correctly. You feel slightly embarrassed about what you were checking for.",
        "A stone shifts under your foot. You freeze. Nothing happens. You keep walking. Behind you, the stone settles back. Just geology.",
        "You've been in the ruins long enough to have a favorite spot. The stone with the good view and the partial shelter. You sit there without deciding to sit there.",
    ],

    "fishermans_cove": [
        # Inner thoughts
        "The cove has refused every incorporation attempt for forty years. Not loudly. Just: doesn't respond to notices, doesn't attend meetings, keeps fishing. This is a form of politics.",
        "You've started understanding the fishermen's silences. This one means concern. That one means acceptance. That one means there's something in the water they've decided not to describe.",
        # Micro-stories
        "Old Grull repairs his boat by touch in the dark sometimes. He's done it so many times he doesn't need light. The boat has been repaired so many times it's mostly new parts with an old name.",
        "A younger fisherman tries to get Grull to explain a knot. Grull does it once. The younger man tries. Gets it wrong. Grull does it once more. The younger man tries. This continues. Grull is patient. He was taught the same way.",
        "A fishing cat has adopted the dock. It earns its keep. Nobody named it. Everyone calls it something different. The cat responds to the tone, not the words.",
        # Resistance
        "Grull's storage shed has supplies that aren't for fishing. Canned goods. Medical supplies. Rope and canvas. He's been adding to it for six months. He doesn't talk about it.",
        "The old boat shed has been quietly stocked. Not fishing equipment. Different supplies. For people. For several people for several weeks.",
        # Supernatural
        "The eastern channel changes color at dusk. Blue-green shifting toward something else. The fishermen have three different explanations. None of them sound like they believe their own explanation.",
        "Fish behavior around the cave entrance has changed. School patterns altered. The old fishermen use the old patterns. The fish aren't following them anymore.",
        # Dark
        "Grull tested the water near the cave entrance. He doesn't say what he found. He said: 'different.' He said it once and hasn't mentioned it since.",
        "The cove's independence from the port authority is the only thing keeping Mercer's docks from regulating it. They've tried three times. The cove doesn't engage with the process. The process requires engagement to function.",
        # Punchy
        "A seagull stole your focus for thirty seconds just by existing near the dock. You've been thinking about the seagull. You've stopped thinking about the seagull. You're thinking about it again.",
        "You watch a fisherman for five minutes. He doesn't notice. He is focused on a task that requires complete focus. You are not a factor. This is refreshing.",
        "High tide smell. Low tide smell. Middle tide smell. You're starting to be able to tell time by the smell of the cove. You don't know what to do with this skill.",
    ],
}


# =============================================================================
# ZONE MASTERY MILESTONES
# Triggered at 10 / 50 / 100 / 250 total steps in a zone.
# Each tier: XP bonus + a specific revelation for that zone.
# =============================================================================

MASTERY_TIERS = {
    100:  {"label": "🥉 Scout",   "xp": 75,   "emoji": "🥉"},
    500:  {"label": "🥈 Regular", "xp": 200,  "emoji": "🥈"},
    1000: {"label": "🥇 Expert",  "xp": 500,  "emoji": "🥇"},
    5000: {"label": "💎 Master",  "xp": 1500, "emoji": "💎"},
}

MASTERY_STEPS = [100, 500, 1000, 5000]  # imported by cache.py

ZONE_MASTERY_LORE: dict[str, dict[int, str]] = {
    "town_square": {
        100:  "You're beginning to read the square's rhythms — when the guards rotate, where the sightlines are, who watches what.",
        500:  "📖 You've learned: The fountain in the center hasn't been cleaned in six weeks. The maintenance contract is listed as 'completed' in Council records.",
        1000: "🔍 You notice something you missed before: the second-floor windows of the Council Hall face the guild steps at an angle that lets someone inside watch every person who enters or exits the guild. The curtain moves sometimes.",
        5000: "💎 Zone Mastered. You know this square the way you know your own hands. The guard rotation, the regular faces, the three conversations that happen in the same spots every day. And one thing you haven't told anyone: the chalk mark on the fountain base that changes every few days. Someone is communicating through this square. You don't know who. You know what it means now.",
    },
    "market_quarter": {
        100:  "The market's surface rhythm is becoming familiar — the surge at mid-morning, the quiet after lunch.",
        500:  "📖 You've learned: Tomás extends credit to twelve families in the residential ward that he never records in the official ledger. He calls it 'the other book.' There is no other book. The credit is just extended.",
        1000: "🔍 You notice: Hana's shop has a back door that opens to an alley that connects to the harbour office. The route is roundabout enough that nobody would trace it. The door is never locked from the inside.",
        5000: "💎 Zone Mastered. You know who owes who, which prices are real and which are compliance theatre, and which merchant's smile reaches their eyes. More importantly: you know the three people in this market who are watching it for someone else. You don't know who they report to. You know what they watch.",
    },
    "residential_ward": {
        100:  "The ward's quiet has a texture now. You're reading it correctly.",
        500:  "📖 You've learned: Bora from the tavern leaves food at seven specific doors in this ward every week. She doesn't knock. The families don't mention it. It has been happening for four months.",
        1000: "🔍 You notice: Three houses on the east side have small marks scratched into the doorframes at knee height. Same shape, same tool, same approximate date. Someone marked them for a reason. The families inside don't seem to know about the marks, or they're very good at not seeming to know.",
        5000: "💎 Zone Mastered. You know this ward better than most people who live in it. The quiet, the debt, the patience — and underneath the patience, something that isn't patience at all. It's decision. People here are deciding something. They haven't decided yet. But they're closer than they were.",
    },
    "port_district": {
        100:  "The port's layered noise is sorting itself. You can hear past the surface now.",
        500:  "📖 You've learned: The harbour office keeps two sets of manifests. The official ones are available for inspection. The second set is in a locked drawer that only Maren accesses. She updates it daily. She has been doing this for eight months.",
        1000: "🔍 You notice: The night ship that arrives without registration lights always ties at dock 7, pier south. The crew changes hands three times during unloading. Each person who touches the cargo is different from the last. Nobody is ever seen twice. This is deliberate.",
        5000: "💎 Zone Mastered. Forty-seven. You've confirmed forty-seven unregistered shipments over the period you've been watching. The cargo, the route, the timing — it's a supply line, not an operation. Someone is building toward something. The port is the artery. You know the rhythm now well enough to predict the next one.",
    },
    "harbour_docks": {
        100:  "The docks have their own logic. You're starting to read it.",
        500:  "📖 You've learned: The crate weight discrepancies average 40% above listed weight for night shipments. 40% is the same percentage that goes to Mercer from every harvest. This may be a coincidence. You do not think it is a coincidence.",
        1000: "🔍 You notice: There's a section of dock floor, third pier east, where the boards have been replaced recently. The new wood doesn't match. Underneath: a sealed compartment, professionally installed. Empty now. It hasn't always been empty.",
        5000: "💎 Zone Mastered. The docks are a translation layer. Things come in as one thing and leave as another thing. The manifests are the fiction. The weights are the truth. You can read the weights now.",
    },
    "farmlands": {
        100:  "The farmlands' openness is settling into something comprehensible.",
        500:  "📖 You've learned: The eastern fields near the forest have shown soil discoloration for four months. Darker, with a mineral smell after rain. The farmers stopped planting the border rows three months ago. They don't explain this to anyone from the city.",
        1000: "🔍 You notice: The old irrigation channel runs under the eastern field access road. Below where the channel crosses the road, recently disturbed soil. Someone dug here and filled it back carefully. The disturbance is recent — within the week.",
        5000: "💎 Zone Mastered. The farmlands know things the city hasn't been told. The soil changes. The silence when rent collectors pass. The way three farming families haven't mentioned their sons in two months. The land is keeping score. You're keeping score too.",
    },
    "ashwood_forest": {
        100:  "The forest's language is starting to make sense. Bird means nothing. Silence means something.",
        500:  "📖 You've learned: The forest operation runs three shifts. Day shift is registered with the Council as 'geological survey.' Night shift doesn't exist on paper. The equipment for night shift is stored in a structure three kilometers north of the registered site that doesn't appear on any official map.",
        1000: "🔍 You've found it: A secondary extraction site, unmarked, running parallel to the registered operation. The ore here is different — darker, denser, warmer. The workers here are different too. Private security, not Council labor. They don't acknowledge you if you're close enough to see them.",
        5000: "💎 Zone Mastered. You know the forest operation better than most people who work it. Three sites, not one. Two sets of workers. One registered, one not. The ore moves east through the Smuggler's Trail, not through the registered port. Whatever is being built with this ore, it's being built somewhere you haven't found yet. The forest is the source. You need to find the destination.",
    },
    "fishermans_cove": {
        100:  "The cove's silences have started meaning things. You're reading them.",
        500:  "📖 You've learned: Old Grull has been measuring the cave entrance water temperature daily for three months. The temperature has risen 2.3 degrees. He hasn't told anyone. He wrote it in a notebook. You know where the notebook is.",
        1000: "🔍 You notice: The boat shed at the north end of the cove has been stocked. Not with fishing equipment. With provisions for several people for several weeks. The boat inside is seaworthy. The supplies are recent. Grull is preparing something. Or preparing for something.",
        5000: "💎 Zone Mastered. The cove is more than a fishing village. It's a door. The sea entrance, the provision store, the old networks that Mercer never managed to license — they're maintained for a reason. Grull knows why. He hasn't told you. But he's stopped pretending the reason doesn't exist when you're around.",
    },
    "ancient_ruins": {
        100:  "The ruins' weight is sorting itself into something you can work with.",
        500:  "📖 You've learned: The symbol on the north wall appears in three other locations: the ore vein formation in the Cursed Grove, the back of six specific cards in Vex's shop, and stamped on the inside of the Sovereignty seal. The symbol is older than any of the three. It belongs to something that preceded them all.",
        1000: "🔍 You've found it: The vault's sealed chamber has a second entrance. Below the main floor, a passage that leads east under the ruins. It was sealed from the inside. Someone locked it from within and didn't come back through this door. The lock is old. The seal on the lock is the closed eye.",
        5000: "💎 Zone Mastered. The ruins aren't ruins. They're architecture for something that hasn't happened yet. The carvings are navigation instructions for a route that doesn't exist above ground. The ore deposits form the reference points. Whatever the closed-eye organization built this place for — they planned to use it. Shade is here because he knows this. He's waiting for the right time. Or the right person.",
    },
    "cursed_grove": {
        100:  "The grove's wrongness has a shape now. You're mapping it.",
        500:  "📖 You've learned: The corruption follows the ore vein, not the surface. Where the vein goes underground, the surface above shows no symptoms. Where the vein surfaces, the corruption appears within weeks. It's not the grove that's cursed. It's the ore.",
        1000: "🔍 You've measured it: The corruption radius has expanded 3.4 meters in the past month. At this rate, it reaches the farmland border in eleven months. It reaches the aquifer in fourteen. The fishermen downstream are already tasting the difference. Nobody official has been told the expansion rate.",
        5000: "💎 Zone Mastered. You understand the grove now. It's a timeline. The center formation was the original exposure point. The concentric rings of damage mark each month since. The ore was here before Mercer — the grove is older than his operation. He found it. He accelerated it. He didn't create the problem. He inherited it and decided it was acceptable.",
    },
    "sea_caves": {
        100:  "The cave's rhythms are beginning to separate themselves from the random.",
        500:  "📖 You've learned: The sea cave connects to an underwater passage that surfaces 800 meters offshore. The passage has been used. Recently. The disturbed sediment trail goes both directions — something came in and something went out. The fishermen don't use that passage. Something else does.",
        1000: "🔍 You've found it: A cache above the high tide line, sealed, maintained. It's been here for months. The supplies inside are for a person, not for fishing. And a message, folded, addressed to no one by name. You don't read it. You note it exists. You note that someone checks it regularly.",
        5000: "💎 Zone Mastered. The caves are older than the ore operation. The ore operation knows about the caves. The operation didn't tell the Council about the underwater passage. Whatever moves through that passage moves outside all official awareness. You know it exists now. You're one of very few who do.",
    },
    "smugglers_trail": {
        100:  "The trail's logic is resolving. It has one.",
        500:  "📖 You've learned: The trail has been maintained continuously for at least three years based on vegetation patterns. Before Mercer's ore operation, it was used by a different group for different purposes. The same trail, different cargo. The resistance used it before the mercenaries did.",
        1000: "🔍 You've confirmed it: The trail has a second branch, unmarked, that loops back toward the farmlands via the old irrigation channel access. You've walked it twice. It connects to a barn with a false floor. You know which barn.",
        5000: "💎 Zone Mastered. The trail is a spine. The ore moves east along it. Other things move west. The people who built it for ore didn't build it — they found it. The people who built it first are still using it. The cargoes share the route without knowing about each other. You know about both.",
    },
    "shadow_den": {
        100:  "The compound's structure is filing itself into your memory.",
        500:  "📖 You've learned: SVT Holdings was incorporated in a non-disclosure jurisdiction eleven months ago. The timing coincides with Mercer's acceleration of the ore extraction. The corporation has one officer listed. The officer's name is a law firm. The law firm is in a city that doesn't extradite.",
        1000: "🔍 You've found it: One of the mercenaries is not what she appears. Her entry records don't match her employment timeline. She arrived before SVT Holdings was formally established. She was placed before the organization existed publicly. Someone knew this was coming before it was announced.",
        5000: "💎 Zone Mastered. The Shadow Den answers to SVT Holdings which answers to the Sovereignty which answers to something older than either. Voss is a commander but not the authority. The authority has never been to Ironhaven. They don't need to come. Ironhaven is one of several. The ore is one of several. You are looking at a part. The whole is much larger than this island.",
    },
}