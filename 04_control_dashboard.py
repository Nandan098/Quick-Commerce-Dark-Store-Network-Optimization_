import streamlit as st
import sqlite3
import pandas as pd
import folium
from streamlit_folium import folium_static

# --- UI Configuration ---
st.set_page_config(page_title="Flipkart DMAIC Control Tower", layout="wide")

st.title("Quick Commerce Dark Store Network Optimization")

# --- Database Fetching ---
def fetch_control_data():
    conn = sqlite3.connect('flipkart_lean_network.db')
    competitors = pd.read_sql("SELECT * FROM competitor_stores", conn)
    proposed = pd.read_sql("SELECT * FROM improved_network_plan", conn)
    # Fetch a sample of customer orders for map rendering (e.g., 1000 points to keep map fast)
    orders = pd.read_sql("SELECT Customer_Lat, Customer_Lon, Order_Value_INR, Order_Hour FROM customer_orders LIMIT 1500", conn)
    conn.close()
    return competitors, proposed, orders

df_comp, df_proposed, df_orders = fetch_control_data()

# --- Sidebar Controls (Control Plan Parameters) ---
st.sidebar.header("Operational Control Limits")
sla_radius = st.sidebar.slider(
    "Critical-to-Quality (CTQ): Delivery Radius (km)", 
    min_value=1.5, max_value=3.5, value=2.0, step=0.1,
    help="2.0 km represents standard 10-minute SLA coverage in urban density."
)

st.sidebar.markdown("---")
st.sidebar.header("Map Layer Toggles")
show_orders = st.sidebar.checkbox("Show Customer Demand Pins", value=False)
show_zepto = st.sidebar.checkbox("Overlay Zepto Map", value=True)
show_blinkit = st.sidebar.checkbox("Overlay Blinkit Map", value=False)
show_instamart = st.sidebar.checkbox("Overlay Instamart Map", value=False)

# --- Executive KPI Cards (Lean & Six Sigma Metrics) ---
col1, col2, col3, col4 = st.columns(4)

total_rent = df_proposed['Monthly_CapEx_INR'].sum()
total_orders = df_proposed['Peak_Order_Volume'].sum()
defects = len(df_proposed[df_proposed['Six_Sigma_Defect_Flag'] == 'Defect: Over Capacity'])

col1.metric("Lean Metric: Proposed Hubs", f"{len(df_proposed)} Hubs")
col2.metric("Financial: Total Monthly CapEx", f"₹{total_rent:,.0f}")
col3.metric("Lean Metric: Orders Serviced", f"{total_orders:,}")
col4.metric("Six Sigma: Capacity Defects", f"{defects} Overloaded", delta_color="inverse" if defects > 0 else "normal")

st.markdown("---")

# --- Interactive Map Construction ---
m = folium.Map(location=[12.9716, 77.5946], zoom_start=11, tiles="CartoDB dark_matter")

# 1. Plot Customer Demand Orders (if toggled on)
if show_orders:
    for _, row in df_orders.iterrows():
        folium.CircleMarker(
            location=[row['Customer_Lat'], row['Customer_Lon']],
            radius=1.5,
            color='#00FFFF', # Cyan dots for customer demand
            fill=True,
            fill_opacity=0.4,
            popup=f"Order Value: ₹{row['Order_Value_INR']:.0f} (Hour: {row['Order_Hour']}:00)"
        ).add_to(m)

# 2. Plot Competitor Overlays
for _, row in df_comp.iterrows():
    company = row['Company']
    if (show_zepto and company == 'Zepto') or \
       (show_blinkit and company == 'Blinkit') or \
       (show_instamart and company == 'Instamart'):
        
        color_map = {'Zepto': '#FF3366', 'Blinkit': '#FFCC00', 'Instamart': '#FF8800'}
        
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=4,
            color=color_map.get(company, '#FFFFFF'),
            fill=True,
            fill_opacity=0.8,
            popup=f"{company} Store"
        ).add_to(m)

# 3. Plot Flipkart Lean Optimized Hubs & SLA Radius
for _, row in df_proposed.iterrows():
    is_defect = row['Six_Sigma_Defect_Flag'] != 'Process in Control'
    pin_color = 'red' if is_defect else 'green'
    
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        icon=folium.Icon(color=pin_color, icon='info-sign'),
        popup=(
            f"<b>{row['Hub_ID']}</b><br>"
            f"<b>Demand:</b> {row['Peak_Order_Volume']}<br>"
            f"<b>Rent:</b> ₹{row['Monthly_CapEx_INR']:,.0f}<br>"
            f"<b>Status:</b> {row['Six_Sigma_Defect_Flag']}"
        )
    ).add_to(m)
    
    folium.Circle(
        location=[row['Latitude'], row['Longitude']],
        radius=sla_radius * 1000,
        color=pin_color, fill=True, fill_opacity=0.15, weight=1.5
    ).add_to(m)

st.subheader("Process Control Map: Demand Heatmap & SLA Coverage")
folium_static(m, width=1250, height=580)

