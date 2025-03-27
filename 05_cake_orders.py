# pip install pillow

import os
import io  
from langchain_openai.chat_models import ChatOpenAI
import pandas as pd
from langchain_core.tools import tool 
from langchain_core.messages import HumanMessage
from PIL import Image  
from agents.cake_order_graph  import CakeOrdersAgent


product_orders_df = pd.read_csv("Data/cakes_orders.csv")
#print(product_orders_df)
cake_df = pd.read_csv("Data/cakes_data.csv")
#print(cake_df)

@tool
def get_cake_order_details(order_id:int) -> str :
    """
    Given an order ID, this function retrieves information about a cake order.
    It checks for an exact match between the provided order ID and existing ones.
    When a match is found, it returns the ordered cakes, the quantity for each, the total price of the order, and the delivery date.
    If no corresponding order ID is found, the function returns None.
    """
    
    order_df = product_orders_df[
                        product_orders_df["Order_ID"] == order_id ]

 
    if len(order_df) == 0 :
        return None
    else:
        return order_df.iloc[0].to_dict()


#print(get_cake_order_details(1006))
 

@tool
def update_order_quantity(order_id:int, qtt:int, operation_type:str) -> bool :
    """
     Updates the quantity of a cake in a given order, using the specified operation type.

    Parameters:
    - order_id (str): The unique ID of the order to update.
    - qtt (int): The quantity value used in the update.
    - operation_type (str): Defines how the quantity should be updated. It can be:
        - "add": Increase the existing quantity by Qtt
        - "replace": Set the quantity to Qtt
        - "subtract": Decrease the existing quantity by Qtt

    Returns:
    - True if the update is successful.
    - False if the order is not found.
    """
    
    order_df = product_orders_df[product_orders_df["Order_ID"] == order_id ]

    
    if len(order_df) == 0 :
        return False
    else:
        order_cake_name =order_df.iloc[0].to_dict()["Nom-du-gâteau"]
        cake_name_df =  cake_df[cake_df["Nom-du-gâteau"] == order_cake_name].iloc[0]
        cake_price =float(cake_name_df.to_dict()["Prix"]) 
     
        current_qtt = product_orders_df[product_orders_df["Order_ID"] == order_id].iloc[0].to_dict()["Qtt"]
        match operation_type:
            case "add":
                new_qtt = int(current_qtt) + qtt
                product_orders_df.loc[
                      product_orders_df["Order_ID"] == order_id, 
                      "Qtt"] = new_qtt
                product_orders_df.loc[
                      product_orders_df["Order_ID"] == order_id, 
                      "Prix"] = new_qtt * cake_price
                
            case "replace":
                product_orders_df.loc[
                      product_orders_df["Order_ID"] == order_id, 
                      "Qtt"] = qtt
                product_orders_df.loc[
                      product_orders_df["Order_ID"] == order_id, 
                      "Prix"] = qtt * cake_price
                
            case "subtract":
                new_qtt = int(current_qtt) - qtt
                if new_qtt <= 0 : new_qtt=0
                product_orders_df.loc[
                      product_orders_df["Order_ID"] == order_id, 
                      "Qtt"] = new_qtt
                product_orders_df.loc[
                      product_orders_df["Order_ID"] == order_id, 
                      "Prix"] = new_qtt * cake_price
        return True

#update_order_quantity(1010, 1, "add")
#print(product_orders_df)
 
model = ChatOpenAI(
    temperature=1,
    max_tokens=1000,
    model='gpt-4o'
)
 

 
system_prompt = """
    You are a professional virtual assistant specialized in managing customer orders for cakes sold by our company.
    Your tools allow you to retrieve order details and update the quantity of items in an order.
    Only provide information related to the specific order requested — never disclose details about other orders.
    You may also engage in small talk and greetings, always maintaining a courteous and professional tone.
    """

 
cake_orders_agent = CakeOrdersAgent(model, 
                           [get_cake_order_details, update_order_quantity], 
                           system_prompt,
                           debug=False)
 

'''
image_data = cake_orders_agent.agent_graph.get_graph().draw_mermaid_png()
image = Image.open(io.BytesIO(image_data))
image.show()
'''

import uuid

user_inputs = [
    "Hope you're doing well — how are things?",
    "Could you provide the details for order number 1006?",
    "Could you increase the quantity of that cake by four?",
    "Can you display the order details once more?",
    "Talk to you soon!"
]

#Create a new thread
config = {"configurable": {"thread_id": str(uuid.uuid4())}}

for input in user_inputs:
    print(f"==========================================\nUSER : {input}")
    user_message = {"messages":[HumanMessage(input)]}
    ai_response = cake_orders_agent.agent_graph.invoke(user_message,config=config)
    print(f"\nAGENT : {ai_response['messages'][-1].content}")
 