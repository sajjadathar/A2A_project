from email import message
from logging import config
from subprocess import check_output
from urllib import response
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages.ai import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import get_availability

from dotenv import load_dotenv

# Step1: Agent & tool
# step2: Agent ecxecutor
# step3: Agent card
# step4: hosta the Agent

load_dotenv()

memory = MemorySaver()

class JeffaGENT():
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        self.tools = [get_availability]
        self.system_prompt = ("You are Jeff Bezos's scheduling assistant.\n"
                    "Your only job is to use the 'get_availability' tool "
                    "to answer questions about Jeff Bezos's schedule for playing badminton.\n\n"
                    "If the question is unrelated to scheduling, politely say you can’t help.\n"
                )

        self.graph = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt=self.system_prompt,
            checkpointer=memory
        )
    async def get_response(self, query, context_id):
        inputs = {"messages": [("user", query)]}
        config = {"configurable": {"thread_id": context_id}}
        raw_response = self.graph.invoke(inputs, config)
        messages = raw_response.get("messages", [])
        ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
        response = ai_messages[-1] if ai_messages else "No response"
        return response