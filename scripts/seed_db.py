"""
Database seeder for Zeta.

Run this ONCE after your first deployment:
    python scripts/seed_db.py

This verifies your DB connection and ensures tables exist.
World data (races, classes, cards, zones, NPCs, enemies) is stored in-memory
in game/data.py. Player data is stored in the database.
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


async def main() -> None:
    print("🌊  Zeta Database Setup")
    print("=" * 40)

    # Test DB connection
    print("Connecting to database...")
    from core.database import init_db, engine

    try:
        await init_db()
        print("✅  Database tables created/verified.")
    except Exception as e:
        print(f"❌  Database error: {e}")
        sys.exit(1)

    # Test Redis connection
    print("Connecting to Redis...")
    from core.cache import init_redis, get_redis

    try:
        redis = await init_redis()
        await redis.ping()
        print("✅  Redis connection verified.")
    except Exception as e:
        print(f"❌  Redis error: {e}")
        sys.exit(1)

    # Print world data summary
    from game.data import RACES, CLASSES, CARDS, ZONES, NPCS, ENEMIES, ITEMS, SHOPS

    print("\n📊  World Data Summary:")
    print(f"  Races:    {len(RACES)}")
    print(f"  Classes:  {len(CLASSES)}")
    print(f"  Cards:    {len(CARDS)}")
    print(f"  Zones:    {len(ZONES)}")
    print(f"  NPCs:     {len(NPCS)}")
    print(f"  Enemies:  {len(ENEMIES)}")
    print(f"  Items:    {len(ITEMS)}")
    print(f"  Shops:    {len(SHOPS)}")

    print("\n✅  Setup complete. Run `python main.py` to start the bot.")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
