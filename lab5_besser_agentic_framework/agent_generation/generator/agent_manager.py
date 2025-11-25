from besser.agent.core.agent import Agent
from besser.agent.platforms.websocket import WEBSOCKET_PORT


class AgentManager:
    port = 8765

    def __init__(self):
        self.agents: dict = {}

    def add_agent(self, agent: Agent):
        if agent.name in self.agents:
            raise ValueError(f"Agent with name {agent.name} already exists")
        agent.set_property(WEBSOCKET_PORT, AgentManager.port)
        AgentManager.port += 1
        self.agents[agent.name] = agent
