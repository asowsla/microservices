import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from shared.core.db_config import INTERVAL
from etl import run_etl


async def main():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        run_etl, 
        "interval", 
        seconds=INTERVAL, 
        max_instances=1)
    scheduler.start()

    print(f"[ETL] scheduler has started with {INTERVAL} sec. interval")

    try:
        while True:
            await asyncio.sleep(3600)
    except Exception as e:
        print("Unexpected error in scheduler", e)
        raise
    

if __name__ == "__main__":
    asyncio.run(main())