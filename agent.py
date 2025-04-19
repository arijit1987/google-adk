from google.adk.agents import LlmAgent
from google.adk.tools import google_search

MODEL = "gemini-2.0-flash-001"

idea_agent = LlmAgent(
    name="IdeaGenerator",
    description="An agent that generates ideas and suggestions based on user preferences and requests.",
    instruction="You are a creative travel agent. Use the tool to brainstorm ideas and suggestions for travel destinations, activities, and itineraries based on user preferences.",
    model=MODEL,
    #tools=[google_search],
    disallow_transfer_to_parent=True
)

refiner_agent = LlmAgent(
    name="RefinerAgent", 
    description="Review provided travel ideas and select only those estimated to cost under the provided budget for a international trip.",
    instruction="Use your tool to review the provided trip ideas. Respond only with the ideas likely to cost under the provided budget for a international trip. Do not provide any additional information.",
    model=MODEL,
    #tools=[google_search],
    disallow_transfer_to_parent=True
)

root_agent = LlmAgent(
    name="PlannerAgent",
    model=MODEL,
    instruction=f"""You are trip planner, coordinating specialist agents. 
Your goal is to provide budget-friendly international trip ideas. For each user requests follow the below instructions:
    1. First use {idea_agent} to brainstorm ideas based on the user requests.
    2. Then use {refiner_agent} to take those ideas to filter them for the provided budget.
    3. Present the final refined list to the user along with the budget.""",
    sub_agents=[idea_agent, refiner_agent]
)

# Export the root agent for ADK to discover
agent = root_agent