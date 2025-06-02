# ETL

## description  
the service is responsible for exporting changed data from PostgreSQL to Elasticsearch.

## service tasks:  
1. extracting updated products from PostgreSQL  
2. transferring new data to Elasticsearch  
3. automatic scheduling of the ETL process  

## module structure  

### `main.py`  
- entry point, task scheduler initialization  
- uses `apscheduler` for periodic task execution  
- interval configured via `SCHEDULE_INTERVAL_SECONDS` environment variable  

### `etl.py`  
- core ETL process:  
  - Calls `extract_updated_products()` and `load_to_elasticsearch()` functions  
  - updates last synchronization timestamp  

### `extractor.py`  
- postgreSQL data extraction:  
  - selects products where `update_time > last_sync_time`  

### `loader.py`  
- elasticsearch data loading:  
  - adds documents to index specified in `.env`  

## component relationships  
- eTL process runs on a timer  
- extracts changes from PostgreSQL  
- sends new/updated records to Elasticsearch  