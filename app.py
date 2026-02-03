import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
DATA_FILE = 'milk_records.csv'

# Rates
RATE_COW = 80
RATE_BUFFALO = 90
RATE_BUFFALO_OLD = 80

# --- BACKGROUND IMAGE FUNCTION ---
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://i.imgur.com/Q7vGj3s.png");
             background-attachment: fixed;
             background-size: cover;
         }}
         /* Make main container slightly transparent to see bg */
         .main {{
             background-color: rgba(255, 255, 255, 0.85);
             padding: 20px;
             border-radius: 10px;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# --- CUSTOMER DATA ---
MORNING_CUSTOMERS = {
    "Beside Mashook - 750ml Buff": "918247844925",
    "Beside muslim suggested - 1lit buff": "",
    "Jyothi akka - 1lit buff": "918186854678",
    "New Arvind Nag Rd2(NE) - 2lit buff": "919390516904",
    "Naveen Arvind Nag Rd-2 - 1.5lit": "",
    "Shesi_Gundu near Shivaji - 1lit Buff": "919886046756",
    "Beside shesi_Shivaji - 1lit Buff": "919010208055",
    "Tiwari 1st(shailender) - 1lit Cow": "918790993828",
    "Tiwari 2(Ranjith) - 1lit Cow": "918790993815",
    "Satyanarayana Relative - 1/2Lit Buffalo": "919182193470",
    "Satyanarayana S Laxmi - 1.5Lit Buffalo": "918688634753",
    "Satyanarayana RoadNo 10 - 1Lit Buffalo": "918555878936",
    "Venkat Reddy colony lane1 (1/2 lit Buff)": "919701357468",
    "Anitha atha - 1/2lit lit buff": "919666039979",
    "cm rao colony new relative(1 lit buff)": "918978530590",
    "cm rao colony new (1 lit buff)": "919701378590",
    "Eswar reddy cm suresh": "919000538623",
    "Cm Suresh - 1Lit Buff": "919000545557",
    "cm rao colony last opp - cow 1lit": "917702305015",
    "Venkat Reddy colony lane2 (1 lit Buff)": "916302670850",
    "Venkatesh Shop Backside - 1lit Cow": "918328293326",
    "Modi 501 - 1Lit Cow and 1/2 Buff": "919701084753",
    "Sid Dad - 1/2Lit Buff": "919100556681",
    "Rishi Mother - 1/2Lit Buff": "919440671576",
    "Poojari - 302 -1/2Lit Cow": "919490318827",
    "Modi 208 - 1Lit Cow": "919449545510",
    "Modi 203 - 1/2lit Buff": "",
    "Modi 1C 1st floor - 1/2 cow": "",
    "Vinod Ice_Cream D105 - 1lit Buff": "",
    "sai shilpa 103 - 1/2Lit Cow": "919482040034",
    "sai shilpa 203 - 1/2Lit Buff": "917569071817",
    "sai shilpa - 201 - 1Lit Buff": "919959917160",
    "Medha 502 - 1/2Lit Cow": "917799477477",
    "Medha 509(1/2 lit Buff)": "919346207119",
    "Medha 309 -(500ml cow)": "918790244355",
    "Medha G1 - 1/2Lit Buff": "916304487419",
    "Medha 204 - 1Lit Buff(Special)": "919666079666",
    "Medha 110 - 1/2Lit": "919110546980",
    "Beside Medha - 1/2lit cow": "919618558104",
    "Manikanta Nilayam 3rd - 1Lit Buff": "919703401903",
    "vidha 1lit cow": "917995510555",
    "Viswa sai 301 - 1.5lit": "918588062241",
    "Viswa sai 303 - 1/2": "918074898248",
    "Viswa sai 504 - 1lit 250ml": "919966126689",
    "kamlakar Reddy (750ml)": "919985560068",
    "above kamlakar - 1/2lit buff": "",
    "Avenue 107 - 1Lit Cow": "917873345336",
    "Avenue 810 - 1/2Lit Cow": "918374530052",
    "Above Blade shop - 1lit Buff": "918950297679",
    "kakthiya 302  - 1/2L Buff": "919010844486",
    "KYR Pradeep 203 - 1/2Lit Cow": "919952696488",
    "Beside Rockstar hair sampath - 1/2Lit Buff": "917075805465",
    "Havisa BackSide - 1.5 lit Buff": "919898600681",
    "shanthinikethan -114 - 1/2lit Buff": "917013891869",
    "shanthinikethan -213 - 1lit Buff": "919985922722",
    "shanthinikethan -314 - 1lit Buff": "91950295071",
    "Modi Care - 1Lit Cow": "919032625666",
    "Shoba Aunty - 1/2 lit buff": "919948314549",
    "Vicky - 1.5Lit Buff": "917207302626",
    "Rampally circle  - 1/2L -cow": "",
    "Hospital Back Laxmi - 1/2Lit Buff": "919640913321",
    "Hospital Back 5th Left - 500ml Buff": "919491380759",
    "Hospital Back 3rd - 1.5Lit Buff": "917989012995",
    "Hospital Back 2nd Left - 1lit Buff": "918143482483",
    "Hospital Back 2nd Right - 1Lit Buff": "919652198919",
    "vani beside tution aunty - 250 ml": "919949377946",
    "tution aunty - 1/2 lit cow": "919052057652"
}

EVENING_CUSTOMERS = {
    "1. Naresh Beside Shed - 1.5L Buff": "918074350032",
    "2. Saritha Beside shed - 1/2L cow": "916302337959",
    "3. Sai Durga Nagraj - 1/2L Buff": "",
    "4. Sanjeev Kumar - 1.5 Lit Cow": "918790993825",
    "5. Srinivas Co Brother - 1/2 lit buff": "919985357947",
    "6. Kirana Shop - 1/2L Buff": "918187079495",
    "7. Rubin - 1L Buff": "919866043585",
    "8. Srikanth Bava - 1/2L Cow": "919912221373",
    "panthulu opp road - 1/2 buff": "",
    "9. Ration shop aunty - 1/2L Buff": "919346991329",
    "10. Vanitha Ration shop - 1/2L Buff": "919652302438",
    "12. Dancer Srinivas- 1L Buff": "919989352523",
    "13. Mestiri Dancer - 1/2L Cow": "918121727023",
    "14. Murthi Ravindra Nag- 1.5L Buff": "917032916617",
    "16. Ravi Kumar Evng - 1/2L Buff": "919885656308",
    "17. PremKumar - 1lit Buff": "917794898083",
    "18. Gangayya - 1L Buff": "919985676879",
    "19. Nethaji Nagar - 1.5L Buff": "919010729485",
    "20. Prashanth Nag - 1/2L - Anjali": "919676138066",
    "21. Prashanth Nag 1/2L -Swapna": "919912274789",
    "22. Nalini Aunty 202 - 1/2L Buff": "91705705783",
    "23. Nalini Aunty 302 - 1/2L Buff": "919398869892",
    "25. Upender uncle - 1L Buff": "919949627575",
    "26. Gold Shop - 2L Buff": "919866916008",
    "27. Gandhi gold shop - 1/2L buff": "918333853319",
    "28. Vardan Reddy - 1L Buff": "919398629596",
    "30. beside Vardan new Down 1/2lit Buff": "918008812844",
    "32. Mounik Reddy - 1L- Down": "918121206243",
    "33. Vijay Hos Back - 1/2L": "919059712115",
    "Raju Krishna Pedda Reddy - 1/2lit Buff": "919515941775",
    "34. Pavan - 1/2L": "918801550473",
    "35. Uma Pavan - 1/2L": "918885027310",
    "36. Praveen -750mL": "919394811248",
    "37. Avinash anna- (1.25L Buff & 1/2 Cow)": "91900990660",
    "Avinash worker - (1/2lit buff)": "",
    "Avinash anna accountant - 1/2L Buff": "",
    "39. Opp mohan Last - 1/2L Buff": "916306266750",
    "40. Mohan Above 3rd": "919392482252",
    "41. Mohan Floor 1st": "919177132826",
    "43. Paramount - 423 -1L": "919704038866",
    "44. Beside Chandhu - 1/2L": "918333011862",
    "45. Chandhu - 1L": "919989819195"
}

# --- FUNCTIONS ---
def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Time", "Route", "Customer", "Type", "Rate", "Quantity", "Total_Price"])

def save_entry(selected_date_str, route, customer, milk_type, rate, quantity):
    df = load_data()
    total = rate * quantity
    new_entry = pd.DataFrame({
        "Date": [selected_date_str],
        "Time": [datetime.now().strftime("%H:%M:%S")],
        "Route": [route],
        "Customer": [customer],
        "Type": [milk_type],
        "Rate": [rate],
        "Quantity": [quantity],
        "Total_Price": [total]
    })
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    return True

# --- APP CONFIG & LOGIN ---
st.set_page_config(page_title="Dharma Dairy Tracker", page_icon="🥛")

# **Apply Background Image**
add_bg_from_url()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = ""

if not st.session_state.logged_in:
    # Login Screen Container with white background
    with st.container():
        st.title("🔒 Dharma Dairy Login")
        user_id = st.text_input("User ID")
        user_pass = st.text_input("Password", type="password")
        
        if st.button("Login", type="primary"):
            if user_id == "worker" and user_pass == "1101":
                st.session_state.logged_in = True
                st.session_state.role = "worker"
                st.rerun()
            elif user_id == "owner" and user_pass == "2305":
                st.session_state.logged_in = True
                st.session_state.role = "owner"
                st.rerun()
            else:
                st.error("❌ Incorrect ID or Password")

else:
    # --- LOGGED IN APP ---
    # Sidebar for Logout
    with st.sidebar:
        st.write(f"👤 Role: **{st.session_state.role.upper()}**")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.role = ""
            st.rerun()

    # Main App Container with white background
    with st.container():
        st.title("🥛 Daily Milk Tracker")

        # DEFINE TABS BASED ON ROLE
        if st.session_state.role == "worker":
            tabs = st.tabs(["📝 Worker Entry"])
            entry_tab = tabs[0]
            billing_tab = None
        else:
            # Owner sees everything
            tabs = st.tabs(["📝 Worker Entry", "💰 Bill & WhatsApp"])
            entry_tab = tabs[0]
            billing_tab = tabs[1]

        # --- TAB 1: ENTRY (Visible to Worker & Owner) ---
        with entry_tab:
            # DATE PICKER
            col_date, col_shift = st.columns(2)
            with col_date:
                entry_date = st.date_input("Select Date", datetime.now())
                date_str = entry_date.strftime("%Y-%m-%d")
            with col_shift:
                route = st.radio("Shift:", ["Morning ☀️", "Evening 🌙"], horizontal=True)
            
            # Load Customers
            if "Morning" in route:
                customer_dict = MORNING_CUSTOMERS
            else:
                customer_dict = EVENING_CUSTOMERS
                
            selected_name = st.selectbox("Select Customer:", list(customer_dict.keys()))
            
            c1, c2 = st.columns(2)
            with c1:
                # Auto-select milk type
                type_index = 0
                if "Cow" in selected_name or "cow" in selected_name:
                    type_index = 0
                elif "Buff" in selected_name or "buff" in selected_name:
                    type_index = 1
                    
                milk_option = st.radio(
                    "Milk Type & Rate:", 
                    [f"Cow (Rs {RATE_COW})", f"Buffalo (Rs {RATE_BUFFALO})", f"Buffalo OLD (Rs {RATE_BUFFALO_OLD})"],
                    index=type_index
                )
                
                if "Cow" in milk_option:
                    rate = RATE_COW
                    m_type = "Cow"
                elif "OLD" in milk_option:
                    rate = RATE_BUFFALO_OLD
                    m_type = "Buffalo (Old)"
                else:
                    rate = RATE_BUFFALO
                    m_type = "Buffalo"

            with c2:
                qty = st.radio("Quantity (Liters):", [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0])

            final_price = rate * qty
            st.info(f"Adding for **{date_str}**: Rs. {int(final_price)}")
            
            if st.button("✅ Save Entry", type="primary", use_container_width=True):
                save_entry(date_str, route, selected_name, m_type, rate, qty)
                st.success(f"Saved for {date_str}: {selected_name} | {qty}L")

        # --- TAB 2: BILLING (Only if Owner) ---
        if billing_tab:
            with billing_tab:
                st.header("Monthly Bill Generator")
                df = load_data()
                
                if not df.empty:
                    all_months = df['Date'].apply(lambda x: x[:7]).unique()
                    selected_month = st.selectbox("Select Month", all_months)
                    
                    monthly_data = df[df['Date'].str.contains(selected_month)]
                    
                    if st.button("Calculate Bills"):
                        bill_summary = monthly_data.groupby("Customer").agg({
                            'Quantity': 'sum',
                            'Total_Price': 'sum'
                        }).reset_index()
                        
                        st.write(f"### Bills for {selected_month}")
                        ALL_CUSTOMERS = {**MORNING_CUSTOMERS, **EVENING_CUSTOMERS}
                        
                        for index, row in bill_summary.iterrows():
                            name = row['Customer']
                            liters = row['Quantity']
                            amount = int(row['Total_Price'])
                            phone = ALL_CUSTOMERS.get(name, "")
                            
                            if phone and len(phone) > 5:
                                msg = f"your milk bill for {selected_month} is Rs. {amount} ({liters} Liters). Please pay via UPI(Google pay or phonepay)-9392182569 Ghanapuram Dharma Reddy and Share the Screenshot."
                                whatsapp_url = f"https://wa.me/{phone}?text={msg.replace(' ', '%20')}"
                                link_text = "📲 Send WhatsApp"
                                valid_link = whatsapp_url
                            else:
                                link_text = "⚠️ No Phone Number"
                                valid_link = "#"

                            # Individual Card for each customer
                            st.divider()
                            c1, c2 = st.columns([3, 1])
                            c1.write(f"**{name}**")
                            c1.caption(f"Total: {liters}L | Bill: Rs. {amount}")
                            if valid_link != "#":
                                c2.link_button(link_text, valid_link)
                            else:
                                c2.write(link_text)
                                
                else:
                    st.info("No data recorded yet.")
