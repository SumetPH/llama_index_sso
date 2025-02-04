from llm_langchain.vector_store import load_vector_store
from llm_langchain.model import google_gemini
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import START, StateGraph
from langchain_core.messages import BaseMessage, trim_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
from typing import Sequence

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    context: str


def model(state: State):
    trimmer = trim_messages(
        strategy="last",
        token_counter=len,
        max_tokens=10,
        start_on="human",
        include_system=True,
    )

    trimmed_messages = trimmer.invoke(state["messages"])
    message = trimmed_messages[-1]
    # message.pretty_print()

    index = load_vector_store()
    results = index.similarity_search_with_score(
        query=message.content,
        k=50,
    )

    context = '\n\n'.join(result[0].page_content for result in results)
    # print(context)

    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "คุณเป็นผู้ช่วยตอบคำถามเกี่ยวกับเรื่องประกันสังคม"
                    "ตอบเป็นภาษาไทย"
                    "\n\n{context}\n\n"
                )
            ),
            # (
            #     "human",
            #     "{context}"
            # ),
            MessagesPlaceholder(variable_name="messages"),
        ],
    )

    prompt = prompt_template.invoke(
        {'messages': trimmed_messages, 'context': context}
    )

    llm = google_gemini()
    response = llm.invoke(prompt)

    return {"messages": response}

def chat_graph():
    graph = StateGraph(state_schema=State)
    graph.add_edge(START, "model")
    graph.add_node("model", model)

    memory = MemorySaver()

    app = graph.compile(checkpointer=memory)
    return app