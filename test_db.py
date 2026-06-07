import asyncio
from database import engine

async def test():
    try:
        async with engine.begin() as conn:
            print("✅ Database Connected Successfully")
    except Exception as e:
        print("❌ Error:", e)

asyncio.run(test())