import io
from langchain_openai.chat_models import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from PIL import Image
from langchain_core.tools import tool
import random

model = ChatOpenAI(
    temperature=1,
    max_tokens=1000,
    model='gpt-4o'
)
 
@tool 
def perform_mysterious_operation(x: int) -> int:
    """
    Generates a mysterious number from the given integer input.

    The internal logic behind this transformation is unknown and cannot be inferred,
    even by the calling agent. The result is always an integer. This function must
    be invoked each time a mysterious number is required, regardless of the input value.

    Parameters:
        x (int): An integer input.

    Returns:
        int: A mysterious integer derived from the input.
    """
    
    return x + random.randint(1, 10)
     

#System prompt
system_prompt = SystemMessage(
    """You are a math expert capable of solving mathematical problems. You have access to a special tool that generates a mysterious number from any given integer.
    This operation cannot be inferred or calculated manually — you must call the tool every time a mysterious number is required.
    Use only the available tools to find solutions to the user's problems, and never attempt to compute results yourself"""
)

agent_tools=[perform_mysterious_operation]

inputs = {"messages":[("user","Return the mysterious number for the number 20, then return the mysterious number obtained from that first result.")]}

agent=create_react_agent(
    model=model, 
    state_modifier=system_prompt,
    tools=agent_tools,
    debug=True
   )
  
result = agent.invoke(inputs) 

print(f"Agent returned : {result['messages'][-1].content}")

