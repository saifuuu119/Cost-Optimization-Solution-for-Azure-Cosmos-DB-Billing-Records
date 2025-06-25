from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient
import datetime

def archive_records():
    cosmos_client = CosmosClient(COSMOS_URL, COSMOS_KEY)
    db = cosmos_client.get_database_client("billing")
    container = db.get_container_client("records")
    
blob_client = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
    blob_container = blob_client.get_container_client("billing-archive")
    
 # Query records older than 90 days
  cutoff = datetime.datetime.now() - datetime.timedelta(days=90)
    query = f"SELECT * FROM c WHERE c.timestamp < '{cutoff.isoformat()}'"
    items = container.query_items(query, enable_cross_partition_query=True)
    
for item in items:
        # Write to Blob Storage
        blob_name = f"{item['timestamp'].year}/{item['timestamp'].month}/{item['id']}.json"
        blob = blob_container.get_blob_client(blob_name)
        blob.upload_blob(json.dumps(item), overwrite=True)
        
# Optional: Mark as archived
 item['archived'] = True   
 container.upsert_item(item)
    
  logging.info("Archival completed")
