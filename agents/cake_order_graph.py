import os

from langchain_openai.chat_models import ChatOpenAI
 
from langchain_core.tools import tool
 
from langgraph.checkpoint.memory import MemorySaver  
from langgraph.graph import StateGraph, END 
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
 
import json

class OrdersAgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class CakeOrdersAgent:
 
    def __init__(self, model, tools, system_prompt, debug):
        
        self.tools = { tool.name : tool for tool in tools }
        self.system_prompt=system_prompt
        self.debug=debug
 
        agent_graph=StateGraph(OrdersAgentState)
        agent_graph.add_node("Cake_LLM",self.call_llm)
        agent_graph.add_node("Cake_Tools",self.call_tools)
        agent_graph.add_conditional_edges(
            "Cake_LLM",
            self.is_tool_call,
            {True: "Cake_Tools", False: END }
        )
        agent_graph.add_edge("Cake_Tools","Cake_LLM")

        agent_graph.set_entry_point("Cake_LLM")

        self.memory=MemorySaver()      
        self.agent_graph = agent_graph.compile(checkpointer=self.memory)

        self.model=model.bind_tools(tools)


   
    def call_llm(self, state:OrdersAgentState):
        
        messages=state["messages"]
        if self.system_prompt:
            messages = [SystemMessage(content=self.system_prompt)] + messages
        result = self.model.invoke(messages)
        if self.debug:
            print(f"\nLLM Returned : {result}")
        #Return the LLM output
        return {"messages":[result] }
    
    
    #Check if the next action is a tool call.
    def is_tool_call(self, state:OrdersAgentState):
        last_message = state["messages"][-1]
        if len(last_message.tool_calls) > 0 :
            return True
        else:
            return False

   
    def call_tools(self, state:OrdersAgentState):    
        tool_calls = state["messages"][-1].tool_calls
        results=[]

        for tool in tool_calls:
            #Handle tool missing error
            if not tool["name"] in self.tools:
                print(f"Unknown tool name {tool}")
                result = "Invalid tool found. Please retry"
            else:
                result=self.tools[tool["name"]].invoke(tool["args"])
            results.append(ToolMessage(tool_call_id=tool['id'], 
                                       name=tool['name'], 
                                       content=str(result)))

            if self.debug:
                print(f"\nTools returned {results}")
            #return tool results
            return { "messages" : results }
