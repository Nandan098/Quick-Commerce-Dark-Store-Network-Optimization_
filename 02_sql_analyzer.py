import sqlite3
import pandas as pd

def run_dmaic_measure_phase():
    print("Step 2: Connecting to Database for Measure & Analyze Phase...")
    conn = sqlite3.connect('flipkart_lean_network.db')
    
    print("\n" + "="*60)
    print(" LEAN SIX SIGMA: BASELINE METRICS (MEASURE PHASE)")
    print("="*60)
    
    # --- INSIGHT 1: Value at Risk (Why do we need capacity limits?) ---
    q1 = """
    SELECT 
        CASE 
            WHEN Order_Hour BETWEEN 19 AND 22 THEN 'Peak Rush (7 PM - 10 PM)'
            ELSE 'Off-Peak Hours' 
        END AS Demand_Window,
        COUNT(Order_ID) AS Total_Orders,
        ROUND(AVG(Order_Value_INR), 0) AS Avg_Basket_Size_INR,
        ROUND(SUM(Order_Value_INR), 0) AS Total_Revenue_At_Risk_INR
    FROM customer_orders
    GROUP BY Demand_Window
    ORDER BY Total_Orders DESC;
    """
    print("\n[Insight 1: Time-Series Demand & Value at Risk]")
    print("Business Pitch: 'Over half of our daily volume hits in a 3-hour window. If warehouses bottleneck here, we risk massive revenue.'")
    print("-" * 60)
    print(pd.read_sql(q1, conn))
    
    # --- INSIGHT 2: Competitor Saturation (Where NOT to fight) ---
    q2 = """
    SELECT 
        Company, 
        COUNT("Store ID") as Total_Operating_Hubs 
    FROM competitor_stores 
    GROUP BY Company 
    ORDER BY Total_Operating_Hubs DESC;
    """
    print("\n[Insight 2: Competitor Baseline in Bengaluru]")
    print("Business Pitch: 'Blinkit and Zepto heavily saturate the market. We must target White-Spaces to avoid expensive real-estate bidding wars.'")
    print("-" * 60)
    print(pd.read_sql(q2, conn))
    
    # --- INSIGHT 3: VIP Customer Heatmap (Who to prioritize) ---
    q3 = """
    SELECT 
        Order_ID, 
        Order_Time_Str, 
        ROUND(Order_Value_INR, 0) AS Order_Value_INR, 
        ROUND(Customer_Lat, 4) AS Lat, 
        ROUND(Customer_Lon, 4) AS Lon
    FROM customer_orders
    WHERE Order_Hour BETWEEN 19 AND 22 AND Order_Value_INR > 750
    ORDER BY Order_Value_INR DESC
    LIMIT 5;
    """
    print("\n[Insight 3: High-Priority VIP Targets during Peak Hours]")
    print("Business Pitch: 'Our ML algorithm must physically prioritize high-value customers (> ₹750) to prevent churn among our most profitable users.'")
    print("-" * 60)
    print(pd.read_sql(q3, conn))

    conn.close()
    print("\nSQL Analysis Complete!")

if __name__ == "__main__":
    run_dmaic_measure_phase()