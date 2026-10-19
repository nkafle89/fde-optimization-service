from dotenv import load_dotenv

from app.agents.transportation_agent import TransportationAgent

load_dotenv()

agent = TransportationAgent()

answer = agent.run(
    "What is the total demand for stores requiring "
    "100, 150, and 80 units?"
)


print(answer)

answer = agent.run(
    "My stores need 100, 150, and 80 units. "
    "My distribution centers have capacities of "
    "200 and 100 units. Can I satisfy demand?"
)

print(answer)
