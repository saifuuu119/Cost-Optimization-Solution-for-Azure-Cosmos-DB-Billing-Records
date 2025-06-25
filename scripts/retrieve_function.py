from azure.cosmos import CosmosClient, exceptions
from azure.storage.blob import BlobServiceClient

def retrieve_record(record_id):
    cosmos_client = CosmosClient(COSMOS_URL, COSMOS_KEY)
    db = cosmos_client.get_database_client("billing")
    container = db.get_container_client("records")
    
    blob_client = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
    blob_container = blob_client.get_container_client("billing-archive")
    
    try:
        # Try Cosmos DB
        item = container.read_item(item=record_id, partition_key=record_id)
        return item
    except exceptions.CosmosResourceNotFoundError:
        # Try Blob Storage
        for year in range(2020, datetime.datetime.now().year + 1):
            for month in range(1, 13):
                blob_name = f"{year}/{month}/{record_id}.json"
                try:
                    blob = blob_container.get_blob_client(blob_name)
                    data = blob.download_blob().readall()
                    return json.loads(data)
                except:
                    continue
        raise Exception("Record not found")