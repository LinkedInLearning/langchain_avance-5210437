import io
import os
from langchain_openai.chat_models import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from PIL import Image

 
model = ChatOpenAI(
    temperature=1,
    max_tokens=1000,
    model='gpt-4o'
)
 
 
@tool
def sum_two_numbers(x:int, y:int) -> int :

    """
    This function takes two integers as input, adds them together, and returns their sum as an integer.
    """
    return x + y

@tool
def multiply_numbers(x:float, y:float) -> float :
    """
    This function takes two integers as input, multiplies them, and returns their product as an integer
    """
    return x * y

@tool 
def divide_numbers(x: float, y: float) -> float:
    """
    This function takes two floating-point numbers as input, divides the first by the second,
    and returns the result as a float. Raises a ZeroDivisionError if the second number is zero.
    """
    return x / y

#System prompt
system_prompt = SystemMessage(
    """You are a math expert capable of solving mathematical problems. Use only the available tools to find solutions to the problems provided by the user, without solving them manually"""
)

agent_tools=[sum_two_numbers, multiply_numbers,divide_numbers]

inputs = {"messages":[("user"," What is the result of 5 + 5? What is the result of dividing that first result by 10? ")]}

agent=create_react_agent(
    model=model, 
    state_modifier=system_prompt,
    tools=agent_tools,
    debug= True
   )
 
  
 
image_data = agent.get_graph().draw_mermaid_png()
image = Image.open(io.BytesIO(image_data))
image.show()
 

result = agent.invoke(inputs) 

print("Step by Step execution : ")
for message in result['messages']:
    print(message.pretty_repr())
 
