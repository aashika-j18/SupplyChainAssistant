import pandas as pd
import pickle
from datetime import datetime
import math
import os

MODEL_DIR = r"C:\Users\Aashi\Documents\Co-curricular\hackathons\ggh\SupplyChainAssistant\agents\inventory_management\helpers\prophet_models"

def predict_demand(item_id: int) -> dict:
    """
    Use this function to predict the total demand for a specific item over the next 30 days using a pre-trained Prophet model.

    Args:
        item_id (int): The unique identifier of the item for which demand prediction is required. It is of integer type.

    Returns:
        int: The ceil value of total predicted demand for the next 30 days.
             Returns -1 if no trained model is found for the specified item_id.
    """


    model_path = os.path.join(MODEL_DIR, f"prophet_model_{item_id}.pkl")
    
    print(model_path)
    if not os.path.exists(model_path):
        print(f"No trained model found for item {item_id}")
        return -1
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    today = datetime.today()
    future = pd.DataFrame({'ds': pd.date_range(start=today, periods=30, freq='D')})
    forecast = model.predict(future)
    next_30_days = forecast[['ds', 'yhat']].rename(columns={'ds': 'date', 'yhat': 'predicted_demand'})
    next_30_days['date'] = next_30_days['date'].dt.date
    total_predicted_demand = math.ceil(next_30_days['predicted_demand'].sum())

    return  str({"predicted_demand": total_predicted_demand})
    
