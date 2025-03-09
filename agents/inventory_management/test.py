from phi.agent import Agent
from phi.model.google import Gemini
import helpers.demand_prediction as dp

gemini_model = Gemini(id="gemini-1.5-flash")

demand_prediction_agent = Agent(
    name="Demand Prediction Agent",
    model=gemini_model,
    tools=[dp.predict_demand],
    instructions=[
        "Predict demand for all items in the store using the 'predict_demand' tool.",
        "List of item IDs: [1,2,3,4,5,6,7,8,9,10].",
        "Provide the predicted demand values in a table format."
    ],
    show_tool_calls=True,
    debug_mode=True,
    markdown=True,
)

from phi.agent import Agent
from phi.model.google import Gemini
import helpers.database_handler as db
import helpers.email_helper as em

conn = db.connect_to_db()
gemini_model = Gemini(id="gemini-1.5-flash")

def get_stock_quantity(item_id: int) -> int:
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT quantity FROM stock WHERE item_id = %s;", (item_id,))
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                print(f"No stock record found for item_id {item_id}")
                return None
    except Exception as e:
        print(f"Error retrieving stock quantity: {e}")
        return None

def get_supplier_email_id(item_id: int) -> str:
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT supplier_mail FROM stock WHERE item_id = %s;", (item_id,))
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                print(f"No record found for item_id {item_id}")
                return None
    except Exception as e:
        print(f"Error retrieving supplier email ID: {e}")
        return None

def is_demand_greater(stock: int, demand: int) -> bool:
    return demand > stock

order_management_agent = Agent(
    name="Order Management Agent",
    model=gemini_model,
    tools=[
        get_stock_quantity,
        is_demand_greater,
        get_supplier_email_id,
        em.send_email,
    ],
    instructions=[
        "Retrieve the available stock quantity for each item using the 'get_stock_quantity' tool.",
        "Compare available stock with predicted demand using the 'is_demand_greater' tool.",
        "If demand exceeds stock, retrieve the supplier email ID using the 'get_supplier_email_id' tool.",
        "Consolidate orders by supplier email ID, listing item IDs and required quantities.",
        "For each supplier, send an order email using the 'send_email' tool."
    ],
    show_tool_calls=True,
    debug_mode=True,
    markdown=True,
)

from phi.agent import Agent
from phi.model.google import Gemini

gemini_model = Gemini(id="gemini-1.5-flash")

orchestrator_agent = Agent(
    name="Orchestrator Agent",
    model=gemini_model,
    tools=[
        demand_prediction_agent,
        order_management_agent,
    ],
    instructions=[
        "Use the Demand Prediction Agent to predict demand for all items.",
        "Pass the predicted demand data to the Order Management Agent to manage stock and place orders as necessary."
    ],
    show_tool_calls=True,
    debug_mode=True,
    markdown=True,
)

query = "Manage inventory based on predicted demand and current stock levels."
try:
    response = orchestrator_agent.run(query)
    if response and hasattr(response, "content"):
        print(response.content)
    else:
        print("Error: Response content is missing or invalid.")
except Exception as e:
    print(f"Error occurred while running the orchestrator agent: {e}")
