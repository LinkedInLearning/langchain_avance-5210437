from langgraph.graph import StateGraph,START, END
from typing import TypedDict
from typing import Annotated
import operator
from PIL import Image
import io


class MyState(TypedDict):
    log: Annotated[list[str], operator.add]

#class MyState(TypedDict):
    #log: str
 
 
 
def node_a(state: MyState) -> MyState:
    print(f"Dans le Node A: {state["log"]}")
    return {"log": ["A"]}

'''  
def node_b(state: MyState) -> MyState:
    print(f"Dans le Node B: {state["log"]}")
    return {"log": ["B"]}
''' 

def node_b1(state: MyState) -> MyState:
    print(f"Dans le Node B1: {state["log"]}")
    return {"log": ["B1"]}
 

def node_b2(state: MyState) -> MyState:
    print(f"Dans le Node B2: {state["log"]}")
    return {"log": ["B2"]}
 

def node_c(state: MyState) -> MyState:
    print(f"Dans le Node C: {state["log"]}")
    return {"log": ["C"]}

def node_d(state: MyState) -> MyState:
    print(f"Dans le Node D: {state["log"]}")
    return {"log": ["D"]}
 
 


 
graph = StateGraph(MyState)

''' 
graph.add_node("A", node_a)
graph.add_node("B", node_b)
graph.add_node("C", node_c)
graph.add_node("D", node_d)

graph.add_edge(START, "A") 
graph.add_edge("A", "B")
graph.add_edge("A", "C")
graph.add_edge("B", "D")
graph.add_edge("C", "D")
graph.add_edge("D", END)
'''


''' 
graph.add_node("A", node_a)
graph.add_node("B1", node_b1)
graph.add_node("B2", node_b2)
graph.add_node("C", node_c)
graph.add_node("D", node_d)

graph.add_edge(START, "A") 
graph.add_edge("A", "B1")
graph.add_edge("A", "C")
graph.add_edge("B1", "B2")
graph.add_edge("B2", "D")
graph.add_edge("C", "D")
graph.add_edge("D", END)
''' 

 
graph.add_node("A", node_a)
graph.add_node("B1", node_b1)
graph.add_node("B2", node_b2)
graph.add_node("C", node_c)
graph.add_node("D", node_d)

graph.add_edge(START, "A") 
graph.add_edge("A", "B1")
graph.add_edge("A", "C")
graph.add_edge("B1", "B2")
graph.add_edge(["B2","C"], "D")
graph.add_edge("D", END)
 

graph.set_entry_point("A") 
app = graph.compile()
 

 
image_data = app.get_graph().draw_mermaid_png()
image = Image.open(io.BytesIO(image_data))
image.show()
 

final_state = app.invoke({"log": []})
print("=== LOG FINAL ===")
print(final_state["log"])