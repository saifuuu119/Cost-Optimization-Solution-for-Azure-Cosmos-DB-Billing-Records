# Cost-Optimization-Solution-for-Azure-Cosmos-DB-Billing-Records

Overview

This solution optimizes costs for a serverless Azure Cosmos DB database storing billing records by implementing a tiered storage approach: recent records (<3 months) remain in Cosmos DB, while older records (>3 months) are archived to Azure Blob Storage. Azure Functions handle archival and retrieval, ensuring no data loss, downtime, or API changes.

Architecture:

Client Application
         |
         v
[API Layer (Azure API Management or App Service)]
         |
         v
[Azure Cosmos DB (Hot Tier: <3 months)]
         |                    ^
         v                    |
[Azure Function: Archival]   [Azure Function: Retrieval]
         |                    |
         v                    |
[Azure Blob Storage (Cold Tier: >3 months)]
         |
         v
[Azure Monitor + Cost Management]

# Azure Cosmos DB Cost Optimization Challenge

This repository contains a solution for optimizing costs in a serverless Azure Cosmos DB database storing billing records. The solution uses a tiered storage approach with Azure Blob Storage for archival and Azure Functions for automation.

## Contents
- `solution.md`: Detailed solution with architecture, pseudocode, and commands.
- `scripts/`: Python scripts for Azure Functions.
- `architecture.drawio`: Architecture diagram.

