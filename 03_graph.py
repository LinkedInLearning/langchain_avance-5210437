# pip install pillow

 
import io 
from langchain_core.messages import HumanMessage
from PIL import Image
import uuid
#from agents.graph_01 import MyGraph
#from agents.graph_02 import MyGraph
from agents.graph_03 import MyGraph
#from agents.graph_04 import MyGraph
   
my_agent = MyGraph()

config = {"configurable": {"thread_id": str(uuid.uuid4())}}  
user_message = {"messages":[HumanMessage("Hello from humain")]}
 
 
image_data = my_agent.agent_graph.get_graph().draw_mermaid_png()
image = Image.open(io.BytesIO(image_data))
image.show()


result = my_agent.my_invoke(user_message, config=config) 

''' 
print("Step by Step execution : ")
for message in result['messages']:
    print(message)
''' 