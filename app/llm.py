from langchain_openai import AzureChatOpenAI

from app.config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_VERSION
)

llm = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    deployment_name=AZURE_OPENAI_DEPLOYMENT,
    api_version=AZURE_OPENAI_API_VERSION,
    temperature=0
)

llm_streaming = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    deployment_name=AZURE_OPENAI_DEPLOYMENT,
    api_version=AZURE_OPENAI_API_VERSION,
    temperature=0,
    streaming=True
)