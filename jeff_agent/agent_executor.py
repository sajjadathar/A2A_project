# step2: Agent ecxecutor

from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue

from agent import JeffAgent

class JeffAgentExecutor(AgentExecutor):
    def __ini__(self):
        self.agent = JeffAgent()
    

    async def exrcute(self, context:RequestContext, event_queue:EventQueue):
        query = context.get_user_input()
        context_id = context.context_id
        response = self.agent.get_response(query=query, context_id=context_id)
        return response["content"]

    async def cancel(self, context:RequestContext, event_queue:EventQueue):
        return