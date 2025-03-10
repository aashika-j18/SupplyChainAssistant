import os
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.googlesearch import GoogleSearch
from phi.tools.csv_tools import CsvTools
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai 

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


gemini_model = Gemini(id="gemini-1.5-flash")


historical_data_path = Path(r'data\cleaned_po_history_data.csv') 
csv_tools = CsvTools(csvs=[historical_data_path])


negotiation_agent = Agent(
    name="Supplier Negotiation Agent",
    model=gemini_model,
    tools=[
        DuckDuckGo(),
        GoogleSearch(),
        csv_tools,
    ],
    instructions=[
        "You are the store owner that needs to place orders for supplies from the supplier.",
        "You only expect input as supplier offer for an item.",
        "You are directly talking to the supplier. Give response accordingly.",
        "Choose the most suitable response and give output.",
        "Don't make assumptions.",
        "Analyze current supplier offers.",
        "You can query (simple) the historical data csv to compare with historical contracts.",
        "CSV Data Columns Explained:",
        "- `item_id`: Unique identifier of the item ordered.",
        "- `item`: Name of the item ordered.",
        "- `quantity`: Number of units purchased.",
        "- `price`: Price per unit.",
        "- `date`: Date of order.",
        "You can compare industry benchmarks by browsing online using google search.",
        "Do negotiation. Refer online for smart negotiation tactics.",
        "Try to bring down the price offered by showing statistics and competitive prices provided by other suppliers. These other suppliers should include mostly wholesale and not retail.",
        "Consider only Indian suppliers.",
        "If the price is already low, then mention about being happy to accept the offer."
        "Always include sources as citations in your responses.",
        "Always tabulate data.",
        "Use search to perform all instructions",
        "Use a gentle tone always",
        "Be straight to the point.",
    ],
    markdown=True,
    debug_mode=True,
    show_tool_calls=True,
)

