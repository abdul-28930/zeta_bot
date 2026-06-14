# =============================================================================
# ZETA — Arc 1 Quest Chains
# "The Weight of Kept Things"
#
# 8 quests per NPC. Each quest earns the next.
# Every quest sends the player somewhere on the map.
# Every quest reveals something human about the giver.
# The main story runs underneath all of it.
#
# Quest structure:
# {
#   "id": str,
#   "title": str,
#   "min_relationship": int,       # score needed to unlock
#   "giver_npc": str,
#   "type": "errand|investigation|intervention",
#   "zone_targets": [str],         # zones the player must visit
#   "npc_targets": [str],          # other NPCs the player interacts with
#   "briefing": str,               # what the NPC says when giving the quest
#   "objective": str,              # what the player must do (displayed in UI)
#   "completion_line": str,        # what the NPC says when player returns
#   "xp": int,
#   "zet": int,
#   "relationship_gain": int,
#   "story_plant": str,            # what this quest quietly plants for later
#   "arc_connection": str,         # which storylet this feeds into
# }
# =============================================================================

QUEST_CHAINS = {

    # =========================================================================
    # OLD TOMÁS
    # The arc: A father who can't say he's scared. Eight quests about watching
    # someone slowly run out of reasons to pretend everything is fine.
    # =========================================================================
    "old_tomas": [

        {
            "id":    "tomas_q1",
            "title": "The Good Flour",
            "min_relationship": 0,
            "giver_npc": "old_tomas",
            "type": "errand",
            "zone_targets": ["fishermans_cove"],
            "npc_targets": ["old_grull"],
            "briefing": (
                "Tomás is reorganizing a shelf that doesn't need reorganizing when you come in.\n\n"
                "*\"Ah! Good timing. I need a favor — not shop business, personal. "
                "The approved flour they send from the Council suppliers tastes like paper. "
                "Old Grull sometimes trades for proper grain from the fishing boats. "
                "Would you pick some up? Tell him it's for me, he'll know the kind.\"*\n\n"
                "He takes coins from his own pocket, not the register.\n\n"
                "*\"It's for Dario's favorite bread. He's coming back — well, "
                "not soon, but when he does. I like to keep in practice.\"*\n\n"
                "He says it like he's been saying it for months. "
                "Because he has."
            ),
            "objective": "Buy proper grain flour from Old Grull at Fisherman's Cove.",
            "completion_line": (
                "He takes the flour and immediately opens the bag to smell it.\n\n"
                "*\"Yes. That's the one. You can always tell by the weight of it.\"*\n\n"
                "He puts it on the shelf behind the counter. Not the supply shelf. "
                "The personal one, where he keeps things that matter.\n\n"
                "*\"He used to eat four of them in one sitting when he was twelve. "
                "His mother said I was spoiling him.\"*\n\n"
                "A pause. He looks at the flour.\n\n"
                "*\"She was right, probably.\"*"
            ),
            "xp": 25, "zet": 35, "relationship_gain": 5,
            "story_plant": "Dario is absent. Tomás marks time by his absence.",
            "arc_connection": "arc1_tomas_letter",
        },

        {
            "id":    "tomas_q2",
            "title": "Maren's Standing Order",
            "min_relationship": 5,
            "giver_npc": "old_tomas",
            "type": "errand",
            "zone_targets": ["port_district"],
            "npc_targets": ["maren"],
            "briefing": (
                "*\"I have Maren's weekly order ready but my delivery boy quit — "
                "Council reassigned him to cargo work, apparently everything is cargo work now. "
                "Could you drop this at the harbour office?\"*\n\n"
                "He hands you a wrapped package — rope, lamp oil, a small jar of something.\n\n"
                "*\"She always pays immediately. Cash. No debt, no ledger — "
                "she said once that she's had enough of other people's ledgers.\"*\n\n"
                "He looks at the package.\n\n"
                "*\"She's good people. One of the ones who was here before Mercer. "
                "We don't talk about what it was like before. "
                "But we both remember.\"*"
            ),
            "objective": "Deliver Maren's weekly order to the Harbour Office in the Port District.",
            "completion_line": (
                "Maren opens the door before you knock — she was expecting the delivery on schedule.\n\n"
                "She takes the package and counts out payment without looking at you.\n\n"
                "*\"Tell Tomás the rope is the right weight this time.\"*\n\n"
                "As you turn to leave:\n\n"
                "*\"He doing alright?\"*\n\n"
                "You say yes. She nods.\n\n"
                "*\"He worries too much. Always has. Good man.\"*\n\n"
                "When you tell Tomás what she said, he smiles — really smiles — "
                "for the first time in a while."
            ),
            "xp": 25, "zet": 30, "relationship_gain": 5,
            "story_plant": "Tomás and Maren know each other. Old Ironhaven network.",
            "arc_connection": "arc1_tomas_letter",
        },

        {
            "id":    "tomas_q3",
            "title": "The Eastern Shipment",
            "min_relationship": 12,
            "giver_npc": "old_tomas",
            "type": "investigation",
            "zone_targets": ["harbour_docks"],
            "npc_targets": [],
            "briefing": (
                "*\"Something's wrong with my supply chain and I can't ask about it "
                "without it becoming official.\"*\n\n"
                "He's quieter than usual. More direct.\n\n"
                "*\"My ingredient orders from the eastern suppliers — three months of delays. "
                "But the manifests say they arrived. They're logged as delivered. "
                "I never received them.\"*\n\n"
                "He slides a manifest copy across the counter.\n\n"
                "*\"The signature on the receipt isn't mine. It's close — same first initial — "
                "but it isn't mine.\"*\n\n"
                "He meets your eyes.\n\n"
                "*\"I'm not asking you to do anything dangerous. "
                "I just need to know if other merchants are having the same problem. "
                "Go to the docks. Look at what's actually there versus what's logged.\"*"
            ),
            "objective": "Investigate the manifest records at Harbour Docks. Compare cargo logs to physical crates.",
            "completion_line": (
                "You return with what you found: four other merchants' cargo listed as delivered, "
                "physically absent. The signature on all of them — the same forged initial.\n\n"
                "Tomás listens without interrupting.\n\n"
                "When you finish, he's quiet for a long time.\n\n"
                "*\"They're not stealing the cargo.\"* He says it slowly, like he's working it out. "
                "*\"If they were stealing it, they'd need to move it. No — they're just redirecting it. "
                "The paperwork says delivered so nobody asks. But it goes somewhere else.\"*\n\n"
                "He looks at the shelf with the flour.\n\n"
                "*\"Dario works for a forest operation. Timber, they said. But if the cargo "
                "manifests are being altered...\"*\n\n"
                "He doesn't finish the sentence. He doesn't need to."
            ),
            "xp": 50, "zet": 45, "relationship_gain": 8,
            "story_plant": "Manifest forgery. First explicit evidence the system is corrupt.",
            "arc_connection": "arc1_tomas_letter",
        },

        {
            "id":    "tomas_q4",
            "title": "Dario's Friends",
            "min_relationship": 22,
            "giver_npc": "old_tomas",
            "type": "errand",
            "zone_targets": ["town_square"],
            "npc_targets": ["captain_rel"],
            "briefing": (
                "He asks the question while wrapping your purchase, not looking at you.\n\n"
                "*\"Dario trained with Rel's people before he left. There were two — "
                "Cassian, the tall one, and a woman called Petra who could outrun everyone. "
                "Could you — I don't want to ask Rel directly. Could you just ask if "
                "they've heard from him? Casually. Like you're just curious.\"*\n\n"
                "He ties the paper wrapping with careful knots.\n\n"
                "*\"I told him training was a waste of time. He did it anyway. "
                "He was like that — decided on things quietly and then just did them.\"*\n\n"
                "He hands over the package.\n\n"
                "*\"Is.\"*\n\n"
                "A beat.\n\n"
                "*\"He is like that. Present tense.\"*"
            ),
            "objective": "Ask Captain Rel about Cassian and Petra — soldiers who trained with Dario.",
            "completion_line": (
                "Rel listens. Goes still in the particular way Rel goes still when "
                "they're controlling a reaction.\n\n"
                "*\"Cassian left Ironhaven four months ago. Petra — "
                "I haven't seen Petra since she took a job at the forest operation "
                "eight months back.\"*\n\n"
                "A pause.\n\n"
                "*\"Tell Tomás they were good soldiers. Both of them.\"*\n\n"
                "When you tell Tomás, he sits down. Just sits, in the chair behind the counter "
                "that he never sits in during business hours.\n\n"
                "*\"Petra too.\"*\n\n"
                "Not a question.\n\n"
                "He looks at his hands. He doesn't say anything else for a long time."
            ),
            "xp": 50, "zet": 0, "relationship_gain": 10,
            "story_plant": "Multiple people from Rel's circle ended up at the operation. Pattern forming.",
            "arc_connection": "arc1_tomas_letter",
        },

        {
            "id":    "tomas_q5",
            "title": "The Debt Document",
            "min_relationship": 35,
            "giver_npc": "old_tomas",
            "type": "investigation",
            "zone_targets": ["town_square"],
            "npc_targets": [],
            "briefing": (
                "He waits until the shop is empty.\n\n"
                "*\"The contract they used to take Dario. I signed part of it — the loan. "
                "But the labour addendum — the clause that said he could fulfill the debt "
                "through work — I didn't sign that part. I would have noticed.\"*\n\n"
                "He's steady. He's thought about this.\n\n"
                "*\"The Council Hall has the original on file. The contract would be in "
                "the debt registry — third floor, public access until the evening bell. "
                "I need to know if my signature is on the addendum. Really mine.\"*\n\n"
                "He takes a breath.\n\n"
                "*\"If it isn't — then they forged it. And if they forged it, "
                "Dario isn't there legally. He's there because they put him there.\"*\n\n"
                "He says it quietly.\n\n"
                "*\"I need to know which thing I'm living with.\"*"
            ),
            "objective": "Access the debt registry in Council Hall. Find Tomás's contract. Check the addendum signature.",
            "completion_line": (
                "The addendum signature is not Tomás's.\n\n"
                "Same initial. Different pressure. Different angle on the T. "
                "You're not a document expert but you don't need to be — "
                "the signature on the shop's own register and the signature on the addendum "
                "do not belong to the same hand.\n\n"
                "When you tell Tomás, he's very still.\n\n"
                "Then, quietly:\n\n"
                "*\"So they took him.\"*\n\n"
                "Not hysteria. Something worse than hysteria — "
                "the absolute stillness of someone whose worst suspicion has been confirmed.\n\n"
                "*\"They took him and they made the paperwork say he chose to go.\"*\n\n"
                "He looks at the flour on the shelf.\n\n"
                "*\"I've been making his bread every week for eighteen months "
                "because I thought it would bring him back. "
                "Like a — like a vigil.\"*\n\n"
                "He stands up.\n\n"
                "*\"Tell me what I can do. Whatever you need from this shop. "
                "Whatever I have. Tell me what I can do.\"*"
            ),
            "xp": 80, "zet": 0, "relationship_gain": 15,
            "story_plant": "Document forgery confirmed. Tomás becomes an active ally.",
            "arc_connection": "arc1_tomas_truth",
        },

        {
            "id":    "tomas_q6",
            "title": "Provisions",
            "min_relationship": 50,
            "giver_npc": "old_tomas",
            "type": "errand",
            "zone_targets": ["market_quarter", "port_district"],
            "npc_targets": ["nurse_hana", "maren"],
            "briefing": (
                "*\"If someone were going to the forest operation — not to work there, "
                "to get someone out — they'd need supplies. Medical. Trail food. "
                "Something for the hands, because the ore does something to skin "
                "and I don't know what.\"*\n\n"
                "He's not asking if you're going. He's preparing as if you are.\n\n"
                "*\"Hana will know what to pack medically. Don't tell her why — "
                "just say forest work, long exposure. She'll understand.\"*\n\n"
                "He hands you a list and enough Zet to cover it.\n\n"
                "*\"And Maren — if anyone knows the night cart schedules on the "
                "Smuggler's Trail, it's Maren. She tracks everything that moves "
                "through this port. If there's a gap in the patrol, she'll know it.\"*\n\n"
                "He straightens his counter.\n\n"
                "*\"I can't go myself. My face is known. But I can prepare.\"*"
            ),
            "objective": "Get medical supplies from Hana. Get patrol schedule information from Maren.",
            "completion_line": (
                "Hana packs the kit without asking the real question. "
                "She adds three things you didn't ask for and says: "
                "*\"For mineral exposure. Apply at the wrists first.\"*\n\n"
                "Maren gives you the cart schedule written in her own shorthand. "
                "At the bottom, she's added: *'Eleven-minute window at the second bell. "
                "I didn't write this.'*\n\n"
                "When you bring everything back to Tomás, "
                "he packages it with the precision of someone who has been running "
                "a shop for thirty years — everything in the right order, nothing wasted.\n\n"
                "*\"I used to pack Dario's school bag like this,\"* he says. "
                "*\"Every morning. Same order.\"*\n\n"
                "He ties the package closed.\n\n"
                "*\"Bring him back. However long it takes. Bring him back.\"*"
            ),
            "xp": 80, "zet": 0, "relationship_gain": 12,
            "story_plant": "Active preparation for forest operation. Three NPCs coordinating.",
            "arc_connection": "arc1_forest_operation",
        },

        {
            "id":    "tomas_q7",
            "title": "After",
            "min_relationship": 65,
            "giver_npc": "old_tomas",
            "type": "intervention",
            "zone_targets": ["ashwood_forest"],
            "npc_targets": [],
            "briefing": (
                "This one he can't say out loud. He writes it on a piece of paper "
                "and slides it across the counter.\n\n"
                "*He's in there. I know he is. I know it like I know the flour. "
                "If you can get in — if there's any way — the workers eat at the "
                "second bell. The perimeter is thinner then. That's from the last letter.*\n\n"
                "He looks at you.\n\n"
                "*\"I'm not a brave man. I've never been a brave man. "
                "I open a shop and I make bread and I keep the accounts. "
                "That's who I am.\"*\n\n"
                "A pause.\n\n"
                "*\"But he's my son. And he's in there because I didn't see "
                "what the loan was until it was too late. "
                "So whatever this costs — it's my debt. Not his.\"*"
            ),
            "objective": "Reach the forest operation during the second-bell shift change. Find Dario.",
            "completion_line": (
                "You found him.\n\n"
                "When you tell Tomás, he sits down in the same chair he sat in "
                "when you told him about the signature.\n\n"
                "But this time it's different.\n\n"
                "He puts both hands flat on the counter and breathes.\n\n"
                "*\"He's alive.\"*\n\n"
                "Not a question. Confirmation of something he's been telling himself "
                "every morning for eighteen months.\n\n"
                "*\"What does he need?\"*\n\n"
                "He's already moving — reaching for the medical kit, "
                "counting coins, thinking in the language of a man who has been "
                "solving practical problems his whole life.\n\n"
                "*\"What does he need and how do I get it to him.\"*"
            ),
            "xp": 120, "zet": 0, "relationship_gain": 20,
            "story_plant": "Dario found. Tomás activated. The circle closes.",
            "arc_connection": "arc1_forest_operation",
        },

        {
            "id":    "tomas_q8",
            "title": "The Bread",
            "min_relationship": 80,
            "giver_npc": "old_tomas",
            "type": "intervention",
            "zone_targets": ["residential_ward", "port_district", "town_square"],
            "npc_targets": ["maren", "captain_rel"],
            "briefing": (
                "The morning after Dario comes home.\n\n"
                "You come into the shop and the plate on the counter is full — "
                "all of them, the ones with seeds on top.\n\n"
                "Tomás is behind the counter. He's been crying and he isn't hiding it.\n\n"
                "*\"Take these. The whole plate. Go to the residential ward first — "
                "there's a family at the end of the second street, three children. "
                "They've been having a hard time. Leave them half.\"*\n\n"
                "He puts a cloth over the plate.\n\n"
                "*\"Then — would you go to Maren? And to Rel? Tell them: "
                "I'm in. Whatever they're planning. I'm in.\"*\n\n"
                "He straightens the cloth.\n\n"
                "*\"I've been watching this city get smaller for eleven years. "
                "I kept my head down. I kept the shop open. "
                "I told myself that was enough.\"*\n\n"
                "He looks at the plate.\n\n"
                "*\"It wasn't enough. But today I made the bread. "
                "That's where I start.\"*"
            ),
            "objective": "Deliver bread to the family in Residential Ward. Tell Maren and Rel that Tomás is in.",
            "completion_line": (
                "The family in the ward opens the door and looks at the bread "
                "like they can't quite believe it's for them.\n\n"
                "The oldest child says: *\"Is this from Tomás?\"* "
                "They knew before you said anything.\n\n"
                "Maren, when you tell her: *\"Good.\"* She adds his name to a list. "
                "You see there are other names already on it.\n\n"
                "Rel, when you tell them: a long pause. Then: "
                "*\"Tell him — tell him I'm sorry it took this long to ask.\"*\n\n"
                "When you return to the shop, Dario is behind the counter. "
                "Working the register. Learning the system. Already.\n\n"
                "Tomás is in the back, making more bread.\n\n"
                "The plate on the counter is empty.\n\n"
                "For the first time in eighteen months."
            ),
            "xp": 150, "zet": 0, "relationship_gain": 25,
            "story_plant": "Tomás officially joins the resistance. Dario's knowledge activates.",
            "arc_connection": "arc1_the_confrontation",
        },
    ],


    # =========================================================================
    # MAREN
    # The arc: A woman who lost everything she built and has been quietly
    # rebuilding in the only way left to her. Eight quests about someone
    # who never stopped fighting — she just changed what she was fighting with.
    # =========================================================================
    "maren": [

        {
            "id":    "maren_q1",
            "title": "The Count",
            "min_relationship": 0,
            "giver_npc": "maren",
            "type": "errand",
            "zone_targets": ["harbour_docks"],
            "npc_targets": [],
            "briefing": (
                "She doesn't look up from her ledger when you walk in.\n\n"
                "*\"I need an independent count of what's on Dock 3. "
                "The official tally doesn't match my records.\"*\n\n"
                "She finally looks up.\n\n"
                "*\"If I go down there and count myself, it becomes official. "
                "Official means it gets flagged. Flagged means someone asks questions "
                "before I'm ready for them to ask questions.\"*\n\n"
                "She holds out a ledger page.\n\n"
                "*\"Count what's there. Write it down. Bring it back. "
                "Don't tell anyone I asked.\"*\n\n"
                "She goes back to her work.\n\n"
                "*\"Well? Go.\"*"
            ),
            "objective": "Count the cargo on Dock 3 at Harbour Docks. Return with accurate figures.",
            "completion_line": (
                "She compares your count to the official tally without comment.\n\n"
                "The difference is eleven crates.\n\n"
                "She writes the number in a small book that goes into her desk drawer. "
                "Not the ledger. The small book.\n\n"
                "*\"Eleven.\"* She says it to herself.\n\n"
                "Then, to you:\n\n"
                "*\"You're accurate. That's useful. Come back tomorrow — "
                "I may have another job.\"*\n\n"
                "It's the closest thing to a compliment she gives."
            ),
            "xp": 30, "zet": 40, "relationship_gain": 5,
            "story_plant": "Discrepancy between official records and reality. Maren is tracking it.",
            "arc_connection": "arc1_maren_manifest",
        },

        {
            "id":    "maren_q2",
            "title": "The Night Watch",
            "min_relationship": 8,
            "giver_npc": "maren",
            "type": "investigation",
            "zone_targets": ["harbour_docks"],
            "npc_targets": [],
            "briefing": (
                "*\"Someone is active on Dock 7 between the second and third bell. "
                "Not dockworkers — they're off shift. Not the official patrol — "
                "I know their schedule.\"*\n\n"
                "She closes her ledger.\n\n"
                "*\"I need to know who and what they're moving. "
                "I need you there at the second bell. Watch from the warehouse side — "
                "there's a gap in the fence near the third post. Don't be seen.\"*\n\n"
                "She looks at you steadily.\n\n"
                "*\"If it's what I think it is, this information matters. "
                "If it isn't, we don't discuss it.\"*"
            ),
            "objective": "Stake out Dock 7 at Harbour Docks during the night shift. Identify who is operating there.",
            "completion_line": (
                "Mercer's private crew. Six men in unmarked clothing. "
                "Loading crates onto a boat with no registration markings. "
                "The crates are heavy — ore-heavy — and they work fast, "
                "practiced, like they've done this many times.\n\n"
                "Maren listens to your description without expression.\n\n"
                "Then she opens the small book from the desk drawer "
                "and adds three lines.\n\n"
                "*\"Third time this month. Same crew. Different boat every time.\"*\n\n"
                "She closes the book.\n\n"
                "*\"They're not hiding it because they think no one's watching. "
                "They're hiding it because they don't think anyone who's watching "
                "would dare do anything about it.\"*\n\n"
                "A pause.\n\n"
                "*\"They're mostly right.\"*"
            ),
            "xp": 45, "zet": 50, "relationship_gain": 8,
            "story_plant": "Private night operations confirmed. Multiple boats. Ongoing operation.",
            "arc_connection": "arc1_maren_manifest",
        },

        {
            "id":    "maren_q3",
            "title": "The Trail",
            "min_relationship": 18,
            "giver_npc": "maren",
            "type": "investigation",
            "zone_targets": ["smugglers_trail"],
            "npc_targets": [],
            "briefing": (
                "*\"The ore isn't coming through the official docks. "
                "I've checked every logged shipment — nothing that accounts for "
                "what I'm seeing on those night boats.\"*\n\n"
                "She spreads a hand-drawn map on her desk. "
                "Not an official map.\n\n"
                "*\"The Smuggler's Trail runs from the port edge to the forest. "
                "If they're moving ore from the forest operation to the night boats, "
                "they're using the trail. I need cart rut counts — "
                "fresh ones, within the last week. And anything left behind. "
                "These crews get lazy.\"*\n\n"
                "She rolls the map up.\n\n"
                "*\"And take the trail, not the main road. "
                "The main road has eyes.\"*"
            ),
            "objective": "Investigate the Smuggler's Trail. Count cart ruts. Look for evidence of regular use.",
            "completion_line": (
                "Forty-plus rut sets in the last week based on depth and layering. "
                "Not occasional — scheduled. And behind a boulder at the trail's "
                "midpoint: a dropped crate tag. The marking is in a code "
                "but one number is readable — the same batch number "
                "you've seen on the Harbour Dock manifests.\n\n"
                "Maren looks at the tag for a long time.\n\n"
                "*\"That's the connection. Forest to trail to dock to boat. "
                "The whole chain.\"*\n\n"
                "She puts the tag in the small book.\n\n"
                "*\"I have forty-seven manifest copies. I have night crew descriptions. "
                "Now I have the physical chain.\"*\n\n"
                "She looks up.\n\n"
                "*\"I need a name. Someone in Ironhaven who connects to "
                "whoever's receiving this. Someone who knows the full picture.\"*\n\n"
                "A pause.\n\n"
                "*\"Shade knows. I don't know how I know that. But I know.\"*"
            ),
            "xp": 60, "zet": 55, "relationship_gain": 10,
            "story_plant": "Full physical chain established. Maren points toward Shade.",
            "arc_connection": "arc1_maren_manifest",
        },

        {
            "id":    "maren_q4",
            "title": "The Cormorant's Papers",
            "min_relationship": 30,
            "giver_npc": "maren",
            "type": "investigation",
            "zone_targets": ["town_square"],
            "npc_targets": [],
            "briefing": (
                "She asks after the shop is empty and the door is closed.\n\n"
                "*\"Before they took my ship, I filed a protest with the Council. "
                "Improper foreclosure. I had the documentation — the loan agreement, "
                "the repayment record, proof the timeline was manipulated.\"*\n\n"
                "She's looking at the window, not you.\n\n"
                "*\"The protest was rejected. No reason given. "
                "But the rejection notice would have a countersigning official's name on it — "
                "whoever rubber-stamped the denial. That name is in the Council Hall archive, "
                "protest registry, three years ago.\"*\n\n"
                "She turns.\n\n"
                "*\"I need that name. Not for any official reason. "
                "For myself. I need to know who signed away my ship.\"*\n\n"
                "Very quietly:\n\n"
                "*\"I've been needing to know for three years.\"*"
            ),
            "objective": "Find Maren's protest rejection notice in Council Hall's archive. Get the countersigning official's name.",
            "completion_line": (
                "The name is Aldric Crane. Council Vice-Administrator for Maritime Assets. "
                "Current position — still active, third office on the left, Council Hall.\n\n"
                "Maren takes the name like she's taking something heavy.\n\n"
                "She writes it down. Looks at it. Folds the paper.\n\n"
                "*\"Aldric Crane.\"*\n\n"
                "She says it the way you learn a thing by saying it once, "
                "clearly, so it doesn't escape.\n\n"
                "*\"He's signed forty-three maritime asset seizures in three years. "
                "I checked after — I've been checking. "
                "Forty-three ships and businesses taken from people who couldn't fight it.\"*\n\n"
                "A long pause.\n\n"
                "*\"The Cormorant. Her name was the Cormorant. "
                "Best boat I've ever sailed.\"*\n\n"
                "It's the first time she's said the name directly to you. "
                "It costs her something."
            ),
            "xp": 70, "zet": 0, "relationship_gain": 15,
            "story_plant": "Council corruption has a name. Aldric Crane connects to the wider seizure pattern.",
            "arc_connection": "arc1_maren_manifest",
        },

        {
            "id":    "maren_q5",
            "title": "The Other Captains",
            "min_relationship": 45,
            "giver_npc": "maren",
            "type": "investigation",
            "zone_targets": ["fishermans_cove", "port_district"],
            "npc_targets": ["old_grull"],
            "briefing": (
                "*\"I'm not the only one they did this to.\"*\n\n"
                "She opens the small book and shows you the last few pages — "
                "names, ship names, dates.\n\n"
                "*\"Twelve captains in three years. All maritime seizures. "
                "All through Aldric Crane's office. "
                "Most of them left Ironhaven after. "
                "But Old Grull — his fishing license was nearly revoked two years ago. "
                "He fought it. He's the only one who fought it and kept something.\"*\n\n"
                "She closes the book.\n\n"
                "*\"Go ask him how he did it. What he used. What made them back off.\"*\n\n"
                "A pause.\n\n"
                "*\"And — ask him how he held on. "
                "I need to understand how someone holds on.\"*"
            ),
            "objective": "Find Old Grull at Fisherman's Cove. Ask him how he kept his fishing license when others lost everything.",
            "completion_line": (
                "Grull takes a long time to answer.\n\n"
                "Then: *\"I had nothing they wanted enough. The cove is nothing — "
                "no deep-water access, no cargo capacity. "
                "Not worth the paperwork of taking it.\"*\n\n"
                "He looks at the water.\n\n"
                "*\"The others had things worth taking. "
                "Maren had the best mid-haul vessel in the harbor.\"*\n\n"
                "And then, quietly: *\"How is she?\"*\n\n"
                "When you tell Maren what Grull said, she's quiet.\n\n"
                "Then: *\"So they took the best ones first. "
                "Then they took what was left.\"*\n\n"
                "She looks out at the harbor.\n\n"
                "*\"The Cormorant. Thirty-one feet. Best boat in Ironhaven.\"*\n\n"
                "She almost smiles.\n\n"
                "*\"Of course they took her first.\"*"
            ),
            "xp": 70, "zet": 0, "relationship_gain": 12,
            "story_plant": "Pattern of targeted asset seizure. The system was designed this way.",
            "arc_connection": "arc1_maren_manifest",
        },

        {
            "id":    "maren_q6",
            "title": "The Forty-Eighth",
            "min_relationship": 60,
            "giver_npc": "maren",
            "type": "investigation",
            "zone_targets": ["harbour_docks", "smugglers_trail"],
            "npc_targets": [],
            "briefing": (
                "*\"Tonight. Second bell. There's going to be a forty-eighth shipment.\"*\n\n"
                "She's already packed what she needs — ledger, manifests, "
                "the small book — in a bag under the desk.\n\n"
                "*\"I need this one documented differently. "
                "Not just rut counts. I need you to physically track the cargo — "
                "Harbour Docks to the trail junction. "
                "Note the number of people. Note the cart type. "
                "Note anything marked on the crates.\"*\n\n"
                "She hands you a second small book, blank.\n\n"
                "*\"Write everything. Your handwriting, your observations, dated. "
                "This becomes a witness account.\"*\n\n"
                "She meets your eyes.\n\n"
                "*\"I've been building this for eight months. "
                "I need one more piece before it's a case, not a complaint.\"*"
            ),
            "objective": "Track the forty-eighth ore shipment from Harbour Docks to the Smuggler's Trail junction. Document everything.",
            "completion_line": (
                "Fourteen crates. Six men. Two carts — heavy-axle, ore-rated. "
                "The crates marked with a symbol you've seen twice before: "
                "a closed eye over a set of scales.\n\n"
                "You write everything in the small book.\n\n"
                "Maren reads it twice.\n\n"
                "*\"That symbol.\"*\n\n"
                "She opens her manifest folder and shows you the back of one document. "
                "The same symbol, stamped faintly in the corner.\n\n"
                "*\"It's on six of the forty-eight. The ones from the earliest shipments. "
                "Before they got careful.\"*\n\n"
                "She looks at you.\n\n"
                "*\"This isn't Mercer's operation. He's running it for someone else. "
                "Someone who was here before him and will be here after him.\"*\n\n"
                "A pause.\n\n"
                "*\"That changes what we're dealing with.\"*"
            ),
            "xp": 90, "zet": 0, "relationship_gain": 15,
            "story_plant": "Sovereignty symbol appears. First direct evidence of the larger organization.",
            "arc_connection": "arc1_shade_meeting",
        },

        {
            "id":    "maren_q7",
            "title": "The List",
            "min_relationship": 75,
            "giver_npc": "maren",
            "type": "intervention",
            "zone_targets": ["residential_ward", "port_district", "farmlands"],
            "npc_targets": [],
            "briefing": (
                "She hands you a folded piece of paper.\n\n"
                "*\"Seven names. People I trust. People who've been watching and "
                "waiting for someone to do something.\"*\n\n"
                "She looks at the harbour through the window.\n\n"
                "*\"I've been doing this alone for eight months because I didn't "
                "know who else was doing it. But the manifest I gave to Tomás — "
                "he said two other shop owners had the same problem. "
                "The workers Hana's treating — there are families. "
                "Rel has people.\"*\n\n"
                "She turns.\n\n"
                "*\"I need to know who's ready. Not who's angry — everyone is angry. "
                "Who's ready to act when the moment comes.\"*\n\n"
                "She taps the paper.\n\n"
                "*\"Go to each name on that list. Just say: 'Maren asks if you're ready.' "
                "Don't explain. See what they say.\"*"
            ),
            "objective": "Visit each name on Maren's list across the city. Deliver her message. Report their answers.",
            "completion_line": (
                "Every single one of them says yes.\n\n"
                "Not dramatically. No speeches. The woman in the residential ward "
                "wiping her hands on an apron: *\"Tell her yes.\"* "
                "The former dock worker in the port district: *\"Tell her I've been ready for two years.\"* "
                "The farmer at the Farmlands border who hasn't said anything "
                "in a conversation with you before: *\"Yes.\"*\n\n"
                "When you tell Maren, she sits down.\n\n"
                "She doesn't say anything for a moment.\n\n"
                "Then:\n\n"
                "*\"Seven people I know. Seven people who didn't know each other were waiting. "
                "All of them ready.\"*\n\n"
                "She looks at her desk — the manifests, the small book, three years of careful documentation.\n\n"
                "*\"I've been thinking of this as a case to build. Evidence to gather. "
                "Something that could be taken to an authority that doesn't exist.\"*\n\n"
                "She straightens.\n\n"
                "*\"It isn't a case. It's a city.\"*"
            ),
            "xp": 100, "zet": 0, "relationship_gain": 18,
            "story_plant": "The resistance network is real and larger than Maren knew.",
            "arc_connection": "arc1_the_confrontation",
        },

        {
            "id":    "maren_q8",
            "title": "The Cormorant's Last Run",
            "min_relationship": 90,
            "giver_npc": "maren",
            "type": "intervention",
            "zone_targets": ["harbour_docks", "port_district"],
            "npc_targets": [],
            "briefing": (
                "She's at the dock's edge when you find her, looking at a ship.\n\n"
                "The Cormorant — different name now, different paint — "
                "is in port for a single night. Resupply stop.\n\n"
                "*\"She came back.\"*\n\n"
                "She doesn't look at you.\n\n"
                "*\"I need her logbooks. The ones they'd have kept when they took her — "
                "the original journey logs, before they renamed her. "
                "They're either on board in the captain's locker "
                "or they were destroyed.\"*\n\n"
                "She's still looking at the ship.\n\n"
                "*\"If they kept them — if the logs are there — "
                "they'll show the original seizure route. "
                "Where she was taken. Who was on board when they brought her in. "
                "One of those names will connect to Aldric Crane.\"*\n\n"
                "A pause.\n\n"
                "*\"That's the reason. But honestly — "
                "I just need to know if she's alright.\"*\n\n"
                "She almost laughs at herself.\n\n"
                "*\"Thirty-one feet of wood and rope and I miss her like a person.\"*"
            ),
            "objective": "Board the renamed Cormorant at Harbour Docks. Find and retrieve the original journey logs.",
            "completion_line": (
                "The logs are there. In the captain's locker, under three years of new records, "
                "the original journey logs in Maren's own handwriting — "
                "every voyage, every port, every cargo. The last entry in her hand:\n\n"
                "*Day 1,847. Ironhaven harbour. Engine maintenance. Home.*\n\n"
                "The next entry is in a different hand. Official. Clinical. The new name.\n\n"
                "When you give the logs to Maren, she holds them for a long time "
                "without opening them.\n\n"
                "Then she opens to the last entry and reads it.\n\n"
                "She's quiet for a long time.\n\n"
                "*\"She's in good repair,\"* she finally says. "
                "*\"Whoever took her — they maintained her properly.\"*\n\n"
                "She closes the log.\n\n"
                "*\"That helps, actually.\"*\n\n"
                "She looks at the harbour.\n\n"
                "*\"Let's finish this. I'm done waiting.\"*"
            ),
            "xp": 150, "zet": 0, "relationship_gain": 25,
            "story_plant": "Maren fully activated. The Cormorant as emotional closure frees her to act.",
            "arc_connection": "arc1_ironhaven_chooses",
        },
    ],


    # =========================================================================
    # NURSE HANA
    # The arc: A healer who took an oath to treat everyone and has been
    # watching people get hurt by the same source she can't expose.
    # Eight quests about the cost of bearing witness.
    # =========================================================================
    "nurse_hana": [

        {
            "id":    "hana_q1",
            "title": "The Herbs",
            "min_relationship": 0,
            "giver_npc": "nurse_hana",
            "type": "errand",
            "zone_targets": ["ashwood_forest"],
            "npc_targets": [],
            "briefing": (
                "She asks while labeling something at her counter, "
                "without turning around.\n\n"
                "*\"I need wolfsbane from the Ashwood. Fresh — the dried supply "
                "loses potency after six months and mine is eight.\"*\n\n"
                "She turns and writes down exactly what to look for.\n\n"
                "*\"Stays on the main path. You'll find it near the large oak "
                "at the first fork — it grows in the root shadow.\"*\n\n"
                "She hands you the note.\n\n"
                "*\"And don't go deeper. The path past the second marker — "
                "people have come back from there with things I don't know how to treat.\"*\n\n"
                "She says it simply. Like it's a medical fact."
            ),
            "objective": "Gather fresh wolfsbane from Ashwood Forest. Stay on the main path.",
            "completion_line": (
                "She examines the herbs immediately, checking the leaves, "
                "smelling the stems, testing something with a drop of solution.\n\n"
                "*\"Good. These are fresh.\"*\n\n"
                "She labels them with the date and her precise handwriting "
                "and puts them in exactly the right place on exactly the right shelf.\n\n"
                "*\"Thank you.\"*\n\n"
                "She goes back to work.\n\n"
                "Then, without turning around:\n\n"
                "*\"Did you see anything unusual on the path?\"*\n\n"
                "She's asking clinically. Professionally. She's been asking "
                "everyone who goes to the forest this question for months."
            ),
            "xp": 25, "zet": 35, "relationship_gain": 5,
            "story_plant": "Hana has been monitoring the forest for months. Something is coming back from there.",
            "arc_connection": "arc1_hana_records",
        },

        {
            "id":    "hana_q2",
            "title": "Grull's Tincture",
            "min_relationship": 8,
            "giver_npc": "nurse_hana",
            "type": "errand",
            "zone_targets": ["fishermans_cove"],
            "npc_targets": ["old_grull"],
            "briefing": (
                "*\"Old Grull makes a saltwater tincture I cannot replicate. "
                "I've tried four times. Something in how he processes the kelp.\"*\n\n"
                "She writes the order carefully.\n\n"
                "*\"Tell him it's for medical use — he has a different price for that. "
                "And tell him I said the last batch worked better than anything "
                "I had for the breathing cases this winter.\"*\n\n"
                "She pauses.\n\n"
                "*\"He won't say anything about that. But he'll know it mattered.\"*\n\n"
                "She folds the note.\n\n"
                "*\"He's one of the people in this city who does exactly what he says. "
                "I find that restful.\"*"
            ),
            "objective": "Buy saltwater tincture from Old Grull at Fisherman's Cove. Tell him the message from Hana.",
            "completion_line": (
                "Grull takes the order. Takes the message. "
                "Doesn't say anything in response — just nods once, "
                "and when he bags the tincture, he adds a second bottle without charging for it.\n\n"
                "When you tell Hana what he did, she's quiet for a moment.\n\n"
                "*\"He does that. He's been doing that for years.\"*\n\n"
                "She puts both bottles in her cabinet.\n\n"
                "*\"There are people in this city who have been quietly taking care "
                "of other people this whole time. Without being asked. Without anyone knowing.\"*\n\n"
                "She straightens the shelf.\n\n"
                "*\"I think about that. On the difficult days, I think about that.\"*"
            ),
            "xp": 30, "zet": 35, "relationship_gain": 6,
            "story_plant": "Informal support network exists. Hana, Grull, others maintaining it quietly.",
            "arc_connection": "arc1_hana_records",
        },

        {
            "id":    "hana_q3",
            "title": "The Worker",
            "min_relationship": 16,
            "giver_npc": "nurse_hana",
            "type": "investigation",
            "zone_targets": ["farmlands"],
            "npc_targets": [],
            "briefing": (
                "She waits until the shop is empty.\n\n"
                "*\"A patient came in two days ago. Timber worker, forest operation. "
                "He had a hand injury. He told me he'd fallen.\"*\n\n"
                "She describes the injury precisely — the pattern of damage, "
                "the specific tissue involved, what falling could and couldn't cause.\n\n"
                "*\"He didn't fall. I documented what he told me. "
                "In the other column, I documented what I saw.\"*\n\n"
                "She looks at you steadily.\n\n"
                "*\"He's back at work — Farmlands border, he said. "
                "I need to know if he's actually alright. "
                "I can't go myself without it becoming a house call, "
                "which becomes official, which puts him at risk.\"*\n\n"
                "She writes a name.\n\n"
                "*\"His name is Edric. He'll be working the east plot. "
                "Just — see how he is. Whether he's afraid.\"*"
            ),
            "objective": "Find Edric at the Farmlands east plot. Check on his condition. Don't make it obvious you're there for him.",
            "completion_line": (
                "Edric is working. He's alright — physically. "
                "But when you get close enough to observe, "
                "his hands move differently than they should for a man his age. "
                "Protective. Careful. Aware of being watched.\n\n"
                "When you mention Hana's name quietly, he goes still.\n\n"
                "*\"Tell her — tell her thank you. And tell her about the ones who stopped coming.\"*\n\n"
                "He goes back to work before you can ask what he means.\n\n"
                "When you tell Hana, she goes still too.\n\n"
                "*\"How many?\"*\n\n"
                "You don't know. That's the problem. She knows.\n\n"
                "She opens the ledger. Points to a column near the back — "
                "twelve names with a small mark beside each.\n\n"
                "*\"These patients stopped coming. "
                "Workers who were coming weekly. "
                "Then they didn't.\"*\n\n"
                "She closes the ledger.\n\n"
                "*\"People who are fine stop needing treatment. "
                "People who aren't fine stop being able to come.\"*"
            ),
            "xp": 55, "zet": 0, "relationship_gain": 10,
            "story_plant": "Workers are disappearing or unable to leave. The operation is worse than known.",
            "arc_connection": "arc1_hana_records",
        },

        {
            "id":    "hana_q4",
            "title": "What the Ore Does",
            "min_relationship": 28,
            "giver_npc": "nurse_hana",
            "type": "errand",
            "zone_targets": ["cursed_grove"],
            "npc_targets": [],
            "briefing": (
                "She puts a small sealed jar on the counter.\n\n"
                "*\"I need a comparison sample. The workers from the forest operation — "
                "what I'm seeing in their tissue matches exposure to a mineral compound. "
                "But I don't have a clean sample to compare against.\"*\n\n"
                "She looks at you carefully.\n\n"
                "*\"The Cursed Grove. There's a formation there — "
                "black ore crystals, different from the standard vein material. "
                "Darker. Warmer. I've heard descriptions from patients who've seen both.\"*\n\n"
                "She holds out the jar.\n\n"
                "*\"Small piece. Wrapped, don't touch it directly. "
                "I need to know if the composition matches what I'm seeing in the workers.\"*\n\n"
                "She hesitates.\n\n"
                "*\"If it matches — if the ore in the grove and the ore in their tissue "
                "are the same compound — then I know what's happening to them. "
                "And I know it doesn't stop.\"*"
            ),
            "objective": "Retrieve a sample of black ore from the Cursed Grove. Handle carefully.",
            "completion_line": (
                "She tests the sample immediately, methodically, "
                "with tools you don't have names for.\n\n"
                "It takes an hour. She doesn't speak during it.\n\n"
                "When she's done, she puts the tools down very carefully.\n\n"
                "*\"It matches. The compound in the grove sample and the mineral deposits "
                "in the workers' tissue are the same origin material.\"*\n\n"
                "A pause.\n\n"
                "*\"The workers aren't just being exposed to the ore. "
                "The ore is — accumulating. In them. Progressive. "
                "Without intervention it will —\"*\n\n"
                "She stops.\n\n"
                "Starts again:\n\n"
                "*\"The twelve who stopped coming. They didn't stop because they got better.\"*\n\n"
                "She sits down on the stool behind her counter. "
                "Just for a moment. Then she stands up again.\n\n"
                "*\"I need to add to the ledger.\"*"
            ),
            "xp": 70, "zet": 0, "relationship_gain": 14,
            "story_plant": "The ore is fatal with prolonged exposure. The operation is killing people.",
            "arc_connection": "arc1_hana_records",
        },

        {
            "id":    "hana_q5",
            "title": "The Delivery",
            "min_relationship": 42,
            "giver_npc": "nurse_hana",
            "type": "intervention",
            "zone_targets": ["ashwood_forest"],
            "npc_targets": [],
            "briefing": (
                "*\"There are three workers who come to me unofficially. "
                "They can't come to the clinic — they're watched. "
                "They meet me on the forest path at the first marker, at dusk.\"*\n\n"
                "She's preparing a medical kit while she talks.\n\n"
                "*\"I can't go tonight. I have a patient who can't be left. "
                "I need you to take this to them.\"*\n\n"
                "She seals the kit.\n\n"
                "*\"The mineral chelation compound — two doses each. "
                "Show them how to apply it. Wrists first, then the hands. "
                "It won't reverse the damage but it will slow it.\"*\n\n"
                "She hands over the kit.\n\n"
                "*\"And ask them — I've been trying to understand the timeline. "
                "Ask how long the ones who stopped coming had been at the operation. "
                "I need to know how much time we have.\"*"
            ),
            "objective": "Deliver Hana's medical supplies to three workers at the Ashwood forest path at dusk. Learn how long the affected workers had been at the operation.",
            "completion_line": (
                "The three workers meet you at the marker. "
                "They take the kit and listen to your instructions carefully — "
                "the practiced attention of people used to memorizing things quickly.\n\n"
                "When you ask about the timeline, the oldest one says: "
                "*\"The ones who went quiet — they'd been there the longest. "
                "Two years plus. We've been there fourteen months.\"*\n\n"
                "A pause.\n\n"
                "*\"Tell her we have eight months. Maybe ten.\"*\n\n"
                "When you tell Hana, she opens the ledger "
                "and does math in the margin.\n\n"
                "Then she closes it.\n\n"
                "*\"Eight months.\"*\n\n"
                "She stands very still for a moment.\n\n"
                "*\"Then we don't have the luxury of waiting for the right moment. "
                "This is the right moment. Whatever it takes.\"*\n\n"
                "She looks at you directly.\n\n"
                "*\"What do you need from me?\"*"
            ),
            "xp": 80, "zet": 0, "relationship_gain": 16,
            "story_plant": "Deadline established. Eight months before workers with longest exposure die.",
            "arc_connection": "arc1_hana_records",
        },

        {
            "id":    "hana_q6",
            "title": "The Testimony",
            "min_relationship": 58,
            "giver_npc": "nurse_hana",
            "type": "errand",
            "zone_targets": ["port_district", "town_square"],
            "npc_targets": ["maren", "captain_rel"],
            "briefing": (
                "She hands you the ledger.\n\n"
                "Not a copy. The original.\n\n"
                "*\"Take this to Maren first. She needs to see the shipment dates "
                "alongside the patient intake dates — they correlate. "
                "Every time there's a large shipment, more workers come in injured "
                "within three days. That's not coincidence, that's extraction pressure.\"*\n\n"
                "She writes a note for Maren.\n\n"
                "*\"Then take it to Rel. They have — they have people who were "
                "in that operation. They should know what's happening to them.\"*\n\n"
                "Her voice is steady. She has been preparing to say all of this.\n\n"
                "*\"I kept this ledger because I believed in a record. "
                "That someone, someday, would ask. "
                "I'm done waiting to be asked.\"*"
            ),
            "objective": "Bring Hana's ledger to Maren in the Port District. Then bring it to Captain Rel in Town Square.",
            "completion_line": (
                "Maren reads the ledger in silence for twelve minutes. "
                "Then she opens her own manifest folder and lays them side by side.\n\n"
                "She points to three dates. Shipment days. "
                "On the ledger, worker intake spikes on the same days.\n\n"
                "*\"They push harder when a shipment is due.\"*\n\n"
                "Rel reads it differently — scanning for names, "
                "finding two that make them close their eyes briefly.\n\n"
                "*\"These are people from my training roster.\"*\n\n"
                "When you return to Hana with both reactions, she nods.\n\n"
                "*\"Maren has the chain of evidence. Rel has the people.\"*\n\n"
                "She takes the ledger back.\n\n"
                "*\"I have the medical record. Three parts of the same truth.\"*\n\n"
                "She looks at you.\n\n"
                "*\"Is it enough?\"*"
            ),
            "xp": 90, "zet": 0, "relationship_gain": 15,
            "story_plant": "Three evidence streams converge. Maren, Hana, Rel all have pieces of the same picture.",
            "arc_connection": "arc1_hana_records",
        },

        {
            "id":    "hana_q7",
            "title": "The Ones Who Can't Wait",
            "min_relationship": 72,
            "giver_npc": "nurse_hana",
            "type": "intervention",
            "zone_targets": ["ashwood_forest", "fishermans_cove"],
            "npc_targets": ["old_grull"],
            "briefing": (
                "*\"There are workers who have been in the operation for over eighteen months. "
                "The three I've been treating are fourteen months — they have time. "
                "But there are others I've never seen, who have never been able to come to me.\"*\n\n"
                "She's making up a larger supply kit.\n\n"
                "*\"When the operation is exposed — when we move — "
                "those workers need to come out at the same time. "
                "And they'll need somewhere to go immediately. Not a plan. Somewhere physical.\"*\n\n"
                "She seals the kit.\n\n"
                "*\"Old Grull has a boat shed at the cove. "
                "It's large enough. It's off the official dock registry. "
                "I need to ask him if we can use it.\"*\n\n"
                "She hesitates.\n\n"
                "*\"I can't ask him myself. We don't — "
                "I've never asked him for anything like this. "
                "I don't know what he'll say.\"*"
            ),
            "objective": "Ask Old Grull if his boat shed at Fisherman's Cove can be used as a safe staging point when the workers are brought out.",
            "completion_line": (
                "Grull listens to the whole thing. Doesn't ask questions. "
                "When you finish, he looks at the shed.\n\n"
                "*\"Been keeping that empty for three years. "
                "Thought about selling it.\"*\n\n"
                "He picks up his fishing line.\n\n"
                "*\"Tell Hana yes. Tell her I'll stock it. Food, water, blankets. "
                "She shouldn't have to ask twice.\"*\n\n"
                "When you tell Hana, she sits very still for a moment.\n\n"
                "Then: *\"He said he'd stock it.\"*\n\n"
                "She writes something in the ledger. Not a patient note. "
                "Just: *Grull — shed — yes.*\n\n"
                "*\"This is what I've been holding onto,\"* she says quietly. "
                "*\"Not the evidence. The fact that there are people like this. "
                "People who say yes before you finish asking.\"*"
            ),
            "xp": 100, "zet": 0, "relationship_gain": 18,
            "story_plant": "Safe house established. Exit route for workers exists. Grull joins the network.",
            "arc_connection": "arc1_the_confrontation",
        },

        {
            "id":    "hana_q8",
            "title": "After the Clinic",
            "min_relationship": 85,
            "giver_npc": "nurse_hana",
            "type": "intervention",
            "zone_targets": ["town_square", "residential_ward"],
            "npc_targets": ["captain_rel"],
            "briefing": (
                "The morning after the workers come out of the forest.\n\n"
                "The boat shed is full. Hana has been there since before dawn "
                "and will be there until tonight.\n\n"
                "She finds you for five minutes.\n\n"
                "*\"The workers need continued treatment — the mineral chelation, "
                "the tissue work. I can do this at the clinic but I need people to know "
                "they can come without being watched.\"*\n\n"
                "She looks tired. The good kind of tired.\n\n"
                "*\"I need Rel to post two of their people at the clinic entrance — "
                "just visible, just present. Not guarding. Just there. "
                "So people know it's safe.\"*\n\n"
                "She hands you a list.\n\n"
                "*\"And this — take this to the residential ward. "
                "Three families whose members are in the shed. "
                "Tell them where to come. Tell them today.\"*\n\n"
                "She goes back.\n\n"
                "*\"Tell them their people are alive. Start with that.\"*"
            ),
            "objective": "Ask Rel to station people at the clinic. Deliver the news to three families in the Residential Ward that their loved ones are alive.",
            "completion_line": (
                "Rel sends four people, not two.\n\n"
                "The families in the residential ward — the first door, "
                "a woman opens it and you say: *'Your husband is alive, '* "
                "and she grabs the doorframe.\n\n"
                "The second door — a man who has clearly not been sleeping. "
                "He listens to the whole thing without expression. "
                "Then he puts on his coat and says: *'Take me there.'*\n\n"
                "The third door — children answer. They're too young "
                "to fully understand but they understand enough.\n\n"
                "When you return to Hana at the end of the day, "
                "the boat shed is different — families are there, "
                "and the workers don't look like workers from an operation anymore. "
                "They look like people.\n\n"
                "Hana is writing in the ledger. Patient notes. Real ones.\n\n"
                "*\"I have been keeping records for fourteen months,\"* she says "
                "without looking up. *\"Of people I couldn't help.\"*\n\n"
                "She writes another entry.\n\n"
                "*\"I'm going to keep records now of people I can.\"*"
            ),
            "xp": 150, "zet": 0, "relationship_gain": 25,
            "story_plant": "Hana's arc complete. The clinic becomes a center of the new Ironhaven.",
            "arc_connection": "arc1_ironhaven_chooses",
        },
    ],


    # =========================================================================
    # CAPTAIN REL
    # The arc: Someone who made a choice eight years ago to wait for the right
    # moment, and has been wondering ever since if the right moment exists.
    # =========================================================================
    "captain_rel": [

        {
            "id":    "rel_q1",
            "title": "Assessment",
            "min_relationship": 3,
            "giver_npc": "captain_rel",
            "type": "errand",
            "zone_targets": ["residential_ward"],
            "npc_targets": [],
            "briefing": (
                "He lowers his voice. Not secretive — precise.\n\n"
                "*\"Simple task. There are three people in the Residential Ward "
                "I\'ve had my eye on. They came to me a few weeks ago asking about training. "
                "I want to know if they\'re serious or just restless.\"*\n\n"
                "*\"Go to the Residential Ward. Walk around. "
                "Get a feel for the place and the people. "
                "That\'s it.\"*\n\n"
                "He looks at you directly.\n\n"
                "*\"When you\'ve been there — come back. Tell me what you saw. "
                "I\'ll know if you actually paid attention.\"*\n\n"
                "**Your objective:** Travel to the Residential Ward, then return to Rel."
            ),
            "objective": "Travel to the Residential Ward. Then return to Rel at the Training Grounds.",
            "completion_line": (
                "He listens to what you describe — how people carried themselves, "
                "what the ward felt like, what you noticed.\n\n"
                "When you finish, he nods once.\n\n"
                "*\"The first two names on my list. I thought so.\"*\n\n"
                "He makes a note.\n\n"
                "*\"You have a reasonable eye.\"*\n\n"
                "He says it plainly. No warmth, no performance. "
                "From Rel, this is a considerable thing to say."
            ),
            "xp": 25, "zet": 30, "relationship_gain": 5,
            "story_plant": "Rel is quietly recruiting. Building something specific.",
            "arc_connection": "arc1_the_confrontation",
        },

        {
            "id":    "rel_q2",
            "title": "Harwick",
            "min_relationship": 8,
            "giver_npc": "captain_rel",
            "type": "errand",
            "zone_targets": ["farmlands"],
            "npc_targets": [],
            "briefing": (
                "*\"There's a retired soldier at the Farmlands border — Harwick. "
                "He served under me. He hasn't checked in this month.\"*\n\n"
                "They don't elaborate on what 'checked in' means.\n\n"
                "*\"Go make sure he's alright. If he's fine, just say I asked after him. "
                "If he's not — come back and tell me.\"*\n\n"
                "A beat.\n\n"
                "*\"Don't ask him about his situation directly. "
                "Ask about the farm. "
                "He'll tell you what he wants you to know through what he says "
                "about the farm.\"*"
            ),
            "objective": "Check on Harwick at the Farmlands border. Ask about the farm.",
            "completion_line": (
                "Harwick is fine. The farm is not.\n\n"
                "Three months of the forty percent, a bad yield, "
                "and a debt extension that added interest he can't service. "
                "He talks about all of this while talking about crop rotation.\n\n"
                "At the end: *\"Tell Rel I heard cart noise again last night. "
                "From the forest. Second bell. Heavy.\"*\n\n"
                "He goes back to work.\n\n"
                "When you tell Rel, they're quiet for a moment.\n\n"
                "*\"How far behind is he?\"*\n\n"
                "You tell them.\n\n"
                "Rel takes coins from their own pocket. "
                "Not many — just enough.\n\n"
                "*\"Give this to him next time you pass. Tell him it's for seed stock. "
                "He won't take charity but he'll take an advance.\"*\n\n"
                "They go back to drilling.\n\n"
                "*\"And note the cart noise. That's useful.\"*"
            ),
            "xp": 35, "zet": 0, "relationship_gain": 8,
            "story_plant": "Rel's network extends to Farmlands. They're tracking the night carts.",
            "arc_connection": "arc1_the_confrontation",
        },

        {
            "id":    "rel_q3",
            "title": "The Training Ground at Night",
            "min_relationship": 20,
            "giver_npc": "captain_rel",
            "type": "investigation",
            "zone_targets": ["town_square"],
            "npc_targets": [],
            "briefing": (
                "*\"Someone has been using the training ground between the second "
                "and third bells. Not my people — my people have the dawn slot.\"*\n\n"
                "They don't look concerned. They look interested.\n\n"
                "*\"The equipment is being used correctly. "
                "I can tell by the wear patterns. "
                "Whoever it is knows what they're doing.\"*\n\n"
                "They hand you a simple task:\n\n"
                "*\"Stay tonight. Find out who.\"*\n\n"
                "They pause.\n\n"
                "*\"Don't confront them. Just observe. "
                "This could be nothing. "
                "It could also be exactly what I'm hoping for.\"*"
            ),
            "objective": "Stake out the Training Grounds at Town Square during the second and third bells. Identify who is training there at night.",
            "completion_line": (
                "Two Council soldiers. Young — both under thirty. "
                "Training hard. Not the performance drills the Council officially runs — "
                "practical work, the kind that prepares someone for actual situations.\n\n"
                "When you tell Rel, they're very still for a moment.\n\n"
                "Then: *\"Which soldiers? What unit?\"*\n\n"
                "You describe their badges.\n\n"
                "Rel almost smiles. It looks unfamiliar on their face.\n\n"
                "*\"Those two have been asking the wrong questions in the barracks for a year. "
                "They transferred to that unit specifically to be closer to — \"*\n\n"
                "They stop.\n\n"
                "*\"Tell them to come to the morning session tomorrow. "
                "Before the others arrive. Tell them Rel says it's time.\"*\n\n"
                "They go back to work.\n\n"
                "*\"Good,\"* they say quietly. *\"They're ready.\"*"
            ),
            "xp": 55, "zet": 0, "relationship_gain": 10,
            "story_plant": "Rel's network includes active Council soldiers who want to defect.",
            "arc_connection": "arc1_the_confrontation",
        },

        {
            "id":    "rel_q4",
            "title": "The Old Names",
            "min_relationship": 32,
            "giver_npc": "captain_rel",
            "type": "investigation",
            "zone_targets": ["ancient_ruins"],
            "npc_targets": ["shade"],
            "briefing": (
                "This one they take longer to ask.\n\n"
                "*\"Eight years ago — before Mercer, before the current Council — "
                "there was a resistance cell. I was — I knew them. "
                "They were betrayed and killed.\"*\n\n"
                "They look at the training yard.\n\n"
                "*\"One of them survived. They went a different direction afterward. "
                "I haven't spoken to them in eight years because I made a choice "
                "that I'm not sure was right, and I don't know how to have that conversation.\"*\n\n"
                "They look at you.\n\n"
                "*\"Go to the Ancient Ruins. Just observe. "
                "Tell me if someone is there. Don't approach them.\"*\n\n"
                "A very long pause.\n\n"
                "*\"Tell me if they look — tell me how they look.\"*"
            ),
            "objective": "Go to the Ancient Ruins. Observe whether someone is there. Report back without approaching.",
            "completion_line": (
                "You describe Shade — what they were doing, "
                "how they stood, what they looked like.\n\n"
                "Rel listens without expression.\n\n"
                "When you finish, they're quiet for a long time.\n\n"
                "*\"Still there.\"*\n\n"
                "Something passes across their face that you can't read.\n\n"
                "*\"I made them wait eight years because I thought we needed more preparation. "
                "More time. A better moment.\"*\n\n"
                "They look at the training yard.\n\n"
                "*\"I wonder sometimes if any moment would have been good enough "
                "or if I was just afraid.\"*\n\n"
                "They straighten.\n\n"
                "*\"When the time comes — and it's coming — "
                "I'm going to need to ask them directly. "
                "I can't send anyone else for that.\"*"
            ),
            "xp": 65, "zet": 0, "relationship_gain": 14,
            "story_plant": "Rel and Shade's history revealed. Rel's guilt established. Connection to Shade's arc.",
            "arc_connection": "arc1_shade_meeting",
        },

        {
            "id":    "rel_q5",
            "title": "The Thirty-Two",
            "min_relationship": 46,
            "giver_npc": "captain_rel",
            "type": "errand",
            "zone_targets": ["residential_ward", "port_district", "farmlands"],
            "npc_targets": [],
            "briefing": (
                "*\"I have thirty-two names. People I've trained over the years. "
                "Some are still in Ironhaven. Some have families now. "
                "Some I haven't spoken to in years.\"*\n\n"
                "They hand you a list.\n\n"
                "*\"I need to know if they're still here. "
                "Not their situation — just if they're still in the city.\"*\n\n"
                "The list is spread across the residential ward, "
                "the port district, the farmlands border.\n\n"
                "*\"Check addresses. You don't need to talk to them. "
                "Just confirm presence.\"*\n\n"
                "They look at the list.\n\n"
                "*\"Thirty-two people who I trained to be ready. "
                "I told them to wait for the right moment.\"*\n\n"
                "A pause.\n\n"
                "*\"They've been waiting for eight years.\"*"
            ),
            "objective": "Check the addresses for the thirty-two names across the Residential Ward, Port District, and Farmlands. Confirm how many are still in Ironhaven.",
            "completion_line": (
                "Twenty-eight of thirty-two are still in the city.\n\n"
                "Three moved away — Rel accepts this.\n\n"
                "One — the name that makes Rel go still when you reach it — "
                "is at the forest operation. Has been for fourteen months.\n\n"
                "When you tell them, they close their eyes briefly.\n\n"
                "*\"Petra.\"*\n\n"
                "They look at the list.\n\n"
                "*\"Twenty-seven. Plus the two Council soldiers. "
                "Plus Harwick if his debt situation resolves.\"*\n\n"
                "They fold the list.\n\n"
                "*\"That's enough. We don't need an army. "
                "We need enough people to make it impossible to ignore.\"*\n\n"
                "They look at you.\n\n"
                "*\"The right moment is when the evidence is ready, "
                "not when the numbers are perfect. "
                "Is the evidence ready?\"*"
            ),
            "xp": 70, "zet": 0, "relationship_gain": 14,
            "story_plant": "Rel's full network established. One of them is in the operation — Petra. Connects to Tomás arc.",
            "arc_connection": "arc1_the_confrontation",
        },

        {
            "id":    "rel_q6",
            "title": "What I Should Have Done",
            "min_relationship": 60,
            "giver_npc": "captain_rel",
            "type": "intervention",
            "zone_targets": ["ancient_ruins"],
            "npc_targets": ["shade"],
            "briefing": (
                "They hand you a folded letter.\n\n"
                "*\"I wrote this four times. "
                "This is the version where I don't explain myself "
                "because explanation isn't what's needed.\"*\n\n"
                "They look at the training yard.\n\n"
                "*\"I chose to wait because I thought we weren't ready. "
                "Eight years ago. The cell — Shade's cell — they were moving. "
                "I thought too soon. I held back the support they were asking for.\"*\n\n"
                "A long pause.\n\n"
                "*\"When they were killed, I told myself it proved I was right — "
                "that they'd moved too fast. I've been telling myself that for eight years.\"*\n\n"
                "They look at you.\n\n"
                "*\"I was wrong. They were ready. I wasn't.\"*\n\n"
                "*\"Take the letter. Find Shade. Give it to them directly. "
                "Stay if they want to talk. Leave if they don't.\"*"
            ),
            "objective": "Deliver Rel's letter to Shade at the Ancient Ruins.",
            "completion_line": (
                "Shade reads the letter without expression.\n\n"
                "When they finish, they fold it carefully "
                "and put it inside their coat.\n\n"
                "They look at you.\n\n"
                "*\"Tell Rel: I know.\"*\n\n"
                "A pause.\n\n"
                "*\"Tell them I've known for eight years and I'm not interested "
                "in the apology. Tell them I'm interested in what comes next.\"*\n\n"
                "They look at the ruins.\n\n"
                "*\"Tell them the right moment is now. "
                "Tell them I'll be there.\"*\n\n"
                "When you tell Rel, they're quiet for a long moment.\n\n"
                "Then: *\"Good.\"*\n\n"
                "They pick up their training equipment.\n\n"
                "*\"Then let's not waste any more time.\"*"
            ),
            "xp": 90, "zet": 0, "relationship_gain": 16,
            "story_plant": "Rel and Shade reconciled. The original resistance reunited.",
            "arc_connection": "arc1_shade_meeting",
        },

        {
            "id":    "rel_q7",
            "title": "Positions",
            "min_relationship": 75,
            "giver_npc": "captain_rel",
            "type": "intervention",
            "zone_targets": ["town_square", "port_district", "residential_ward", "farmlands"],
            "npc_targets": [],
            "briefing": (
                "*\"When we move, people need to be in place before the moment comes. "
                "Not after. Before.\"*\n\n"
                "They spread a hand-drawn map on the training ground wall. "
                "Ironhaven, with positions marked.\n\n"
                "*\"The square — that's the center. People there, visibly, "
                "when the Council is in session. Not armed. Just present.\"*\n\n"
                "They tap four other points.\n\n"
                "*\"Port, residential ward, farmlands border, and here — "
                "people at each point who can pass information and can move quickly.\"*\n\n"
                "They hand you a second, smaller list.\n\n"
                "*\"Tell each of these people: dawn, day after tomorrow. "
                "Their position. Come ready.\"*\n\n"
                "They take down the map.\n\n"
                "*\"No speeches. No explanations. They know what this is.\"*"
            ),
            "objective": "Deliver Rel's instructions to each name on the list at their positions across the city.",
            "completion_line": (
                "Every single person you tell responds the same way: they nod, "
                "they say something like *'I'll be there'* or just *'yes'* or nothing at all — "
                "and they're already moving, already adjusting, already ready.\n\n"
                "When you report back to Rel, they listen to each response.\n\n"
                "When you finish, they're quiet.\n\n"
                "*\"Thirty years of service,\"* they say. *\"The regular kind. "
                "The Council kind. Orders and compliance and don't ask why.\"*\n\n"
                "They look at the training yard.\n\n"
                "*\"This is different. This is people who chose.\"*\n\n"
                "They straighten.\n\n"
                "*\"That's what I've been waiting for. Not numbers. Not timing. "
                "People who chose.\"*"
            ),
            "xp": 100, "zet": 0, "relationship_gain": 18,
            "story_plant": "The network is positioned. The resistance has a physical presence across the city.",
            "arc_connection": "arc1_the_confrontation",
        },

        {
            "id":    "rel_q8",
            "title": "The Morning After",
            "min_relationship": 88,
            "giver_npc": "captain_rel",
            "type": "intervention",
            "zone_targets": ["town_square"],
            "npc_targets": [],
            "briefing": (
                "The morning after the Council votes.\n\n"
                "The portrait is gone from the wall.\n\n"
                "Rel is at the training ground, alone, "
                "doing the same drills they do every morning. "
                "But slower. Not tired — deliberate.\n\n"
                "*\"There's a young woman in the square. "
                "She's been standing there for an hour looking at the wall "
                "where the portrait was.\"*\n\n"
                "They don't stop drilling.\n\n"
                "*\"I think she's from the residential ward. "
                "One of the children who grew up under the portrait. "
                "She doesn't know what a square without it looks like.\"*\n\n"
                "They pause.\n\n"
                "*\"Go talk to her. I don't know what you'll say. "
                "But someone should.\"*"
            ),
            "objective": "Find the young woman in Town Square. Talk to her.",
            "completion_line": (
                "She's nineteen, maybe twenty. Staring at the wall.\n\n"
                "When you approach, she says: "
                "*\"I grew up being told that's just how things are. "
                "That the portrait is there because that's how things are.\"*\n\n"
                "A pause.\n\n"
                "*\"Who took it down?\"*\n\n"
                "You tell her: nobody knows. Or everyone did. Something like that.\n\n"
                "She looks at the bare wall for a long time.\n\n"
                "*\"Is it always going to be like this now?\"*\n\n"
                "You tell her you don't know. But it's different now. That much is certain.\n\n"
                "She nods. Slowly. Then she goes.\n\n"
                "When you tell Rel what she said, they're quiet.\n\n"
                "*\"That's what it costs,\"* they say. "
                "*\"You take down the portrait and then you have to "
                "figure out what to put in its place.\"*\n\n"
                "They resume drilling.\n\n"
                "*\"That's the longer work. "
                "I've been preparing for this part for thirty years. "
                "It turns out I was right that it would take that long.\"*"
            ),
            "xp": 150, "zet": 0, "relationship_gain": 25,
            "story_plant": "Arc 1 aftermath. The harder work of building something begins.",
            "arc_connection": "arc1_ironhaven_chooses",
        },
    ],

    # =========================================================================
    # VEX — quest chains continued in same format
    # The arc: Someone running a cover operation who tests everyone
    # and eventually decides to trust the player with something real.
    # =========================================================================
    "vex": [

        {
            "id":    "vex_q1",
            "title": "The Acquisition",
            "min_relationship": 0,
            "giver_npc": "vex",
            "type": "errand",
            "zone_targets": ["harbour_docks"],
            "npc_targets": [],
            "briefing": (
                "*\"A shipment arrived yesterday. Listed as decorative goods — "
                "third crate, red tag, Dock 5.\"*\n\n"
                "He arranges cards while talking.\n\n"
                "*\"The tax collector catalogs Dock 5 at the third bell. "
                "You have until then.\"*\n\n"
                "He looks up.\n\n"
                "*\"The crate isn't valuable. What's inside it is. "
                "They're not the same thing.\"*\n\n"
                "He goes back to the cards.\n\n"
                "*\"And don't open it.\"*"
            ),
            "objective": "Retrieve the red-tagged crate from Dock 5 at Harbour Docks before the third bell.",
            "completion_line": (
                "He takes the crate without opening it in front of you. "
                "Goes to the back room. Returns without it.\n\n"
                "*\"Good timing.\"*\n\n"
                "He counts out payment.\n\n"
                "*\"Most people ask what's in it.\"*\n\n"
                "He looks at you.\n\n"
                "*\"You didn't.\"*\n\n"
                "He goes back to arranging cards.\n\n"
                "*\"Come back. I'll have something else eventually.\"*"
            ),
            "xp": 30, "zet": 50, "relationship_gain": 5,
            "story_plant": "Vex receives things through unofficial channels. He's testing whether you ask questions.",
            "arc_connection": "arc1_shade_meeting",
        },

        {
            "id":    "vex_q2",
            "title": "The Ruins Survey",
            "min_relationship": 8,
            "giver_npc": "vex",
            "type": "investigation",
            "zone_targets": ["ancient_ruins"],
            "npc_targets": [],
            "briefing": (
                "*\"The north wall of the Ancient Ruins. Third panel from the left.\"*\n\n"
                "He doesn't look up.\n\n"
                "*\"There's a carving. I need a description — not an interpretation, "
                "a description. What you see, exactly, without deciding what it means.\"*\n\n"
                "A pause.\n\n"
                "*\"Most people see something and immediately decide what it is. "
                "That's the problem with most people.\"*"
            ),
            "objective": "Examine the third panel from the left on the north wall of the Ancient Ruins. Describe it accurately.",
            "completion_line": (
                "You describe the carving: a closed eye over a set of scales, "
                "surrounded by a ring of what might be islands or might be waves. "
                "Very old. Very deliberate.\n\n"
                "Vex listens with his eyes closed.\n\n"
                "When you finish: *\"Islands.\"*\n\n"
                "He opens his eyes.\n\n"
                "*\"Did you notice anything else at the ruins?\"*\n\n"
                "His tone hasn't changed but something in the question is different — "
                "more specific than curiosity.\n\n"
                "You describe what else you saw, including whether Shade was there.\n\n"
                "He nods once. Files it.\n\n"
                "*\"The symbol on the wall and the symbol on certain cards in my back display case "
                "are the same symbol. They predate this city by at least three hundred years.\"*\n\n"
                "He picks up a card.\n\n"
                "*\"Someone built a shop in Ironhaven that sells things marked with that symbol. "
                "I'd like to know why.\"*"
            ),
            "xp": 40, "zet": 0, "relationship_gain": 8,
            "story_plant": "Sovereignty symbol is ancient. It predates Mercer. Someone built the card shop around it.",
            "arc_connection": "arc1_shade_meeting",
        },

        {
            "id":    "vex_q3",
            "title": "The Grove Sample",
            "min_relationship": 18,
            "giver_npc": "vex",
            "type": "errand",
            "zone_targets": ["cursed_grove"],
            "npc_targets": [],
            "briefing": (
                "*\"The Cursed Grove. There's a formation of black ore — "
                "not vein material, something different. Darker. Warmer.\"*\n\n"
                "He puts a sealed container on the counter.\n\n"
                "*\"Small piece. Don't touch it with bare hands. "
                "Wrap it in the cloth in the container.\"*\n\n"
                "He looks at you.\n\n"
                "*\"I know what you're thinking.\"*\n\n"
                "He doesn't say what that is.\n\n"
                "*\"The answer is: yes, it's connected. No, I won't explain how yet. "
                "The explanation requires trust I don't extend until it's earned.\"*\n\n"
                "He pushes the container toward you.\n\n"
                "*\"The grove will feel wrong when you're in it. That's accurate. "
                "Stay alert.\"*"
            ),
            "objective": "Retrieve a sample of the unusual black ore formation from the Cursed Grove.",
            "completion_line": (
                "He examines the sample without touching it, "
                "using tools from beneath the counter.\n\n"
                "He's quiet for several minutes.\n\n"
                "Then he puts it in a case alongside the crate contents from Quest 1 — "
                "a card with the closed-eye symbol on the back.\n\n"
                "He sets them side by side.\n\n"
                "*\"The ore in the grove and the ore in the forest operation are "
                "the same compound at different concentrations.\"*\n\n"
                "He looks at you.\n\n"
                "*\"The forest operation isn't mining for trade value. "
                "The ore has a property that someone specifically wants.\"*\n\n"
                "He covers the case.\n\n"
                "*\"I've known about this for eight months. I've been deciding "
                "whether to do anything about it for eight months.\"*\n\n"
                "A pause.\n\n"
                "*\"I think I've decided.\"*"
            ),
            "xp": 55, "zet": 0, "relationship_gain": 12,
            "story_plant": "Vex has been monitoring the ore independently. He's been sitting on intelligence.",
            "arc_connection": "arc1_shade_meeting",
        },

        {
            "id":    "vex_q4",
            "title": "The Question",
            "min_relationship": 30,
            "giver_npc": "vex",
            "type": "intervention",
            "zone_targets": [],
            "npc_targets": [],
            "briefing": (
                "He closes the shop. Locks the door.\n\n"
                "*\"I'm going to ask you something and I need a real answer. "
                "Not a safe answer. Not the answer you think I want.\"*\n\n"
                "He looks at you steadily.\n\n"
                "*\"What do you think is happening in this city? "
                "Not what you've been told. Not the official version. "
                "What do you actually think?\"*\n\n"
                "He waits.\n\n"
                "*\"Everything you say in the next five minutes "
                "determines what I tell you next.\"*"
            ),
            "objective": "Answer Vex honestly. Tell him what you think is happening in Ironhaven.",
            "completion_line": (
                "He listens to your full answer without interrupting.\n\n"
                "When you finish, he's quiet for a moment.\n\n"
                "Then he reaches under the counter and puts a card on the table. "
                "Not from the display case — from below. "
                "The back has the closed-eye symbol.\n\n"
                "*\"The card shop is a front. Has been since I opened it.\"*\n\n"
                "He slides a note across. An address. A time.\n\n"
                "*\"The people meeting there — they've been watching the same things you have. "
                "Some of them longer. They need what you know. "
                "You need what they have.\"*\n\n"
                "He picks up the card.\n\n"
                "*\"The symbol. Closed eye over scales. "
                "The organization that uses it — "
                "Mercer answers to them. They were here before Mercer.\"*\n\n"
                "He puts the card away.\n\n"
                "*\"They'll be here after Mercer, unless someone decides otherwise.\"*"
            ),
            "xp": 70, "zet": 0, "relationship_gain": 18,
            "story_plant": "Vex reveals the card shop is a resistance cover. First explicit resistance contact.",
            "arc_connection": "arc1_shade_meeting",
        },

        {
            "id":    "vex_q5",
            "title": "The Back Inventory",
            "min_relationship": 46,
            "giver_npc": "vex",
            "type": "errand",
            "zone_targets": ["ancient_ruins", "cursed_grove"],
            "npc_targets": [],
            "briefing": (
                "*\"There are two items I need. They're not in stock. "
                "They're not for sale.\"*\n\n"
                "He puts two sketches on the counter — "
                "objects that look like cards but thicker, older, different material.\n\n"
                "*\"Pre-Ironhaven artifacts. The ruins and the grove "
                "both have sections I haven't been able to survey personally.\"*\n\n"
                "He looks at the sketches.\n\n"
                "*\"The first is at the Ancient Ruins — sealed alcove, "
                "east wall, below the main carvings. "
                "The second is at the grove center, inside the stone ring.\"*\n\n"
                "He covers the sketches.\n\n"
                "*\"These predate the Sovereignty. Which means they predate "
                "whatever the Sovereignty was before it was the Sovereignty.\"*\n\n"
                "He looks at you.\n\n"
                "*\"That's useful.\"*"
            ),
            "objective": "Retrieve two artifacts — one from the Ancient Ruins sealed alcove, one from the Cursed Grove stone ring center.",
            "completion_line": (
                "He examines both without touching them, using the same tools as before.\n\n"
                "Very quietly: *\"These are navigation instruments.\"*\n\n"
                "He looks up.\n\n"
                "*\"Not maps. Instructions. How to find something "
                "by using the ore formations as reference points.\"*\n\n"
                "He puts them in the case with the other items.\n\n"
                "*\"The ore is a compass. The grove and the forest and the caves — "
                "they form a pattern. Someone laid that pattern down "
                "before this island was settled.\"*\n\n"
                "He closes the case.\n\n"
                "*\"The Sovereignty isn't mining the ore. "
                "They're following a path someone laid down a long time ago.\"*\n\n"
                "He looks at you.\n\n"
                "*\"And we're standing in the middle of it.\"*"
            ),
            "xp": 80, "zet": 0, "relationship_gain": 14,
            "story_plant": "Void Century breadcrumb. The ore is ancient navigation. The Sovereignty is following old instructions.",
            "arc_connection": "arc1_shade_truth",
        },

        {
            "id":    "vex_q6",
            "title": "The Cards",
            "min_relationship": 60,
            "giver_npc": "vex",
            "type": "errand",
            "zone_targets": ["residential_ward", "port_district"],
            "npc_targets": [],
            "briefing": (
                "He puts two envelopes on the counter.\n\n"
                "*\"Deliver these. The addresses are on the front. "
                "Don't open them. Don't tell anyone where you got them.\"*\n\n"
                "He goes back to arranging the display case.\n\n"
                "*\"One is for a sailor in the port district. "
                "One is for a woman in the residential ward.\"*\n\n"
                "He pauses.\n\n"
                "*\"They've both been watching the same things we have. "
                "Independently. Without knowing about each other.\"*\n\n"
                "He selects a card from the case with care.\n\n"
                "*\"The envelopes tell them they're not alone. "
                "That's the whole message.\"*\n\n"
                "He looks up.\n\n"
                "*\"Turns out that's enough.\"*"
            ),
            "objective": "Deliver Vex's envelopes to the addresses in the Port District and Residential Ward.",
            "completion_line": (
                "The sailor reads the envelope on the dock. Looks up at you. "
                "Nods once. *\"Tell him: ready.\"*\n\n"
                "The woman in the ward reads hers inside, door half-closed. "
                "Then she opens it fully. *\"Tell him I have something. "
                "Something he'll want. Tell him to come.\"*\n\n"
                "When you tell Vex, he writes both responses in a small notebook.\n\n"
                "He looks at what he's written.\n\n"
                "*\"Forty-three cards in my display case,\"* he says. "
                "*\"Each one takes months to find. I verify them carefully. "
                "I don't sell the ones that aren't right.\"*\n\n"
                "He closes the notebook.\n\n"
                "*\"This is the same work. Finding the right people. "
                "Verifying them. Waiting for the hand to be complete.\"*\n\n"
                "He looks at you.\n\n"
                "*\"The hand is complete.\"*"
            ),
            "xp": 80, "zet": 0, "relationship_gain": 14,
            "story_plant": "Vex's network completes. He's been building this the same way he builds his card inventory.",
            "arc_connection": "arc1_the_confrontation",
        },

        {
            "id":    "vex_q7",
            "title": "What the Symbol Means",
            "min_relationship": 74,
            "giver_npc": "vex",
            "type": "investigation",
            "zone_targets": ["ancient_ruins"],
            "npc_targets": ["shade"],
            "briefing": (
                "*\"The closed-eye symbol. I've spent eight months researching it.\"*\n\n"
                "He opens the case — all the items together: "
                "the ore sample, the artifacts, the card, the crate contents.\n\n"
                "*\"I know what the Sovereignty is. "
                "I know what they want the ore for. "
                "I don't know the timeline.\"*\n\n"
                "He looks at you.\n\n"
                "*\"Shade knows the timeline. They were close to it eight years ago. "
                "When the cell was killed, Shade would have kept whatever they found.\"*\n\n"
                "He closes the case.\n\n"
                "*\"Go to the ruins. Tell Shade what I have. "
                "Ask what they know about the timeline. "
                "Tell them I'm asking — they'll know what that means.\"*\n\n"
                "A pause.\n\n"
                "*\"They'll probably come here themselves after. "
                "That's fine. I've been expecting that conversation.\"*"
            ),
            "objective": "Tell Shade what Vex has found. Ask about the Sovereignty's timeline. Report back.",
            "completion_line": (
                "Shade listens to everything without moving.\n\n"
                "Then: *\"Vex has been running the card shop as a front since two months "
                "after I took Mercer's offer. I knew. I let it run because if I "
                "reported it, the evidence they were building would disappear.\"*\n\n"
                "They look at you.\n\n"
                "*\"Tell them: eighteen months from the date on the third Sovereignty letter "
                "in Mercer's archive. That's the decommission date.\"*\n\n"
                "They hand you a small piece of paper.\n\n"
                "*\"That's my calculation. I've had it for three months. "
                "I didn't know who to give it to.\"*\n\n"
                "When you bring the paper to Vex, he looks at the date.\n\n"
                "He's quiet for a long time.\n\n"
                "*\"Four months.\"*\n\n"
                "He looks at you.\n\n"
                "*\"Then we're not building anymore. We're moving.\"*"
            ),
            "xp": 100, "zet": 0, "relationship_gain": 18,
            "story_plant": "Timeline established. Four months. Vex and Shade connect. Urgency confirmed.",
            "arc_connection": "arc1_shade_truth",
        },

        {
            "id":    "vex_q8",
            "title": "The Display Case",
            "min_relationship": 85,
            "giver_npc": "vex",
            "type": "intervention",
            "zone_targets": ["town_square"],
            "npc_targets": [],
            "briefing": (
                "The morning after the vote.\n\n"
                "Vex is rearranging the display case.\n\n"
                "*\"I'm making space.\"*\n\n"
                "He doesn't elaborate. Then:\n\n"
                "*\"Before this — before what just happened — "
                "this was a front. The cards were real, the shop was real, "
                "but the purpose was elsewhere.\"*\n\n"
                "He puts a card in the center position of the display. "
                "The one with the closed-eye symbol on the back. "
                "Face up, for the first time, visible to anyone walking past.\n\n"
                "*\"I'd like to keep the shop open. "
                "As an actual shop. Not a front.\"*\n\n"
                "He looks at you.\n\n"
                "*\"The square is different today. Go look at it. "
                "Tell me what you see.\"*"
            ),
            "objective": "Go to Town Square. Observe the difference. Return and tell Vex what you see.",
            "completion_line": (
                "The square without the portrait. People moving differently. "
                "The particular atmosphere of a city that has done something "
                "and doesn't quite know what happens next.\n\n"
                "When you describe it to Vex, he listens carefully.\n\n"
                "*\"The space where the portrait was,\"* he says. "
                "*\"What's there?\"*\n\n"
                "Just the wall.\n\n"
                "He nods.\n\n"
                "*\"Good. Empty is the right starting point.\"*\n\n"
                "He turns back to the display case.\n\n"
                "*\"I've been running a cover operation for eight months. "
                "I'm good at it. I know what to say and what not to say "
                "and when to let silence do the work.\"*\n\n"
                "He straightens a card.\n\n"
                "*\"I'm going to try being a shopkeeper now. "
                "Apparently I'm good at that too.\"*\n\n"
                "He looks at the symbol-back card in the center of the case.\n\n"
                "*\"Not a secret anymore. Just a card.\"*"
            ),
            "xp": 150, "zet": 0, "relationship_gain": 25,
            "story_plant": "Vex chooses to stay. The card shop becomes real. The symbol becomes public.",
            "arc_connection": "arc1_ironhaven_chooses",
        },
    ],

    # =========================================================================
    # BORA
    # The arc: The cheerful one. Everyone thinks she's just friendly.
    # She's been keeping this city alive by herself for three years.
    # =========================================================================
    "bora": [

        {
            "id":    "bora_q1",
            "title": "Maren's Message",
            "min_relationship": 0,
            "giver_npc": "bora",
            "type": "errand",
            "zone_targets": ["port_district"],
            "npc_targets": ["maren"],
            "briefing": (
                "She hands you a folded note while pulling someone else's drink "
                "with the other hand.\n\n"
                "*\"For Maren. She hasn't been in this week — "
                "which means she's either buried in manifests or "
                "she found something that's got her stuck. "
                "Either way, she needs to eat.\"*\n\n"
                "She adds a wrapped package to the note.\n\n"
                "*\"She'll say she's fine and she doesn't need it. "
                "Put it on her desk and leave before she can give it back.\"*"
            ),
            "objective": "Deliver Bora's note and food to Maren at the Harbour Office. Don't take no for an answer.",
            "completion_line": (
                "Maren takes the package before she can stop herself, "
                "already unwrapping it before she starts to say she doesn't need it.\n\n"
                "She reads the note. Something softens in her face for a moment.\n\n"
                "*\"Tell her — tell her the coffee was the right temperature last time. "
                "That she knows how I like it.\"*\n\n"
                "When you tell Bora, she grins.\n\n"
                "*\"That's Maren for 'thank you and I love you.'\"*\n\n"
                "She refills your drink.\n\n"
                "*\"She's been keeping track of every ship that moves through that harbour "
                "for three years. I feed her so she doesn't forget to eat.\"*\n\n"
                "She says it simply. Like it's just the arrangement.\n\n"
                "*\"We all do what we can.\"*"
            ),
            "xp": 25, "zet": 30, "relationship_gain": 5,
            "story_plant": "Bora maintains people. She's been the informal support network for three years.",
            "arc_connection": "arc1_ironhaven_chooses",
        },

        {
            "id":    "bora_q2",
            "title": "The Hungry Family",
            "min_relationship": 8,
            "giver_npc": "bora",
            "type": "errand",
            "zone_targets": ["residential_ward"],
            "npc_targets": [],
            "briefing": (
                "She lowers her voice, which is rare for Bora.\n\n"
                "*\"There's a family in the residential ward — "
                "three kids, parents both on double shifts since the rate hike. "
                "I've been sending things but I can't get away tonight.\"*\n\n"
                "She hands over a covered basket.\n\n"
                "*\"Don't tell them it's from me. "
                "They'll refuse it if they think it's charity.\"*\n\n"
                "She goes back to normal volume.\n\n"
                "*\"Tell them it's from a regular who didn't finish their order. "
                "They know that's not true. They'll accept it anyway "
                "because they have three kids.\"*"
            ),
            "objective": "Deliver the basket to the family in the Residential Ward without revealing it's from Bora.",
            "completion_line": (
                "The older child opens the door. Looks at the basket. Looks at you.\n\n"
                "*\"Tell Bora thank you. She always thinks we don't know it's her.\"*\n\n"
                "When you tell Bora, she laughs — the real kind, surprised.\n\n"
                "*\"Of course they know. They've known for a year.\"*\n\n"
                "She wipes down the bar.\n\n"
                "*\"I know they know. They know I know they know. "
                "We all keep the fiction going because it makes it easier.\"*\n\n"
                "She looks at the bar.\n\n"
                "*\"This city runs on things that are easier. "
                "The forty percent. The portraits. The official version of everything. "
                "All of it easier than the truth.\"*\n\n"
                "A beat.\n\n"
                "*\"I wonder sometimes how much energy we all spend "
                "keeping the easier version going.\"*"
            ),
            "xp": 30, "zet": 0, "relationship_gain": 8,
            "story_plant": "The city survives on maintained fictions. Bora sees through all of them.",
            "arc_connection": "arc1_ironhaven_chooses",
        },

        {
            "id":    "bora_q3",
            "title": "What the Soldiers Said",
            "min_relationship": 18,
            "giver_npc": "bora",
            "type": "investigation",
            "zone_targets": ["smugglers_trail"],
            "npc_targets": [],
            "briefing": (
                "*\"A Council sergeant had seven drinks on Tuesday and said something "
                "about an ore extraction quota being behind schedule. "
                "I wrote it down. I write most things down.\"*\n\n"
                "She shows you the note briefly — two sentences in her neat handwriting, "
                "then she puts it away.\n\n"
                "*\"The quota they're behind on — they're going to push harder to meet it. "
                "Which means more night cart runs.\"*\n\n"
                "She slides you a drink.\n\n"
                "*\"Go check the Smuggler's Trail. Count the ruts. "
                "If they're pushing harder, the ruts will be fresher and more numerous.\"*\n\n"
                "She looks at you.\n\n"
                "*\"I've been counting things people say when they drink for three years. "
                "You'd be surprised what a person says when they feel safe.\"*"
            ),
            "objective": "Check the Smuggler's Trail for evidence of increased cart activity.",
            "completion_line": (
                "Heavier than last time. Deeper ruts, more of them, some overlapping — "
                "multiple trips in close succession.\n\n"
                "When you tell Bora, she writes it in her small notebook.\n\n"
                "*\"They're rushing.\"*\n\n"
                "She thinks.\n\n"
                "*\"Rushing means mistakes. Rushing means people get hurt faster. "
                "Rushing means they don't have as much time as they thought.\"*\n\n"
                "She closes the notebook.\n\n"
                "*\"I have — I have a lot of notes. Three years of conversations. "
                "What Council soldiers complain about when they're drunk, "
                "what dock workers say when they're scared, "
                "what the people from the forest operation don't say "
                "when they come in here looking like that.\"*\n\n"
                "She looks at you.\n\n"
                "*\"I've been waiting for someone who could use them.\"*"
            ),
            "xp": 50, "zet": 0, "relationship_gain": 10,
            "story_plant": "Bora has been systematically collecting intelligence for three years.",
            "arc_connection": "arc1_the_confrontation",
        },

        {
            "id":    "bora_q4",
            "title": "The Notes",
            "min_relationship": 30,
            "giver_npc": "bora",
            "type": "errand",
            "zone_targets": ["port_district", "town_square"],
            "npc_targets": ["maren", "captain_rel"],
            "briefing": (
                "She brings out a folder from under the bar.\n\n"
                "*\"Three years. Everything I've heard that mattered.\"*\n\n"
                "She holds it.\n\n"
                "*\"I can't use this myself. I'm the barkeep. "
                "If I do something with this information, "
                "the tavern becomes a known resistance point "
                "and I lose my ability to collect anything.\"*\n\n"
                "She hands it over.\n\n"
                "*\"Take the first section to Maren — shipping and cargo. "
                "Take the second section to Rel — Council military movements. "
                "Keep the third section. It's about everything else, "
                "and I think you'll know what to do with it.\"*\n\n"
                "She straightens.\n\n"
                "*\"And don't get caught with it. "
                "This represents three years of a woman who listens well.\"*"
            ),
            "objective": "Deliver the relevant sections of Bora's intelligence notes to Maren and Captain Rel.",
            "completion_line": (
                "Maren reads her section and immediately cross-references "
                "three of her manifest dates. *\"This confirms it.\"*\n\n"
                "Rel reads their section without expression, "
                "then: *\"There's a patrol pattern in here I haven't seen documented before. "
                "This changes the timing.\"*\n\n"
                "When you return to Bora:\n\n"
                "*\"Useful?\"*\n\n"
                "Very.\n\n"
                "She nods.\n\n"
                "*\"I once heard a philosopher — someone passing through, "
                "years ago, before all of this — say that information is the only currency "
                "that doesn't devalue when you spend it.\"*\n\n"
                "She pours herself a small drink. The first time you've seen her do that.\n\n"
                "*\"I've been spending mine carefully. "
                "I think now is the right time to spend it all.\"*"
            ),
            "xp": 65, "zet": 0, "relationship_gain": 14,
            "story_plant": "Bora's full intelligence passed to Maren and Rel. Three networks converge.",
            "arc_connection": "arc1_the_confrontation",
        },

        {
            "id":    "bora_q5",
            "title": "The Addresses",
            "min_relationship": 44,
            "giver_npc": "bora",
            "type": "intervention",
            "zone_targets": ["residential_ward", "port_district", "farmlands"],
            "npc_targets": [],
            "briefing": (
                "She hands you a list.\n\n"
                "*\"There are people in this city who are going to need somewhere to go. "
                "When things change — and they're going to change — "
                "some of them won't be safe where they are.\"*\n\n"
                "She's serious in a way that looks unfamiliar on her.\n\n"
                "*\"Workers' families. People who've been vocal. "
                "People whose loved ones are in the operation.\"*\n\n"
                "She taps the list.\n\n"
                "*\"Go to each address. Just knock. Say: 'Bora knows where it's safe.' "
                "See what they say.\"*\n\n"
                "She goes back to the bar.\n\n"
                "*\"I've been keeping this list for a year. "
                "I just needed something to point them toward. "
                "Now I do.\"*"
            ),
            "objective": "Visit each address on Bora's list. Deliver her message.",
            "completion_line": (
                "Every door. Every address.\n\n"
                "The woman in the residential ward who has two children and "
                "a husband in the forest operation — she starts crying before you finish the sentence. "
                "*\"Tell her yes. Tell her please. Tell her we've been waiting.\"*\n\n"
                "The former dock worker at the port — "
                "*\"I know three others. Can I bring them?\"*\n\n"
                "The farmer at the Farmlands border, alone, careful — "
                "*\"How do I know this is real?\"* You tell him what you know. "
                "He looks at you for a long time. *\"Alright.\"*\n\n"
                "When you return to Bora, she writes each confirmation down.\n\n"
                "When the list is full, she puts it away.\n\n"
                "*\"I've been feeding people and listening to people and "
                "keeping track of people for three years,\"* she says quietly. "
                "*\"Not because someone asked me to. "
                "Just because someone had to.\"*\n\n"
                "She looks at the bar.\n\n"
                "*\"Turns out that's the work. "
                "Not the dramatic kind. "
                "Just the keeping going kind.\"*"
            ),
            "xp": 80, "zet": 0, "relationship_gain": 16,
            "story_plant": "Bora's safe network activated. She's been maintaining this city by herself.",
            "arc_connection": "arc1_ironhaven_chooses",
        },

        {
            "id":    "bora_q6",
            "title": "The Council Sergeant",
            "min_relationship": 58,
            "giver_npc": "bora",
            "type": "investigation",
            "zone_targets": ["port_district"],
            "npc_targets": [],
            "briefing": (
                "*\"The sergeant who talks too much when he drinks — "
                "he's in tonight. Third stool. He's already on his second.\"*\n\n"
                "She doesn't look at you.\n\n"
                "*\"I need the name of the Sovereignty contact in Ironhaven. "
                "Not Mercer — above Mercer. The person Mercer reports to locally.\"*\n\n"
                "She wipes down the bar.\n\n"
                "*\"He mentioned 'the liaison' three weeks ago and then changed the subject "
                "when he noticed I was nearby. He's careless but not stupid.\"*\n\n"
                "She slides a drink toward the end of the bar.\n\n"
                "*\"He likes to feel like he's the most important person in the room. "
                "Give him someone who thinks he is. "
                "See what he says.\"*"
            ),
            "objective": "Get the Council sergeant talking at the Port District tavern. Find out who the Sovereignty's local liaison is.",
            "completion_line": (
                "It takes an hour and four drinks but he gets there.\n\n"
                "The liaison. A name you haven't heard before — "
                "not a Council official, not a merchant, "
                "a name attached to an import-export company that arrived "
                "in Ironhaven two years ago and mostly seems to do paperwork.\n\n"
                "When you tell Bora, she writes the name without reacting.\n\n"
                "Then: *\"That company has an office in the Council district. "
                "I've walked past it a hundred times.\"*\n\n"
                "She looks at the name.\n\n"
                "*\"It's always the ones who seem like paperwork.\"*\n\n"
                "She puts the note in her folder.\n\n"
                "*\"This is the piece Maren needed. "
                "The name that connects the manifests to the organization.\"*\n\n"
                "She looks at you.\n\n"
                "*\"We have everything now. Don't we?\"*"
            ),
            "xp": 90, "zet": 0, "relationship_gain": 16,
            "story_plant": "Local Sovereignty liaison identified. The final connection in the evidence chain.",
            "arc_connection": "arc1_the_confrontation",
        },

        {
            "id":    "bora_q7",
            "title": "The Night Before",
            "min_relationship": 72,
            "giver_npc": "bora",
            "type": "errand",
            "zone_targets": ["residential_ward", "town_square", "port_district"],
            "npc_targets": [],
            "briefing": (
                "The night before everything.\n\n"
                "The tavern is quieter than usual — people sense something, "
                "even if they don't know what.\n\n"
                "*\"I have three deliveries. Not food this time.\"*\n\n"
                "She hands you three small sealed envelopes.\n\n"
                "*\"One for the family in the ward — their person comes out tomorrow. "
                "They need to know to be ready.\"*\n\n"
                "*\"One for the dock crew that's been watching the night boats — "
                "they've been waiting for a signal. This is it.\"*\n\n"
                "*\"One for the young woman in the square — "
                "the one who grew up under the portrait. "
                "She needs to know it's alright to be in the square tomorrow.\"*\n\n"
                "She looks at the three envelopes.\n\n"
                "*\"Three years of this and it comes down to three envelopes "
                "the night before.\"*\n\n"
                "She almost laughs.\n\n"
                "*\"Go on. And come back after. I'll have something warm.\"*"
            ),
            "objective": "Deliver Bora's three envelopes before midnight.",
            "completion_line": (
                "All three received.\n\n"
                "The family in the ward: the mother holds the envelope "
                "before opening it. When she reads it, she sits very still. "
                "Then: *\"Tomorrow.\"* Like she's trying the word on.\n\n"
                "The dock crew: they read it together, quickly. "
                "One of them looks up at the night sky. "
                "*\"Finally.\"*\n\n"
                "The young woman in the square — she reads it twice. "
                "Folds it carefully. *\"Tell her I'll be there.\"*\n\n"
                "When you return to Bora, the tavern is empty. "
                "She's made something warm. She sits across from you.\n\n"
                "*\"I've been the person who keeps things going,\"* she says. "
                "*\"The person people come to when they need somewhere to be. "
                "I like that. I chose it.\"*\n\n"
                "She looks at the fire.\n\n"
                "*\"Tomorrow it might be something different. "
                "Better, probably. Still work.\"*\n\n"
                "She raises her cup.\n\n"
                "*\"To all the people who kept going when it was just the "
                "keeping going that mattered.\"*"
            ),
            "xp": 100, "zet": 0, "relationship_gain": 18,
            "story_plant": "Bora's full arc. The city's informal support network made the arc possible.",
            "arc_connection": "arc1_ironhaven_chooses",
        },

        {
            "id":    "bora_q8",
            "title": "The Day After",
            "min_relationship": 85,
            "giver_npc": "bora",
            "type": "errand",
            "zone_targets": ["residential_ward", "farmlands", "fishermans_cove"],
            "npc_targets": [],
            "briefing": (
                "The tavern is full. The loudest it's been in years.\n\n"
                "Bora is in constant motion — refilling, remembering orders, "
                "laughing at things, touching people's shoulders.\n\n"
                "When she gets a moment:\n\n"
                "*\"Three people who were part of last night — "
                "they weren't in the square. They didn't see it.\"*\n\n"
                "She hands you three small notes.\n\n"
                "*\"Harwick at the farmlands, the fishing family at the cove, "
                "and old Petra — she came out of the forest operation two days ago, "
                "she's at the residential ward, she hasn't left the room yet.\"*\n\n"
                "She looks at the notes.\n\n"
                "*\"Tell them what happened. In person. "
                "The city changed yesterday and not everyone knows yet.\"*\n\n"
                "She goes back to work.\n\n"
                "*\"Some news is better told by someone who was there.\"*"
            ),
            "objective": "Tell Harwick, the fishing family at the Cove, and Petra in the Residential Ward what happened in the square.",
            "completion_line": (
                "Harwick listens to the whole thing. "
                "When you finish, he looks at his fields.\n\n"
                "*\"Forty percent,\"* he says. *\"Think they'll change the rate?\"*\n\n"
                "You don't know. But it's possible now in a way it wasn't yesterday.\n\n"
                "He nods. *\"That's enough for today.\"*\n\n"
                "The fishing family hears it together on the dock. "
                "The grandmother says nothing but looks at the sea "
                "for a long time with an expression you can't read.\n\n"
                "Petra — she's in a small room, hands still dark from the ore, "
                "Tomás's bread on the table beside her. "
                "She listens to everything. When you finish:\n\n"
                "*\"Did they vote?\"*\n\n"
                "Six to one.\n\n"
                "She closes her eyes.\n\n"
                "When you return to Bora and describe each reaction, "
                "she listens carefully.\n\n"
                "Then: *\"That's the real thing,\"* she says. "
                "*\"Not the portrait coming down. "
                "Harwick asking about the forty percent. "
                "The grandmother looking at the sea. "
                "Petra closing her eyes.\"*\n\n"
                "She looks at the full tavern.\n\n"
                "*\"The big moment was yesterday. "
                "The real thing is today and tomorrow and the day after. "
                "The real thing is people being able to think about the future again.\"*\n\n"
                "She refills your cup.\n\n"
                "*\"Welcome to the real thing.\"*"
            ),
            "xp": 150, "zet": 0, "relationship_gain": 25,
            "story_plant": "Arc 1 complete. Bora's arc ends with the city beginning the harder work.",
            "arc_connection": "arc1_ironhaven_chooses",
        },
    ],
}