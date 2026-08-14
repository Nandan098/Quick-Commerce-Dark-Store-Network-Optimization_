import sqlite3
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

def run_dmaic_improve_phase(n_stores=8, six_sigma_capacity_limit=1200):
    print("Step 3: Running Machine Learning Spatial Optimization (Improve Phase)...")
    
    # 1. Connect to our SQLite database
    conn = sqlite3.connect('flipkart_lean_network.db')
    
    # 2. Extract customer demand coordinates from SQL
    df_demand = pd.read_sql("SELECT Customer_Lat, Customer_Lon FROM customer_orders", conn)
    
    # 3. IMPROVE (Lean): Run K-Means to mathematically minimize transit distances (waste)
    print(f"Applying K-Means Clustering to place {n_stores} optimal dark stores...")
    coordinates = df_demand[['Customer_Lat', 'Customer_Lon']].values
    kmeans = KMeans(n_clusters=n_stores, init='k-means++', random_state=42, n_init=10)
    df_demand['Assigned_Hub'] = kmeans.fit_predict(coordinates)
    
    # Extract the store centroid coordinates
    centroids = kmeans.cluster_centers_
    proposed_hubs = pd.DataFrame(centroids, columns=['Latitude', 'Longitude'])
    proposed_hubs['Hub_ID'] = [f"FLK-LEAN-{i+1:02d}" for i in range(n_stores)]
    
    # 4. IMPROVE (Six Sigma): Apply Capacity Controls to prevent warehouse bottlenecks
    order_counts = df_demand['Assigned_Hub'].value_counts().to_dict()
    proposed_hubs['Peak_Order_Volume'] = proposed_hubs.index.map(order_counts)
    
    # Flag defects if a warehouse exceeds the maximum safe packing limit
    proposed_hubs['Six_Sigma_Defect_Flag'] = proposed_hubs['Peak_Order_Volume'].apply(
        lambda x: 'Defect: Over Capacity' if x > six_sigma_capacity_limit else 'Process in Control'
    )

    # 5. Financial Analysis: Calculate Real-Estate CapEx (Rent) based on latitude zones
    rent_values = np.interp(proposed_hubs['Latitude'], [12.85, 13.05], [260000, 140000])
    proposed_hubs['Monthly_CapEx_INR'] = np.round(rent_values, -2)

    # Save the optimized network plan back to the database for our Streamlit dashboard
    proposed_hubs.to_sql('improved_network_plan', conn, if_exists='replace', index=False)
    conn.close()
    
    print("\n" + "="*70)
    print("OPTIMIZED DARK STORE NETWORK PLAN (IMPROVE PHASE)")
    print("="*70)
    print(proposed_hubs[['Hub_ID', 'Peak_Order_Volume', 'Six_Sigma_Defect_Flag', 'Monthly_CapEx_INR']])
    print("\nMachine Learning Optimization Complete! Plan saved to database.")

if __name__ == "__main__":
    run_dmaic_improve_phase()