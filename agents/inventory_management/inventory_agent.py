import os
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.csv_tools import CsvTools
from pathlib import Path

import helpers.database_handler as db
import helpers.demand_prediction as dp
import helpers.email_helper as em

from dotenv import load_dotenv
import google.generativeai as genai 



def get_stock_quantity(item_id: int) -> int:
    """
    Use this function to retrieve the stock quantity for a specific item from the database.

    Args:
        item_id (int): Unique identifier of the item.

    Returns:
        int or None: Quantity of the item in stock if found; otherwise, None.

    Raises:
        Exception: If an error occurs during the database query.
    """

    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT quantity FROM stock WHERE item_id = %s;", (item_id,))
            result = cur.fetchone()
            if result:
                return str({"available_stock": result[0]})
            else:
                print(f"No stock record found for item_id {item_id}")
                return None
    except Exception as e:
        print(f"Error retrieving stock quantity: {e}")
        return None

def get_supplier_email_id(item_id: int) -> str:
    """
    Use this function to retrieve the email ID of the supplier for a specific item from the database.

    Args:
        item_id (int): Unique identifier of the item.

    Returns:
        str or None: email ID of the supplier of the item if found; otherwise, None.

    Raises:
        Exception: If an error occurs during the database query.
    """

    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT supplier_mail FROM stock WHERE item_id = %s;", (item_id,))
            result = cur.fetchone()
            if result:
                return str({"supplier_mail": result[0]})
            else:
                print(f"No record found for item_id {item_id}")
                return None
    except Exception as e:
        print(f"Error retrieving stock quantity: {e}")
        return None



def is_demand_greater(stock: int, demand: int) -> bool:
    """
    Use this function to compare the available stock quantity with predicted demand value and determine if demand is greater.

    Args:
        stock (int): Available stock quantity.
        demand (int): Predicted demand value.

    Returns:
        bool: True, if predicted demand value is greater than stock quantity. Else, False."
    """
    return str(int(demand) > int(stock))




load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = Gemini(id="gemini-1.5-flash")



conn = db.connect_to_db()


inventory_agent = Agent(
    name="Inventory Management Agent",
    model=gemini_model,
    tools=[
        #DuckDuckGo(),
        get_stock_quantity,
        dp.predict_demand,
        is_demand_greater,
    ],
    instructions=[#"You are a store owner that needs to place orders for supplies from the supplier.",
        "You need to predict demand for all the items in the store using the 'predict demand' tool.",
        "List of item IDs: [1,2,3,4,5,6,7,8,9,10].",
        "Provide the predicted demand values in a table format.", ##
        "Retrieve the available stock quantity for each item.",
        "Provide the available stock quantity values in a table format.", ##
        "Restructure the item id, available stock quantity values and predicted demand values into a json format. Also include the required quantity as the difference between demand and stock."
        "For each of the 10 item IDs compare available stock and predicted demand value obtained from previous tool calls using 'is_demand_greater' tool. If demand is found to be greater than stock available, display it.",
        
        #"For items where demand exceeds stock, retrieve the supplier email ID using the 'get_supplier_email_id' tool.",
        #"Consolidate orders by supplier email ID, listing item IDs and required quantities.",
        #"For each supplier, send an order email using the 'send_email' tool."
        ],

    show_tool_calls=True,
    debug_mode=True,
    markdown=True,

)


email_agent = Agent(
    name="Email Retreiver Agent",
    model=gemini_model,
    tools=[
        get_supplier_email_id,
        em.send_email,
    ],
    instructions=[
        "For the item_ids retrieve the supplier email ID using the 'get_supplier_email_id' tool and display them.",
        "Consolidate orders by supplier email ID, listing item IDs and required quantities.",
        "For each supplier, send an order email using the 'send_email' tool.",
    ],
    show_tool_calls=True,
    debug_mode=True,
    markdown=True,
)



orchestrator_agent = Agent(
    name="Orchestrator Agent",
    model=gemini_model,
    team=[
        inventory_agent,
        email_agent,
    ],
    instructions=[
        "Use the Inventory Agent to predict demand for all items, get available stock, find requirement.",
        "Pass this data with item ids only where demand greater than stock to the Email Retreiver Agent in this format to retreive required supplier mail ids."
    ],
    show_tool_calls=True,
    debug_mode=True,
    markdown=True,
    add_transfer_instructions=True,
) 

query = "Follow the instructions given"
try:
    response = orchestrator_agent.run(query)
    if response and hasattr(response, "content"):
        print(response)
    else:
        print("Error: Response content is missing or invalid.")
except Exception as e:
    print(f"Error occurred while running the agent: {e}")



