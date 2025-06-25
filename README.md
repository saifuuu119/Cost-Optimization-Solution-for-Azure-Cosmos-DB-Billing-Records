# Cost-Optimization-Solution-for-Azure-Cosmos-DB-Billing-Records

Overview

This solution optimizes costs for a serverless Azure Cosmos DB database storing billing records by implementing a tiered storage approach: recent records (<3 months) remain in Cosmos DB, while older records (>3 months) are archived to Azure Blob Storage. Azure Functions handle archival and retrieval, ensuring no data loss, downtime, or API changes.

Implementation

1. Configure Cosmos DB:

Enable TTL (90 days) on records.
Use serverless mode.
Command:
az cosmosdb update \--name MyCosmosAccount \--resource-group MyResourceGroup \--default-ttl 7776000 \--server-version 3.2 \--enable-serverless true

2. Set Up Blob Storage:
Create a Cool tier container.

Command:
az storage container create \--name billing-archive \--account-name mystorageaccount \--access-tier Cool

3. Archival Function:
Trigger: Daily timer.

Logic:
Query records older than 90 days.
Copy to Blob Storage.
Mark as archived in Cosmos DB (optional metadata).

4. Retrieval Function:

Objective: Handle retrieval requests, checking Cosmos DB first and fetching from Blob Storage if the record is not found.

Trigger: HTTP trigger or Cosmos DB change feed trigger for read requests.
Logic:
Attempt to read from Cosmos DB.
If not found, fetch from Blob Storage based on the record ID and timestamp-derived path.
Command to Deploy Function:

bash cammand:
az functionapp deployment source config-zip \--name MyRetrievalFunction \--resource-group MyResourceGroup \--src retrieval-function.zip

5. Monitoring:
Set up Azure Monitor for logs.
Create cost alerts in Azure Cost Management.

Command:
az monitor alert create --name cost-alert --resource-group <rg> --condition "total cost > 100" --action email --email-address sayedsaif9520@gmail.com

Create Cost Alert:
bash cammand:
az monitor alert create \--name CostAlertForBilling \--resource-group MyResourceGroup \--scopes /subscriptions/<subscription-id>/resourceGroups/MyResourceGroup \--condition "total cost > 100" \--action "email sayedsaif9520@gmail.com" \ --description "Alert when monthly cost exceeds $100"
