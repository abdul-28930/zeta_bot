from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


def utcnow():
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Player core
# ---------------------------------------------------------------------------

class Player(Base):
    __tablename__ = "players"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    discord_name: Mapped[str] = mapped_column(String(64))
    character_name: Mapped[str | None] = mapped_column(String(32), nullable=True)
    race_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    class_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    subclass_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    char_created: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    stats: Mapped["PlayerStats"] = relationship("PlayerStats", back_populates="player", uselist=False, lazy="joined")
    progression: Mapped["PlayerProgression"] = relationship("PlayerProgression", back_populates="player", uselist=False, lazy="joined")
    flags: Mapped[list["PlayerFlag"]] = relationship("PlayerFlag", back_populates="player", lazy="select")


class PlayerStats(Base):
    __tablename__ = "player_stats"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.user_id"), primary_key=True)
    strength: Mapped[int] = mapped_column(Integer, default=5)
    defense: Mapped[int] = mapped_column(Integer, default=5)
    agility: Mapped[int] = mapped_column(Integer, default=5)
    intel: Mapped[int] = mapped_column(Integer, default=5)
    vit: Mapped[int] = mapped_column(Integer, default=5)
    lck: Mapped[int] = mapped_column(Integer, default=1)
    unspent_points: Mapped[int] = mapped_column(Integer, default=0)

    player: Mapped["Player"] = relationship("Player", back_populates="stats")

    @property
    def max_hp(self) -> int:
        return self.vit * 5

    def to_dict(self) -> dict:
        return {
            "str": self.strength,
            "def": self.defense,
            "agi": self.agility,
            "int": self.intel,
            "vit": self.vit,
            "lck": self.lck,
        }


class PlayerProgression(Base):
    __tablename__ = "player_progression"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.user_id"), primary_key=True)
    level: Mapped[int] = mapped_column(Integer, default=1)
    xp: Mapped[int] = mapped_column(Integer, default=0)
    zet_wallet: Mapped[int] = mapped_column(Integer, default=100)
    current_hp: Mapped[int] = mapped_column(Integer, default=25)
    current_zone_id: Mapped[str] = mapped_column(String(64), default="town_square")
    current_building_id: Mapped[str | None] = mapped_column(String(64), nullable=True)

    player: Mapped["Player"] = relationship("Player", back_populates="progression")

    def xp_to_next(self) -> int:
        thresholds = [0, 200, 500, 1000, 2000, 3500, 5000, 7500, 10000, 15000, 20000]
        lvl = min(self.level, len(thresholds) - 1)
        return thresholds[lvl]


class PlayerFlag(Base):
    __tablename__ = "player_flags"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.user_id"), primary_key=True)
    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    value: Mapped[str | None] = mapped_column(Text, nullable=True)

    player: Mapped["Player"] = relationship("Player", back_populates="flags")


# ---------------------------------------------------------------------------
# Inventory & Bank
# ---------------------------------------------------------------------------

class PlayerInventory(Base):
    __tablename__ = "player_inventory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.user_id"))
    item_id: Mapped[str] = mapped_column(String(64))
    quantity: Mapped[int] = mapped_column(Integer, default=1)


class PlayerCardCollection(Base):
    __tablename__ = "player_card_collection"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.user_id"))
    card_id: Mapped[str] = mapped_column(String(64))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    level: Mapped[int] = mapped_column(Integer, default=1)  # auto-levels with player level
    obtained_from: Mapped[str | None] = mapped_column(String(32), nullable=True)


class PlayerDeck(Base):
    __tablename__ = "player_deck"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.user_id"), primary_key=True)
    card_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)


class PlayerBank(Base):
    __tablename__ = "player_bank"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.user_id"), primary_key=True)
    zet_balance: Mapped[int] = mapped_column(BigInteger, default=0)
    vault_slots: Mapped[int] = mapped_column(Integer, default=50)
    last_interest_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class BankVault(Base):
    __tablename__ = "bank_vault"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.user_id"))
    item_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    card_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)


# ---------------------------------------------------------------------------
# NPC Relationship & Dialogue
# ---------------------------------------------------------------------------

