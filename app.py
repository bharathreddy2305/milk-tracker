import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
# This file stores the data
DATA_FILE = 'milk_records.csv'
MILK_RATE_PER_LITER = 90 

# YOUR CUSTOMERS (Update these names and numbers!)
# Format: "Name": "919999999999" (Must have 91 for India)
CUSTOMERS = {
    "Bharath": "919666496078", 
    "Sita": "919988776655",
    "Ramesh": "911234567890"
}

# --- FUNCTIONS ---
def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Customer", "Quantity_Liters"])

def save_entry(customer, quantity):
    df = load_data()
    new_entry = pd.DataFrame({
        "Date": [datetime.now().strftime("%Y-%m-%d")],
        "Customer": [customer],
        "Quantity_Liters": [quantity]
    })
    # Append the new entry
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    return True

# --- APP LAYOUT ---
st.set_page_config(page_title="Milk Tracker", page_icon="🥛")
st.title("🥛 Daily Milk Tracker")

# Tabs for the two different jobs
tab1, tab2 = st.tabs(["Worker (Daily Entry)", "Owner (End of Month)"])

# --- WORKER TAB ---
with tab1:
    st.header("📝 New Entry")
    # 1. Select Name
    selected_customer = st.selectbox("Select Customer", list(CUSTOMERS.keys()))
    
    # 2. Select Amount
    quantity = st.radio("How much milk?", [0.5,0.75, 1.0,1.25, 1.5,1.75, 2.0,2.25,2.5,2.75, 3.0], horizontal=True)
    
    # 3. Save Button
    if st.button("✅ Save Entry", type="primary"):
        save_entry(selected_customer, quantity)
        st.success(f"Saved {quantity}L for {selected_customer}!")

# --- OWNER TAB ---
with tab2:
    st.header("💰 Generate Bills")
    
    # Show data table
    df = load_data()
    
    if not df.empty:
        st.dataframe(df.tail(5)) # Show last 5 entries
        
        if st.button("Calculate Monthly Bills"):
            # Math logic
            bill_summary = df.groupby("Customer")["Quantity_Liters"].sum().reset_index()
            bill_summary["Total_Bill"] = bill_summary["Quantity_Liters"] * MILK_RATE_PER_LITER
            
            st.write("---")
            for index, row in bill_summary.iterrows():
                name = row['Customer']
                liters = row['Quantity_Liters']
                amount = int(row['Total_Bill'])
                phone = CUSTOMERS.get(name)
                
                # WhatsApp Logic
                msg = f"Hello {name}, your milk bill for this month is Rs. {amount} for {liters} Liters. Please pay via UPI."
                whatsapp_url = f"https://wa.me/{phone}?text={msg.replace(' ', '%20')}"
                
                # Layout for each person
                c1, c2 = st.columns([2, 1])
                c1.write(f"**{name}**: Rs. {amount}")
                c2.link_button(f"📲 WhatsApp", whatsapp_url)
    else:
        st.info("No records found yet.")
