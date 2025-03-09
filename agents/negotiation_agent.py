import os
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.csv_tools import CsvTools
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai 

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


gemini_model = Gemini(id="gemini-1.5-flash")


historical_data_path = Path('data\cleaned_po_history_data.csv')  ###
csv_tools = CsvTools(csvs=[historical_data_path])


negotiation_agent = Agent(
    name="Supplier Negotiation Agent",
    model=gemini_model,
    tools=[
        DuckDuckGo(),
        csv_tools,
    ],
    instructions=[
        "You are the store owner that needs to place orders for supplies from the supplier.",
        "You only expect input as supplier offer for an item.",
        "Analyze current supplier offers.",
        "You can query the historical data csv to compare with historical contracts.",
        "You can compare industry benchmarks by browsing online using duckduckgo.",
        "Do negotiation.",
        "Try to bring down the price offered by showing statistics and competitive prices provided by other suppliers. These other suppliers should include mostly wholesale and not retail.",
        "Consider only Indian suppliers.",
        "If the price is already low, then mention about being happy to accept the offer."
        "Always include sources as citations in your responses.",
        "Always tabulate data.",
        "Use search to perform all instructions",
        "Use a gentle tone always",
    ],
    markdown=True
)

