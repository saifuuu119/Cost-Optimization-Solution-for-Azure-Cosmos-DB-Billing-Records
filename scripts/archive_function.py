import azure.cosmos.cosmos_client as cosmos
from azure.storage.blob import BlobServiceClient
import datetime
import json

client = cosmos.CosmosClient("https://mycosmosaccount.documents.azure.com", "mykey")
database = client.get_database_client("billing")
container = database.get_container_client("records")

blob_client = BlobServiceClient(account_url="https://mystorageaccount.blob.core.windows.net", credential="myblobkey")
container_client = blob_client.get_container_client("billing-archive")

cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=90)
query = "SELECT * FROM c WHERE c.timestamp < @cutoff"
items = container.query_items(query=query, parameters=[{"name": "@cutoff", "value": cutoff.isoformat()}])

for item in items:
    blob_name = f"{item['timestamp'].year}/{item['timestamp'].month}/{item['id']}.json"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(json.dumps(item), overwrite=True)
    item['archived'] = True
    container.upsert_item(item)
