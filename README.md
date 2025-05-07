# Predictive Planning

## Installation
1. Fork and clone the repository.
1. Create a Python virtual environment
    ```python
    python -m venv venv
    ```
1. Run:
    ```python
    pip install -r requirements.txt
    ```
    to install dependencies

## AWS Bedrock Setup
You will need access to an AWS account.

### Model Access
This tool is currently set up for Anthropic Claude 3.7.
1. Navigate to the Amazon Bedrock service in the AWS Management Console.
2. Explore the available models in the "Foundation models" section. Choose Anthropic Claude 3.7.

### Knowledge Base using Files in S3

To create a knowledge base for the RAG model using files in Amazon S3, we need the "Knowledge base" feature.
1. Create an S3 bucket and store the files there.
2.  **Create a Knowledge base:**
    * In the Bedrock console, go to "Agents" and then "Knowledge bases."
    * Click "Create knowledge base."
    * Provide a name and description for your knowledge base.
3.  **Connect to your S3 bucket:**
    * In the "Data source" section, select "Amazon S3."
    * Specify the S3 URI of the bucket or the specific prefix where your documents are located.
4.  **Configure embedding model:**
    * Choose an embedding model available in Bedrock (e.g., Amazon Titan Embedding G1 - Text). This model will be used to create vector embeddings of your documents.
5. Choose a managed vector store provided by Bedrock.
6.  **Create and sync:** Review your configuration and click "Create knowledge base." Bedrock will then process the documents, generate embeddings, and store them in the chosen vector store. You might need to manually "sync" the knowledge base after creation or when you add new documents.

### Agent
After creating the knowledge base, you need an agent that uses it for retrieval during generation:

1.  **Create an Agent:**
    * In the Bedrock console, go to "Agents" and click "Create agent."
    * Provide a name and description for your agent.
    * Select the foundation model you want the agent to use for generation.
2.  **Attach the Knowledge Base:**
    * In the "Add knowledge base" step, select the knowledge base you created in the previous step.
    * Configure any relevant retrieval parameters (e.g., number of results to retrieve).
3.  **Add Tools (Optional):**
    * You can integrate other tools or functions with your agent if needed.
5.  **Review and Create:** Review your agent configuration and click "Create agent."
6.  **Test your Agent:** Use the testing console to interact with your agent and see how it leverages the knowledge base to answer questions.

You will need to configure AWS Credentials in your local shell as detailed [here](https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-files.html)

Then, run the application using this command in the terminal:
```bash
streamlit run src/main.py 
```