import pandas as pd
from prophet import Prophet
from datetime import datetime
import pickle
import os
from pathlib import Path

# Directory to store models
MODEL_DIR = "prophet_models"
os.makedirs(MODEL_DIR, exist_ok=True)

sales_data = Path(__file__).parent.parent.parent / "data" / "filtered_sales_data.csv"
df = pd.read_csv(sales_data)

# Convert 'date' to datetime format
df['date'] = pd.to_datetime(df['date'])

# Get top 10 unique items
top_items = df['item_id'].unique()[:10]

# Dictionary to store trained models
trained_models = {}

# Train and save Prophet models for each item
for item_id in top_items:
    item_df = df[df['item_id'] == item_id].drop(columns=['item_id'])
    item_df = item_df.rename(columns={'date': 'ds', 'sales': 'y'})

    model = Prophet()
    model.fit(item_df)

    # Save model
    model_filename = os.path.join(MODEL_DIR, f"prophet_model_{item_id}.pkl")
    with open(model_filename, 'wb') as f:
        pickle.dump(model, f)
    
    trained_models[item_id] = model_filename

print("Models trained and saved successfully!")
