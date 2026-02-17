# step2: Agent ecxecutor

from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue

from agent import MarkAgent

class MarkAgentExecutor(AgentExecutor):
    def __ini__(self):
        self.agent = MarkAgent()
    

    async def execute(self, context:RequestContext, event_queue:EventQueue):
        query = context.get_user_input()
        # context_id = context.context_id
        response = self.agent.invoke(query=query)
        return response

    async def cancel(self, context:RequestContext, event_queue:EventQueue):
        return