class NPCRelationship(Base):
    __tablename__ = "npc_relationships"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.user_id"), primary_key=True)
    npc_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    visit_count: Mapped[int] = mapped_column(Integer, default=0)
    relationship_score: Mapped[int] = mapped_column(Integer, default=0)
    shared_details: Mapped[dict] = mapped_column(JSONB, default=dict)
    first_met_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    @property
    def relationship_level(self) -> str:
        score = self.relationship_score
        if score < 10:   return "Stranger"
        elif score < 30: return "Acquaintance"
        elif score < 60: return "Friendly"
        elif score < 90: return "Trusted"
        else:            return "Beloved"


class DialogueTurn(Base):
    __tablename__ = "dialogue_turns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.user_id"))
    npc_id: Mapped[str] = mapped_column(String(64))
    role: Mapped[str] = mapped_column(String(16))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


# ---------------------------------------------------------------------------
# Storylet progress
# ---------------------------------------------------------------------------

class PlayerStoryletProgress(Base):
    __tablename__ = "player_storylet_progress"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.user_id"), primary_key=True)
    storylet_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    status: Mapped[str] = mapped_column(String(32), default="active")
    choice_made: Mapped[str | None] = mapped_column(String(64), nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


# ---------------------------------------------------------------------------
# Quests
# ---------------------------------------------------------------------------

class PlayerQuest(Base):
    __tablename__ = "player_quests"

    user_id:      Mapped[int] = mapped_column(BigInteger, ForeignKey("players.user_id"), primary_key=True)
    quest_id:     Mapped[str] = mapped_column(String(64), primary_key=True)
    npc_id:       Mapped[str] = mapped_column(String(64))
    status:       Mapped[str] = mapped_column(String(16), default="offered")
    progress:     Mapped[dict] = mapped_column(JSONB, default=dict)
    started_at:   Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


# ---------------------------------------------------------------------------
# Market
# ---------------------------------------------------------------------------

class MarketListing(Base):
    __tablename__ = "market_listings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    seller_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.user_id"))
    item_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    card_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    listing_fee_paid: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(16), default="active")
    listed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    buyer_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    @property
    def price_per(self) -> int:
        return self.price // max(self.quantity, 1)

    def is_expired(self) -> bool:
        if not self.expires_at:
            return False
        return datetime.now(timezone.utc) >= self.expires_at


# ---------------------------------------------------------------------------
# Adventurer's Guild
# ---------------------------------------------------------------------------

class GuildContract(Base):
    __tablename__ = "guild_contracts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    day_key: Mapped[str] = mapped_column(String(10))
    tier: Mapped[str] = mapped_column(String(8))
    contract_type: Mapped[str] = mapped_column(String(32))
    target_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    target_count: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    reward_xp: Mapped[int] = mapped_column(Integer)
    reward_zet: Mapped[int] = mapped_column(Integer)


class PlayerGuildContract(Base):
    __tablename__ = "player_guild_contracts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.user_id"))
    contract_id: Mapped[int] = mapped_column(Integer, ForeignKey("guild_contracts.id"))
    progress: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(16), default="active")
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    claimed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


# ---------------------------------------------------------------------------
# Gathering System
# ---------------------------------------------------------------------------

class PlayerGatheringSkill(Base):
    """Tracks each gathering skill level + XP per player."""
    __tablename__ = "player_gathering_skills"

    user_id:    Mapped[int] = mapped_column(BigInteger, ForeignKey("players.user_id"), primary_key=True)
    skill_type: Mapped[str] = mapped_column(String(32), primary_key=True)
    level:      Mapped[int] = mapped_column(Integer, default=1)
    xp:         Mapped[int] = mapped_column(Integer, default=0)


class PlayerEquipment(Base):
    """Stores which tool item is currently equipped in each tool slot."""
    __tablename__ = "player_equipment"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.user_id"), primary_key=True)
    slot:    Mapped[str] = mapped_column(String(32), primary_key=True)
    item_id: Mapped[str] = mapped_column(String(64))