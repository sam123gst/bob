from langchain_google_vertexai import ChatVertexAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

memory = MemorySaver()


class CarReviewerAgent:
    SYSTEM_INSTRUCTION = """You are a car review agent tasked with 
    providing information about cars, reviews, and recommendations. Use the google_search 
    tool to find information on the web about options, reviews, and recommendations 
    and procedures. Cite your sources in your responses. Output all of the 
    information you find."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self):
        self.model = ChatVertexAI(
            model="gemini-2.5-flash-lite",
            location=os.getenv("GOOGLE_CLOUD_LOCATION"),
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        ).bind_tools([{"google_search": {}}])

        def call_model(state):
            messages = [("system", self.SYSTEM_INSTRUCTION), *state["messages"]]
            response = self.model.invoke(messages)
            return {"messages": [response]}

        builder = StateGraph(MessagesState)
        builder.add_node("agent", call_model)
        builder.add_edge(START, "agent")
        builder.add_edge("agent", END)
        self.graph = builder.compile(checkpointer=memory)

    def invoke(self, query, sessionId) -> str:
        config = {"configurable": {"thread_id": sessionId}}
        self.graph.invoke({"messages": [("user", query)]}, config)
        return self.get_agent_response(config)

    def get_agent_response(self, config):
        current_state = self.graph.get_state(config)
        return current_state.values["messages"][-1].content
