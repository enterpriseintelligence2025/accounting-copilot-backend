from langchain_core.messages import HumanMessage, AIMessage
from app.llm import llm, llm_streaming

def chat(messages: list) -> str:
    lc_messages = []
    for m in messages:
        if m["role"] == "user":
            lc_messages.append(HumanMessage(content=m["content"]))
        else:
            lc_messages.append(AIMessage(content=m["content"]))

    response = llm.invoke(lc_messages)
    return response.content



def stream_chat(messages: list):
    lc_messages = []

    for m in messages:
        if m["role"] == "user":
            lc_messages.append(HumanMessage(content=m["content"]))
        else:
            lc_messages.append(AIMessage(content=m["content"]))

    for chunk in llm_streaming.stream(lc_messages):
        if chunk.content:
            yield chunk.content