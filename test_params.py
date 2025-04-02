import json

def main(args):
    response = {
        "status": "ok",
        "received": args
    }
    return {
        "body": json.dumps(response),
        "headers": { "Content-Type": "application/json" },
        "statusCode": 200
    }



#%%

import json
import base64

def main(args):
    # Initialize an empty dictionary to hold the received data
    received_data = {}

    # Check if the '__ce_body' field exists in the incoming arguments
    if '__ce_body' in args:
        try:
            # Decode the base64-encoded data
            decoded_bytes = base64.b64decode(args['__ce_body'])
            decoded_str = decoded_bytes.decode('utf-8')
            # Parse the JSON string into a dictionary
            received_data = json.loads(decoded_str)
        except (base64.binascii.Error, json.JSONDecodeError) as e:
            # Handle decoding errors
            return {
                "body": json.dumps({"status": "error", "message": "Invalid base64 or JSON data", "error": str(e)}),
                "headers": { "Content-Type": "application/json" },
                "statusCode": 400
            }
    else:
        # If '__ce_body' is not present, assume the data is in the standard args
        received_data = args

    # Construct the response
    response = {
        "status": "ok",
        "received": received_data
    }

    return {
        "body": json.dumps(response),
        "headers": { "Content-Type": "application/json" },
        "statusCode": 200
    }


#%%
import json
import base64
import urllib.request

def main(args):
    received_data = {}

    if '__ce_body' in args:
        try:
            decoded_bytes = base64.b64decode(args['__ce_body'])
            decoded_str = decoded_bytes.decode('utf-8')
            received_data = json.loads(decoded_str)
        except (base64.binascii.Error, json.JSONDecodeError) as e:
            return {
                "body": json.dumps({"status": "error", "message": "Invalid base64 or JSON data", "error": str(e)}),
                "headers": { "Content-Type": "application/json" },
                "statusCode": 400
            }
    else:
        received_data = args

    # ✅ Use urllib to test external connectivity to Box
    try:
        with urllib.request.urlopen("https://api.box.com/2.0/") as response:
            box_status = response.status
            box_body = response.read().decode()
    except Exception as e:
        box_status = "error"
        box_body = str(e)

    # Return both the echo and the Box test
    return {
        "body": json.dumps({
            "status": "ok",
            "received": received_data,
            "box_api_test": {
                "status": box_status,
                "response": box_body
            }
        }),
        "headers": { "Content-Type": "application/json" },
        "statusCode": 200
    }


#%%%


