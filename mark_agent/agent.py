from urllib import response
from crewai import LLM, Agent, Crew, Process, Task
from dotenv import load_dotenv
import os

from tools import AvailabilityTool

import logging
logging.getLogger("google").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("root").setLevel(logging.CRITICAL)


load_dotenv()

class MarkAgent():
    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]
    
    def __init__(self):
        self.api_key=os.getenv("GEMINI_API_KEY")

        self.llm = LLM(
            model="gemini-2.0-flash",
            api_key=self.api_key,
        )

        self.agent = Agent(
            role="Scheduling Assistant",
            goal="Answer questions about Mark's availability.",
            backstory="You are a helpful scheduling assistant who checks Mark's calendar.",
            tools=[AvailabilityTool()],
            llm=self.llm,
        )

    async def invoke(self, user_question):
        task = Task(
            description=f"User asked: '{user_question}'.",
            expected_output="Polite response about availability",
            agent=self.agent,

        )
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
        )
        try:
            agent_response = str(crew.kickoff())
            return agent_response

        except Exception as e:
            print("\n[MarkAgent] Gemini unavailable → switching to TOOL MODE")
            print("Reason:", e)

            # Direct tool execution fallback
            for tool in self.agent.tools:
                if hasattr(tool, "run"):
                    return tool.run(user_question)

            return "Sorry, I cannot check Mark's availability right now."


    # print(invoke("Is Mark available on 2025-11-14", agent))

# import asyncio
# mark_agent = MarkAgent()
# print(asyncio.run(mark_agent.invoke("Is Mark available on 14th of November 2025")))