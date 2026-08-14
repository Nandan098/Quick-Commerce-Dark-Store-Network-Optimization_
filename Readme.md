#  Quick Commerce Supply Chain Network Optimization Engine
## A Lean Six Sigma DMAIC Approach to Dark Store Placement & SLA Control

---

## Executive Problem Statement & Supply Chain Challenge
In hyper-local quick commerce operations—such as in Bengaluru, which sees upward of 400,000 to 500,000 daily orders—maintaining a strict **10-minute Service Level Agreement (SLA)** is the primary driver of customer retention and market share. 

* **The Operational Bottleneck:** Poor warehouse site selection leads to excessive transit distances, violating the 10-minute delivery window. Furthermore, uneven order distribution causes severe warehouse congestion during peak evening rushes (7 PM – 10 PM), leading to process variation and packing failures.
* **The Strategic Dilemma:** Rapidly scaling the dark store footprint increases real-estate CapEx (monthly rent), while under-investing in infrastructure creates massive delivery bottlenecks and revenue-at-risk.

---

##  The Lean Six Sigma DMAIC Framework Implementation

This project applies a rigorous **DMAIC (Define, Measure, Analyze, Improve, Control)** methodology to engineer a cost-effective, high-speed dark store network:

### 1. DEFINE Phase
* **Critical-to-Quality (CTQ) Metric:** The 10-minute delivery window, constrained by a maximum delivery radius of **2.0 km**.
* **Capacity Thresholds:** Established a Six Sigma control limit capping individual dark store volume at **1,200 orders** during peak hours to prevent warehouse packing bottlenecks.

### 2. MEASURE Phase
* **Data Architecture:** Integrated real-world competitor store footprints (Blinkit, Zepto, Instamart) with a synthesized, statistically weighted demand dataset of **6,000 peak-hour customer orders**.
* **Baseline Analytics (SQL):** Quantified operational risk, proving through time-series analysis that over 50% of daily revenue is concentrated in a tight 3-hour evening window, establishing our baseline "Value at Risk."

### 3. ANALYSE Phase
* **Competitor Intelligence & White-Space Mapping:** Cross-referenced customer demand density against competitor saturation metrics. 
* **Root-Cause Prevention:** Identified that opening hubs in saturated zones triggers costly delivery wars. Shifted the strategic target toward high-density **"White-Spaces"**—underserved residential and commercial corridors with heavy demand but zero rival presence.

### 4. IMPROVE Phase
* **Spatial Optimization (K-Means Clustering):** Deployed unsupervised machine learning weighted around Bengaluru’s major consumption nodes (Koramangala, Whitefield, HSR Layout) to mathematically minimize delivery transit distances—**eliminating Lean transportation waste**.
* **CapEx vs. Service Trade-Off:** Minimized the total monthly real-estate CapEx while ensuring all proposed hubs operate safely below the Six Sigma capacity defect threshold.

### 5. CONTROL Phase
* **Executive Control Tower (Streamlit):** Developed an interactive operational dashboard equipped with live GIS mapping, dynamic SLA sensitivity sliders, and automated defect-tracking flags to continuously monitor network health.

---