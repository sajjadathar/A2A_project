# step3: Agent card

from pydoc import describe
from a2a.types import(
    AgentCapabilities,
    AgentCard,
    AgentSkill
)
import uvicorn
from agent import MarkAgent
from agent_executor import MarkAgentExecutor
# import httpx
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.apps import A2AStarletteApplication


def main(host="localhost", port=10005):
    
    skill = AgentSkill(
        id="scheduling_badminton",
        name="Badminton scheduling tool",
        description="Helps with finding Mark's availability for badminton",
        tags=["scheduling", "badminton"],
        examples=["Are you available to play badminton on 2025-11-09"]
    )

    agent_card = AgentCard(
        name="Mark's Agent",
        description="Helps with scheduling badminton games",
        url=f"http://{host}:{port}",
        version="",
        defaultInputModes=MarkAgent.SUPPORTED_CONTENT_TYPES,
        defaultOutputModes=MarkAgent.SUPPORTED_CONTENT_TYPES,
        capabilities=AgentCapabilities(),
        skills=[skill],
    )

    # step4: hosta the Agent
    # Request handler

    # httpx_client = httpx.AsyncClient()

    request_handler =DefaultRequestHandler(
        agent_executor=MarkAgentExecutor,
        task_store=InMemoryTaskStore(),
        # push_notifier=InMemoryPushNotifier(httpx_client),
    )

    # Host the app
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler
    )

    uvicorn.run(server.build(), host=host, port=port)


if __name__=="__main__":
    main() 


