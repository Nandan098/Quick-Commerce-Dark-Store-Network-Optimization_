import sqlite3
import pandas as pd
import numpy as np

def setup_dmaic_database():
    print("Initializing Quick Commerce Database with Organic Clusters...")
    conn = sqlite3.connect('flipkart_lean_network.db')

    # 1. Load Real Competitor Dataset
    try:
        df_comp = pd.read_excel(r"Dataset\darkstores_Cleaned_Standardized.xlsx", sheet_name='All Stores')
        df_comp[df_comp['City'] == 'Bengaluru'].to_sql('competitor_stores', conn, if_exists='replace', index=False)
        print("✅ Competitor data loaded.")
    except Exception as e:
        print(f"Error loading competitor data: {e}")

    # 2. Generate Organic Clustered Customer Demand (Realistic City Spread)
    np.random.seed(42)
    num_orders = 6000
    
    # Define major commercial/residential hotspots in Bangalore (Lat, Lon centers)
    hotspots = [
        (12.9352, 77.6245), # Koramangala
        (12.9698, 77.7500), # Whitefield
        (12.9716, 77.5946), # Majestic / Central
        (12.9166, 77.6101), # HSR Layout
        (13.0358, 77.5970), # Hebbal
        (12.9279, 77.5829), # Jayanagar
        (12.9784, 77.6408)  # Indiranagar
    ]
    
    # Distribute orders among these hotspots organically
    cluster_indices = np.random.choice(len(hotspots), size=num_orders, p=[0.25, 0.20, 0.15, 0.15, 0.10, 0.10, 0.05])
    lats, lons = [], []
    
    for idx in cluster_indices:
        center_lat, center_lon = hotspots[idx]
        # Add random normal spread around the hotspot (standard deviation creates organic blobs)
        lats.append(np.random.normal(loc=center_lat, scale=0.035))
        lons.append(np.random.normal(loc=center_lon, scale=0.035))

    # Time-series bell curve peaking at 8:00 PM
    base_date = pd.to_datetime('2026-08-14 00:00:00')
    seconds_offsets = np.clip(np.random.normal(loc=20 * 3600, scale=2.5 * 3600, size=num_orders), 0, 86399)
    timestamps = [base_date + pd.to_timedelta(sec, unit='s') for sec in seconds_offsets]

    df_orders = pd.DataFrame({
        'Order_ID': [f"ORD-{i}" for i in range(10000, 10000 + num_orders)],
        'Customer_Lat': lats,
        'Customer_Lon': lons,
        'Order_Timestamp': timestamps,
        'Order_Value_INR': np.random.normal(loc=480, scale=150, size=num_orders).clip(120, 2500)
    })
    
    df_orders['Order_Hour'] = df_orders['Order_Timestamp'].dt.hour
    df_orders['Order_Time_Str'] = df_orders['Order_Timestamp'].dt.strftime('%H:%M:%S')
    
    df_orders.to_sql('customer_orders', conn, if_exists='replace', index=False)
    conn.close()
    print("Organic customer demand generated successfully!")

if __name__ == "__main__":
    setup_dmaic_database()