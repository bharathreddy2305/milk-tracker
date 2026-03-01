import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

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
             background-image: url("https://raw.githubusercontent.com/bharathreddy2305/milk-tracker/main/DairyFarmLogo.jpg");
             background-attachment: fixed;
             background-size: cover;
             background-position: center;
         }}
         .block-container {{
             background-color: rgba(255, 255, 255, 0.95);
             padding: 30px;
             border-radius: 15px;
             margin-top: 20px;
             box-shadow: 0 4px 6px rgba(0,0,0,0.1);
         }}
         h1, h2, h3, p, div, label, span {{
             color: #000000 !important;
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
def get_default_milk_info(cust_name):
    cust_lower = cust_name.lower()
    m_type = "Cow" if "cow" in cust_lower else "Buffalo"
    
    if "1 and 1/2" in cust_lower or "1.5" in cust_lower: qty = 1.5
    elif "1/2" in cust_lower or "500ml" in cust_lower or "500 ml" in cust_lower: qty = 0.5
    elif "750ml" in cust_lower or "750 ml" in cust_lower: qty = 0.75
    elif "250" in cust_lower: qty = 0.25
    elif "2lit" in cust_lower or "2l" in cust_lower: qty = 2.0
    elif "1.25" in cust_lower or "1lit 250ml" in cust_lower: qty = 1.25
    elif "1lit" in cust_lower or "1l" in cust_lower or "1 lit" in cust_lower: qty = 1.0
    else: qty = 1.0 # Default
    
    return m_type, qty

def load_data():
    try:
        df = pd.read_csv(DATA_FILE)
        if 'Date' in df.columns:
            df['Date'] = df['Date'].astype(str)
        return df
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

def delete_entry(index):
    df = load_data()
    df = df.drop(index)
    df.to_csv(DATA_FILE, index=False)
    return True

# --- APP CONFIG & LOGIN ---
st.set_page_config(page_title="Dharma Dairy", page_icon="🥛", layout="centered")
add_bg_from_url()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = ""

if not st.session_state.logged_in:
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
    with st.sidebar:
        st.write(f"👤 Role: **{st.session_state.role.upper()}**")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.role = ""
            st.rerun()

    with st.container():
        st.title("🥛 Daily Milk Tracker")

        if st.session_state.role == "worker":
            tabs = st.tabs(["📝 Worker Entry"])
            entry_tab = tabs[0]
            billing_tab = None
            manage_tab = None
            dash_tab = None
        else:
            tabs = st.tabs(["📝 Entry", "📲 Bill & Send", "🗑️ Manage", "📊 Dashboard"])
            entry_tab = tabs[0]
            billing_tab = tabs[1]
            manage_tab = tabs[2]
            dash_tab = tabs[3]

        # --- TAB 1: ENTRY ---
        with entry_tab:
            entry_mode = st.radio("Choose Entry Method:", 
                                  ["⚡ Smart Route", "Manual / Bulk Update", "📂 Upload Excel"], 
                                  horizontal=True)
            
            # --- METHOD 1: SMART ROUTE ---
            if entry_mode == "⚡ Smart Route":
                st.info("💡 Review the route. Uncheck anyone who didn't buy today. Quantities and Milk Types are auto-filled!")
                
                col_date, col_shift = st.columns(2)
                with col_date:
                    entry_date = st.date_input("Select Date", datetime.now())
                    date_str = entry_date.strftime("%Y-%m-%d")
                with col_shift:
                    route = st.radio("Shift:", ["Morning ☀️", "Evening 🌙"], horizontal=True)
                
                customer_dict = MORNING_CUSTOMERS if "Morning" in route else EVENING_CUSTOMERS
                
                default_data = []
                for cust in customer_dict.keys():
                    m_type, qty = get_default_milk_info(cust)
                    default_data.append({
                        "Log": True,
                        "Customer": cust,
                        "Type": m_type,
                        "Quantity": qty
                    })
                    
                df_route = pd.DataFrame(default_data)
                
                edited_df = st.data_editor(
                    df_route,
                    column_config={
                        "Log": st.column_config.CheckboxColumn("✅ Log?", default=True),
                        "Customer": st.column_config.Column("Customer", disabled=True),
                        "Type": st.column_config.SelectboxColumn("Milk Type", options=["Cow", "Buffalo", "Buffalo (Old)"]),
                        "Quantity": st.column_config.NumberColumn("Liters", step=0.25, format="%.2f")
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                to_save = edited_df[edited_df["Log"] == True]
                
                if st.button("🚀 Save Entire Route", type="primary", use_container_width=True):
                    for index, row in to_save.iterrows():
                        m_t = row["Type"]
                        rate = RATE_COW if m_t == "Cow" else (RATE_BUFFALO_OLD if m_t == "Buffalo (Old)" else RATE_BUFFALO)
                        save_entry(date_str, route, row["Customer"], m_t, rate, row["Quantity"])
                    st.success(f"Successfully logged {len(to_save)} entries for {date_str}!")

            # --- METHOD 2: MANUAL / BULK OVERRIDE ---
            elif entry_mode == "Manual / Bulk Update":
                st.write("---")
                date_mode = st.radio("Dates:", ["Single Day", "Date Range"], horizontal=True)
                
                if date_mode == "Single Day":
                    col_date, col_shift = st.columns(2)
                    with col_date:
                        entry_date = st.date_input("Select Date", datetime.now())
                        date_list = [entry_date]
                    with col_shift:
                        route = st.radio("Shift:", ["Morning ☀️", "Evening 🌙"], horizontal=True)
                else:
                    col_start, col_end = st.columns(2)
                    with col_start:
                        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=1))
                    with col_end:
                        end_date = st.date_input("End Date", datetime.now())
                    route = st.radio("Shift:", ["Morning ☀️", "Evening 🌙"], horizontal=True)
                    
                    date_list = []
                    if start_date <= end_date:
                        delta = end_date - start_date
                        for i in range(delta.days + 1):
                            date_list.append(start_date + timedelta(days=i))

                customer_dict = MORNING_CUSTOMERS if "Morning" in route else EVENING_CUSTOMERS
                
                st.write("#### 🔍 Filter Customers")
                f_col1, f_col2 = st.columns(2)
                with f_col1:
                    filter_type = st.selectbox("Filter by Default Type:", ["All", "Cow", "Buffalo"])
                with f_col2:
                    filter_qty = st.selectbox("Filter by Default Liters:", ["All", 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0])

                filtered_customers = []
                for cust in customer_dict.keys():
                    def_type, def_qty = get_default_milk_info(cust)
                    match_type = True if filter_type == "All" else (filter_type in def_type)
                    match_qty = True if filter_qty == "All" else (filter_qty == def_qty)
                    if match_type and match_qty:
                        filtered_customers.append(cust)
                
                selected_names = st.multiselect(
                    f"Select Customer(s) - Showing {len(filtered_customers)} matches:", 
                    list(customer_dict.keys()), 
                    default=filtered_customers
                )
                
                st.write("#### ✏️ Update Details")
                c1, c2 = st.columns(2)
                with c1:
                    milk_option = st.radio(
                        "Actual Milk Type & Rate to Log:", 
                        [f"Cow (Rs {RATE_COW})", f"Buffalo (Rs {RATE_BUFFALO})", f"Buffalo OLD (Rs {RATE_BUFFALO_OLD})"]
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
                    qty = st.radio("Actual Quantity (Liters) to Log:", [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0])

                if st.button("✅ Save Selected Customers", type="primary", use_container_width=True):
                    if not selected_names:
                        st.error("Please select at least one customer.")
                    elif not date_list:
                        st.error("Invalid Date Range")
                    else:
                        total_saves = 0
                        for s_name in selected_names:
                            for d in date_list:
                                save_entry(d.strftime("%Y-%m-%d"), route, s_name, m_type, rate, qty)
                                total_saves += 1
                        st.success(f"Successfully saved {total_saves} total entries!")

            # --- METHOD 3: UPLOAD EXCEL ---
            elif entry_mode == "📂 Upload Excel":
                st.info("Upload an Excel (.xlsx) or CSV file to add multiple records instantly.")
                uploaded_file = st.file_uploader("Choose a file", type=['xlsx', 'csv'])
                
                if uploaded_file is not None:
                    try:
                        if uploaded_file.name.endswith('.csv'):
                            df_new = pd.read_csv(uploaded_file)
                        else:
                            df_new = pd.read_excel(uploaded_file)
                        
                        req_cols = ["Date", "Route", "Customer", "Type", "Rate", "Quantity"]
                        
                        if all(col in df_new.columns for col in req_cols):
                            st.dataframe(df_new.head())
                            if st.button("💾 Save Uploaded Data to App", type="primary"):
                                df_new['Date'] = pd.to_datetime(df_new['Date']).dt.strftime('%Y-%m-%d')
                                df_new['Time'] = datetime.now().strftime("%H:%M:%S")
                                df_new['Total_Price'] = df_new['Rate'] * df_new['Quantity']
                                df_final = df_new[["Date", "Time", "Route", "Customer", "Type", "Rate", "Quantity", "Total_Price"]]
                                existing_df = load_data()
                                combined_df = pd.concat([existing_df, df_final], ignore_index=True)
                                combined_df.to_csv(DATA_FILE, index=False)
                                st.success(f"✅ Successfully added {len(df_new)} records!")
                                st.balloons()
                        else:
                            st.error(f"❌ Your file is missing some columns. Please ensure it has exactly: {', '.join(req_cols)}")
                    except Exception as e:
                        st.error(f"Error reading file. Details: {e}")

        # --- TAB 2: RAPID-FIRE BILLING ---
        if billing_tab:
            with billing_tab:
                st.header("📲 Rapid-Fire Billing")
                df = load_data()
                
                if not df.empty:
                    # Sort months so the newest is at the top
                    all_months = sorted(df['Date'].apply(lambda x: x[:7]).unique(), reverse=True)
                    selected_month = st.selectbox("Select Month to Bill", all_months)
                    
                    monthly_data = df[df['Date'].str.contains(selected_month)]
                    
                    if not monthly_data.empty:
                        bill_summary = monthly_data.groupby("Customer").agg({
                            'Quantity': 'sum',
                            'Total_Price': 'sum'
                        }).reset_index()
                        
                        st.write(f"### 📋 Checklist for {selected_month}")
                        
                        ALL_CUSTOMERS = {**MORNING_CUSTOMERS, **EVENING_CUSTOMERS}
                        
                        # --- PROGRESS TRACKING LOGIC ---
                        chk_prefix = f"sent_{selected_month}_"
                        total_bills = len(bill_summary)
                        
                        # Count how many checkboxes are currently marked True for this month
                        sent_count = sum(1 for key in st.session_state.keys() if key.startswith(chk_prefix) and st.session_state[key])
                        
                        # Display Progress Bar
                        progress = sent_count / total_bills if total_bills > 0 else 0
                        st.progress(progress)
                        st.write(f"**Progress:** {sent_count} of {total_bills} Sent")
                        st.divider()

                        # --- RENDER BILLS ---
                        for index, row in bill_summary.iterrows():
                            name = row['Customer']
                            liters = row['Quantity']
                            amount = int(row['Total_Price'])
                            phone = ALL_CUSTOMERS.get(name, "")
                            
                            chk_key = f"{chk_prefix}{name}"
                            
                            # Initialize checkbox state if it doesn't exist
                            if chk_key not in st.session_state:
                                st.session_state[chk_key] = False

                            c1, c2, c3 = st.columns([3, 2, 1])
                            
                            with c1:
                                # Strikethrough if done
                                if st.session_state[chk_key]:
                                    st.write(f"~~**{name}**~~ ✅")
                                else:
                                    st.write(f"**{name}**")
                                st.caption(f"Total: {liters}L | Bill: Rs. {amount}")
                                
                            with c2:
                                if phone and len(phone) > 5:
                                    msg = f"Hello {name}, your milk bill for {selected_month} is Rs. {amount} ({liters} Liters). Please pay via UPI."
                                    whatsapp_url = f"https://wa.me/{phone}?text={msg.replace(' ', '%20')}"
                                    st.link_button("📲 Send WhatsApp", whatsapp_url, use_container_width=True)
                                else:
                                    st.write("⚠️ No Phone")
                                    
                            with c3:
                                # The checkbox itself
                                st.checkbox("Done", key=chk_key)
                                
                            st.divider()
                else:
                    st.info("No data recorded yet.")

        # --- TAB 3: MANAGE RECORDS ---
        if manage_tab:
            with manage_tab:
                st.header("🗑️ Manage Records")
                m_date = st.date_input("Filter by Date:", datetime.now())
                m_date_str = m_date.strftime("%Y-%m-%d")
                df = load_data()
                
                if not df.empty:
                    daily_data = df[df['Date'] == m_date_str]
                    if not daily_data.empty:
                        for index, row in daily_data.iterrows():
                            col1, col2, col3 = st.columns([3, 2, 1])
                            with col1:
                                st.write(f"**{row['Customer']}**")
                            with col2:
                                st.write(f"{row['Quantity']}L - Rs.{row['Total_Price']}")
                            with col3:
                                if st.button("Delete", key=f"del_{index}"):
                                    delete_entry(index)
                                    st.rerun()
                        st.divider()

        # --- TAB 4: DASHBOARD ---
        if dash_tab:
            with dash_tab:
                st.header("📊 Business Analytics")
                df = load_data()

                if not df.empty:
                    all_months = df['Date'].apply(lambda x: x[:7]).unique()
                    dash_month = st.selectbox("Select Month for Analysis:", all_months)
                    m_df = df[df['Date'].str.contains(dash_month)]
                    
                    if not m_df.empty:
                        total_revenue = m_df['Total_Price'].sum()
                        total_liters = m_df['Quantity'].sum()
                        avg_daily = total_revenue / m_df['Date'].nunique()
                        
                        k1, k2, k3 = st.columns(3)
                        k1.metric("💰 Revenue", f"Rs. {int(total_revenue)}")
                        k2.metric("🥛 Volume", f"{total_liters} L")
                        k3.metric("📅 Avg/Day", f"Rs. {int(avg_daily)}")
                        
                        st.divider()
                        c1, c2 = st.columns(2)
                        with c1:
                            st.bar_chart(m_df['Type'].value_counts())
                        with c2:
                            st.line_chart(m_df.groupby('Date')['Total_Price'].sum())

                        st.divider()
                        st.subheader("🏆 Top Customers")
                        st.bar_chart(m_df.groupby('Customer')['Total_Price'].sum().sort_values(ascending=False).head(5))
