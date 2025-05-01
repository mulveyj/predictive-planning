import json
import requests

def invoke_sagemaker_endpoint(endpoint_url, input_data, content_type="application/json", custom_auth_header_name=None, custom_auth_header_value=None):
    """
    Invokes a SageMaker endpoint using the requests library.

    Args:
        endpoint_url (str): The URL of the SageMaker endpoint.
        input_data (dict or str): The input data to send to the model.  If it's a dict,
            it will be converted to a JSON string (if content_type is application/json).
            If it's already a string, it's sent as is.
        content_type (str, optional): The content type of the input data.
            Defaults to "application/json".
        custom_auth_header_name (str, optional): Name of a custom authorization header.
            Defaults to None.
        custom_auth_header_value (str, optional): Value of the custom authorization header.
            Defaults to None.

    Returns:
        dict: The model's prediction, as a Python dictionary (if the response is JSON),
              or the raw response text if the response is not JSON.  Returns None on error.
    """
    headers = {'Content-Type': content_type}
    if custom_auth_header_name and custom_auth_header_value:
        headers[custom_auth_header_name] = custom_auth_header_value

    # Convert input_data to JSON string if it's a dictionary and content type is json
    if isinstance(input_data, dict) and content_type == "application/json":
        input_data = json.dumps(input_data)
    elif not isinstance(input_data, str):
        input_data = str(input_data) #convert to string if it is not a dict or string.

    try:
        # Disable SSL verification (use with caution!)
        response = requests.post(endpoint_url, data=input_data, headers=headers, verify=False) #Added verify=False
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Attempt to decode the response as JSON
        try:
            return response.json()
        except json.JSONDecodeError:
            # If the response is not JSON, return the raw text
            return response.text

    except requests.exceptions.RequestException as e:
        print(f"Error invoking endpoint: {e}")
        return None
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        return None



def main():
    """
    Main function to demonstrate invoking a SageMaker endpoint.
    """
    # Replace with your actual SageMaker endpoint URL.
    endpoint_url = "https://runtime.sagemaker.us-west-2.amazonaws.com/endpoints/canvas-new-deployment-05-01-2025-11-03-AM/invocations"  # IMPORTANT: Replace this!

    # Example input data (replace with your model's expected input format)
    input_data = {
        "instances": [
            [5.1, 3.5, 1.4, 0.2],  # Example feature vector 1
            [6.2, 2.9, 4.3, 1.3]   # Example feature vector 2
        ]
    }

    # Example of sending JSON data
    print("Invoking endpoint with JSON input:")
    prediction = invoke_sagemaker_endpoint(endpoint_url, input_data)
    if prediction:
        print("Prediction:", prediction)

    # Example of sending a simple string
    print("\nInvoking endpoint with string input:")
    prediction_str = invoke_sagemaker_endpoint(endpoint_url, "This is a test string", content_type="text/plain")
    if prediction_str:
        print("Prediction (string response):", prediction_str)

    # Example with a custom authorization header (replace with your actual header and value if needed)
    # custom_header_name = "X-Amz-SageMaker-Custom-Attributes"  # Example header name
    # custom_header_value = "auth-token=my-secret-token"  # Replace with your actual token
    # print("\nInvoking endpoint with custom authorization header:")
    # prediction_auth = invoke_sagemaker_endpoint(endpoint_url, input_data, custom_auth_header_name=custom_header_name, custom_auth_header_value=custom_header_value)
    # if prediction_auth:
    #     print("Prediction (with auth):", prediction_auth)



if __name__ == "__main__":
    main()