# Azure AI Search Custom Address Merge Skill

This project demonstrates how to extend Azure AI Search with a custom web API skill. The solution processes JSON documents containing address components and merges them into a unified searchable address field during indexing.

## Solution Overview

The solution consists of the following components:

1. **Source Data**: JSON documents containing separate address components (street name, house number, city)
2. **Custom Web API Skill**: A Python-based Azure Function that merges address components
3. **Azure AI Search**: Configuration including data source, index definition, skillset, and indexer

## Architecture

```
┌─────────────┐     ┌───────────────┐     ┌───────────────────────┐
│ JSON Data   │────>│ Azure AI      │────>│ Custom Address Merge  │
│ in Blob     │     │ Search Indexer│     │ Skill (Azure Function)│
└─────────────┘     └───────┬───────┘     └──────────┬────────────┘
                            │                        │
                            ▼                        │
                    ┌─────────────────┐              │
                    │ Azure AI Search │<─────────────┘
                    │ Index           │
                    └─────────────────┘
```

## Components

### 1. Source Data

Sample JSON data is structured as follows:

```json
[
    {
        "id": "1",
        "streetName": "Main Street",
        "houseNumber": "123B",
        "city": "New York"
    },
    {
        "id": "2",
        "streetName": "Park Avenue",
        "houseNumber": "456 33B",
        "city": "San Francisco"
    }
]
```

### 2. Custom Address Merge Skill

An Azure Function that:
- Accepts HTTP POST requests with a JSON payload containing address components
- Combines streetName, houseNumber, and city into a formatted fullAddress field
- Returns the merged address in a format compatible with Azure AI Search's custom skill interface

The skill is implemented in Python and follows the Azure AI Search custom skill interface requirements.

### 3. Azure AI Search Configuration

#### Data Source

The data source connects to an Azure Blob Storage container using managed identity authentication, targeting the "mergetestaddress" container.

#### Index Definition

The index includes fields for:
- id (key field)
- streetName (original component)
- houseNumber (original component)
- city (original component)
- fullAddress (enriched field from the custom skill)

All fields are configured with appropriate attributes for searching, filtering, and retrieving.

#### Skillset

The skillset configuration defines how the custom web API skill is integrated into the indexing pipeline, specifying:
- The skill's endpoint (URI)
- Input and output field mappings
- Context and batch processing parameters

#### Indexer

The indexer connects everything, defining:
- The data source to pull from
- The skillset to apply
- The target index where the results will be stored
- Field mappings between the source data, skills, and index

## Setup and Deployment

### Prerequisites

- Azure subscription
- Azure AI Search service
- Azure Storage account with a container for the source data
- Azure Function App for hosting the custom skill

### Deployment Steps

1. **Deploy the Custom Skill**:
   - Navigate to the `skill` directory
   - Deploy the Azure Function using Azure CLI or VS Code
   ```
   cd skill
   func azure functionapp publish <your-function-app-name>
   ```

2. **Configure Azure AI Search**:
   - Create the data source, index, skillset, and indexer using the JSON definitions in the `definitions` directory
   - Update the URI in the skillset definition with your function app's URL and key

3. **Run the Indexer**:
   - Trigger the indexer to process the data and apply the custom skill
   - Monitor the indexer status in Azure Portal

## Testing

You can test the custom skill locally before deployment:

1. Install the required dependencies:
   ```
   pip install -r skill/requirements.txt
   ```

2. Start the function locally:
   ```
   cd skill
   func start
   ```

3. Send a test request to the function endpoint:
   ```
   POST http://localhost:7071/api/merge-address
   ```

## Related Documentation

- [Azure AI Search Documentation](https://learn.microsoft.com/en-us/azure/search/)
- [Azure AI Search Custom Skills](https://learn.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-interface)
- [Create a Custom Skill for Azure AI Search](https://learn.microsoft.com/en-us/azure/search/cognitive-search-create-custom-skill-example)
- [Azure Functions Python Developer Guide](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- [Managed Identity with Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-howto-managed-identities-data-sources)

## Advanced Scenarios

This solution demonstrates a basic implementation of a custom skill, but it can be extended for more complex scenarios:

- **Multiple Custom Skills**: Chain multiple skills together for advanced data processing
- **AI Enrichment**: Integrate with Azure OpenAI or other AI services for more sophisticated data enrichment
- **Complex Data Transformation**: Enhance the custom skill to handle more complex data transformation logic
- **Error Handling**: Implement more robust error handling and validation
- **Monitoring**: Add telemetry and monitoring for production environments

## Contributing

Contributions to improve this solution are welcome. Please feel free to submit pull requests or open issues to suggest improvements.

## License

[Specify your license information here]