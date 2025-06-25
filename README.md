# Cost-Optimization-Solution-for-Azure-Cosmos-DB-Billing-Records

Overview

This solution optimizes costs for a serverless Azure Cosmos DB database storing billing records by implementing a tiered storage approach: recent records (<3 months) remain in Cosmos DB, while older records (>3 months) are archived to Azure Blob Storage. Azure Functions handle archival and retrieval, ensuring no data loss, downtime, or API changes.

Implementation

1. Configure Cosmos DB:

Enable TTL (90 days) on records.
Use serverless mode.
Command:
az cosmosdb update --name <cosmos-account> --resource-group <rg> --default-ttl 7776000

2. Set Up Blob Storage:
Create a Cool tier container.

Command:
az storage container create --name billing-archive --account-name <storage-account> --access-tier Cool

3. Archival Function:
Trigger: Daily timer.

Logic:
Query records older than 90 days.
Copy to Blob Storage.
Mark as archived in Cosmos DB (optional metadata).

4. Retrieval Function:

Trigger: HTTP or Cosmos DB read request.
Logic:
Check Cosmos DB.
If not found, fetch from Blob Storage.

5. Monitoring:
Set up Azure Monitor for logs.
Create cost alerts in Azure Cost Management.

Command:
az monitor alert create --name cost-alert --resource-group <rg> --condition "total cost > 100" --action email --email-address admin@company.com
