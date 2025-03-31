import json
import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function endpoint that processes requests for the Address Merge Skill.
    This function merges streetName, houseNumber and city fields into a fullAddress field.
    """
    logging.info('Address Merge Skill: Function processed a request.')

    try:
        body = req.get_json()
    except ValueError:
        logging.error("Invalid request body received")
        return func.HttpResponse(
            body=json.dumps({"error": "Invalid request body"}),
            mimetype="application/json",
            status_code=400
        )

    if not body:
        logging.error("Empty request body received")
        return func.HttpResponse(
            body=json.dumps({"error": "Request body is empty"}),
            mimetype="application/json",
            status_code=400
        )
    
    values = body.get('values', [])
    if not values:
        logging.warning("No values provided in the request")
    
    # Process the records
    results = []
    for record in values:
        record_id = record['recordId']
        data = record.get('data', {})
        
        try:
            # Extract the address components
            street_name = data.get('streetName', '')
            house_number = data.get('houseNumber', '')
            city = data.get('city', '')
            
            # Merge the components into a full address
            full_address = f"{street_name} {house_number}, {city}"
            full_address = full_address.strip()
            
            # Log successful processing
            logging.info(f"Successfully processed record {record_id}: created '{full_address}'")
            
            results.append({
                "recordId": record_id,
                "data": {
                    "fullAddress": full_address
                },
                "errors": None,
                "warnings": None
            })
        except Exception as e:
            # Log any errors during processing
            logging.error(f"Error processing record {record_id}: {str(e)}")
            results.append({
                "recordId": record_id,
                "errors": [{"message": str(e)}],
                "warnings": None,
                "data": {
                    "fullAddress": None
                }
            })

    # Return the results
    return func.HttpResponse(
        body=json.dumps({"values": results}),
        mimetype="application/json"
    )