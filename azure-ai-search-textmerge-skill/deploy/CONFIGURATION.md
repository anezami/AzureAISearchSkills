# Configuration Guide

This document explains how to securely configure and deploy the Azure AI Search Custom Address Merge Skill solution.

## Configuration Files

The solution uses template configuration files with placeholders for sensitive information. Before deploying, you'll need to create your own configuration files with actual values:

### 1. Data Source Configuration

Copy `definitions/dataSource.template.json` to `definitions/dataSource.json` and replace the placeholders:

```json
"credentials": {
  "connectionString": "ResourceId=/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.Storage/storageAccounts/<your-storage-account>;"
},
"container": {
  "name": "<your-container-name>",
  "query": null
}
```

### 2. Custom Skill Configuration

Copy `skill/address_merge_skill.template.json` to `skill/address_merge_skill.json` and update:

```json
"uri": "https://<your-function-app-name>.azurewebsites.net/api/merge-address?code=<your-function-key>"
```

## Azure Function Local Settings

When developing locally, create a `local.settings.json` file in the `skill` directory:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "",
    "FUNCTIONS_WORKER_RUNTIME": "python"
  }
}
```

## Environment Variables

For deployment automation, create a `.env` file in the `deploy` directory with your configuration values:

```
SUBSCRIPTION_ID=your-subscription-id
RESOURCE_GROUP=your-resource-group
STORAGE_ACCOUNT_NAME=your-storage-account
CONTAINER_NAME=your-container-name
FUNCTION_APP_NAME=your-function-app-name
SEARCH_SERVICE_NAME=your-search-service-name
SEARCH_ADMIN_KEY=your-search-admin-key
```

**Important:** All files containing actual credentials (`.env`, `local.settings.json`, and the non-template configuration files) are included in the `.gitignore` file to prevent accidentally committing secrets to version control.

## Security Best Practices

1. **Use Managed Identities** whenever possible instead of connection strings or keys
2. **Restrict Access** to your Azure resources using appropriate network rules
3. **Rotate Keys** regularly for any shared access keys that are used
4. **Use Environment Variables** for sensitive information in CI/CD pipelines
5. **Audit Access** to your Azure resources regularly