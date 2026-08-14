# --- INSIGHT 1: Value at Risk (Why do we need capacity limits?) ---
SELECT 
        CASE 
            WHEN Order_Hour BETWEEN 17 AND 22 THEN 'Peak Rush (7 PM - 10 PM)'
            ELSE 'Off-Peak Hours' 
        END AS Demand_Window,
        COUNT(Order_ID) AS Total_Orders,
        ROUND(AVG(Order_Value_INR), 0) AS Avg_Basket_Size_INR,
        ROUND(SUM(Order_Value_INR), 0) AS Total_Revenue_At_Risk_INR
    FROM customer_orders
    GROUP BY Demand_Window
    ORDER BY Total_Orders DESC;
  

# --- INSIGHT 2: VIP Customer Heatmap (Who to prioritize) ---  
  
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
   
   
# --- INSIGHT 3: Competitor Saturation (Where NOT to fight) ---   
    
  SELECT 
        Company, 
        COUNT("Store ID") as Total_Operating_Hubs 
    FROM competitors
    GROUP BY Company 
    ORDER BY Total_Operating_Hubs DESC;