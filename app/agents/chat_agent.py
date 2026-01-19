from langchain_core.messages import HumanMessage, AIMessage
from app.llm import llm, llm_streaming

def chat(messages: list) -> str:
    """
    Process a chat conversation and generate a response using the LLM.

    Args:
        messages (list): A list of message dictionaries (role, content).

    Returns:
        str: The content of the AI's response.
    """
    lc_messages = []
    for m in messages:
        if m["role"] == "user":
            lc_messages.append(HumanMessage(content=m["content"]))
        else:
            lc_messages.append(AIMessage(content=m["content"]))

    response = llm.invoke(lc_messages)
    return response.content



def stream_chat(messages: list):
    """
    Stream a chat conversation response using the streaming LLM.

    Args:
        messages (list): A list of message dictionaries (role, content).

    Yields:
        str: Chunks of the AI's response content.
    """
    lc_messages = []

    for m in messages:
        if m["role"] == "user":
            lc_messages.append(HumanMessage(content=m["content"]))
        else:
            lc_messages.append(AIMessage(content=m["content"]))

    for chunk in llm_streaming.stream(lc_messages):
        if chunk.content:
            yield chunk.content
