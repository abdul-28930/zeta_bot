import asyncio
import asyncpg

async def test():
    conn = await asyncpg.connect("postgresql://postgres:YOURPASSWORD@db.zfgjlztyzdxpdywgrree.supabase.co:5432/postgres")
    print("Connected!")
    await conn.close()

asyncio.run(test())