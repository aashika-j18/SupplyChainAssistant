# SupplyChainAssistant
Google Girl Hackathon '25

## Overview    
This repository contains the codebase and documentation for an **AI-driven supply chain management assistant** designed to **optimize procurement and inventory management** for enterprises. The solution integrates **conversational AI, demand forecasting models, and intelligent process automation** to improve efficiency, reduce costs, and enhance sustainability in supply chain operations.  
By leveraging **machine learning, NLP, agentic AI and real-time data processing**, the system enhances **supplier negotiations, stock monitoring, and demand predictions**, helping businesses streamline operations, **reduce waste, and improve decision-making.**  

### **Key Challenges:**  
In many enterprises, supply chain management processes are **repetitive, time-consuming, and inefficient** when handled manually.  
1. **Supplier Communication:** Manual price negotiations are slow and delay the supply chain.  
2. **Inventory Reordering:** Manual stock level checks are inefficient and error-prone.  
3. **Demand Forecasting:** Forecasting demand manually can result in **overstocking (waste) or understocking (loss of sales).**  

### **Proposed Solution:**  
We introduce a **team of AI agents** to streamline supply chain operations:  

- **Conversational AI Agent** (Procurement)  
  - Negotiates with suppliers by analyzing **historical deals, current offers, and market trends.**  
  - Automates supplier communication, reducing manual effort and improving efficiency.  

- **Demand Forecasting AI Agent** (Inventory Management)  
  - Uses **machine learning models** to predict demand based on **historical and real-time data.**  
  - Automates **inventory replenishment** to prevent overstocking and shortages.  

---

## **Solution Approach**  

1. **Conversational AI for Procurement Negotiation**  
   - Uses **Gemini API** for intelligent supplier communication.  
   - Analyzes **pricing trends and past contracts** to recommend optimal negotiation strategies.  

2. **Machine Learning-Based Demand Forecasting**  
   - Uses **time series models (Prophet)** for demand prediction.  
   - Tracks stock levels and **automatically recommends reorders** when needed.  

3. **UI**  
   - **Streamlit**: Provides an interactive frontend for negotiation and communication.  

---

## **Results**
![image](https://github.com/user-attachments/assets/5677b28d-6522-44c2-b6cb-95f464e0679c)

### Link to view demo video: https://github.com/aashika-j18/SupplyChainAssistant/issues/1

---

## **Getting Started**  

### **1. Clone the Repository**  
```sh
git clone https://github.com/aashika-j18/SupplyChainAssistant.git
```

### **2. Navigate into the project directory**
```sh
cd SupplyChainAssistant
```
### **3. Set Up Environment Variables**
Create a .env file in the project root and add:
```sh
GOOGLE_API_KEY=your-api-key

DB_NAME=db-name
DB_USER=db-user
DB_PASSWORD=your-db-password
DB_HOST=db-host
DB_PORT=db-port

EMAIL_SENDER=your-mail-id
EMAIL_PASSWORD=your-app-password
```


### **4. Install Dependencies**
Ensure python3 is installed and run the following:
```sh
pip install -r requirements.txt  
```

### **5a. Run the negotiation agent chat interface:**

```sh
cd agents\negotiation_agent
python -m streamlit run negotiation_ui.py  
```

### **5b. Run the inventory management agent:**

```sh
cd agents\inventory_management
python inventory_agent.py
```

