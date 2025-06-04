from datetime import datetime, timezone
from typing import Optional
from extractor import extract_updated_products
from loader import load_to_elasticsearch
from configs.db_config import get_db_session_instance


# variable to track last time synchonization
last_sync_time: Optional[datetime] = None


# performs ETL process to synchronize updated products with Elasticsearch
async def run_etl():
    global last_sync_time
    current_sync_time = datetime.now(timezone.utc)
    
    session = await get_db_session_instance()
    
    try:
        products = await extract_updated_products(session, last_sync_time)
        
        if not products:
            print("[ETL] no changes to synchronization")
            return
            
        await load_to_elasticsearch(products)
        print(f"[ETL] synchronized {len(products)} updated product(s)")
            
        last_sync_time = current_sync_time
        
    finally:
        await session.close()