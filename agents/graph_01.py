from langgraph.checkpoint.memory import MemorySaver  
from langgraph.graph import StateGraph, END 
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage 
 


class OrdersAgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class MyGraph:

    
    def __init__(self): 

        agent_graph=StateGraph(OrdersAgentState)
        agent_graph.add_node("Node1",self.operation_node_1)
        agent_graph.add_node("Node2",self.operation_node_2)
        agent_graph.add_edge("Node1","Node2")
        agent_graph.add_edge("Node2",END)
        agent_graph.set_entry_point("Node1")
        self.memory=MemorySaver()
        self.agent_graph = agent_graph.compile(checkpointer=self.memory)
 
    
    def operation_node_1(self, state:OrdersAgentState):
        input_message = state["messages"][-1].content
        print(f"Input of Node-1 : {input_message}")
        return {"messages":[f"Hello from Node-1"] }
    
    def operation_node_2(self, state:OrdersAgentState):
        input_message = state["messages"][-1]
        print(f"Input of Node-2 : {input_message}")
        return {"messages":[f"Hello from Node-2"] }
     
    
      
    def my_invoke(self, inputs, config):
        return self.agent_graph.invoke(inputs, config=config) 