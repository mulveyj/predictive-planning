import boto3
import json

bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-west-2'
)

BASE_PROMPT = (
        "You are an expert advisor assisting a local council officer responsible for housing strategy. "
        "We are exploring options to meet future housing demand in a specific area.\n\n"
        "We are developing a predictive model to estimate future housing need and delivery, using inputs such as:\n"
        "- Population growth and migration trends\n"
        "- Local economic indicators (e.g. employment rates, wage growth, sector expansion)\n"
        "- Planning constraints and land availability\n"
        "- Local intelligence (e.g. strategic projects, regeneration plans, infrastructure investments)\n\n"
        "- Specifically take into account - gap between demand and supply - population - housing stock - net migration\n\n"
        "Keep the advice concise, strategic, and practical for use in a public sector context.\n\n"
    )

def generate_text(prompt, max_tokens=500, temperature=1):
    """
    Generate text using Claude 3.7 Sonnet on AWS Bedrock
    using an existing inference profile
    """
    inference_profile_arn = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "top_k": 250,
        "stop_sequences": [],
        "temperature": temperature,
        "top_p": 0.999,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    response = bedrock.invoke_model(
        modelId=inference_profile_arn, 
        contentType="application/json",
        accept="application/json",
        body=json.dumps(request_body)
    )
    
    # Parse the response
    response_body = json.loads(response.get('body').read())
    return response_body

# Example usage
if __name__ == "__main__":
    #add  user input here
    user_input = "Tell me the impact that there would be if a new development in Durham was all bungalows"
    prompt = BASE_PROMPT + user_input
    response = generate_text(prompt)
    
    # Extract and print the assistant's message
    if 'content' in response:
        for item in response['content']:
            if item['type'] == 'text':
                print(item['text'])