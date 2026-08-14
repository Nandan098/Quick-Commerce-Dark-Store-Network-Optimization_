# Flipkart Quick Commerce Network Optimization: A Lean Six Sigma DMAIC Engine

An enterprise-grade supply chain optimization platform designed to solve the critical-to-quality (CTQ) 10-minute delivery SLA challenge for quick commerce operations in Bengaluru. This project integrates spatial data science, SQL analytics, Unsupervised Machine Learning (K-Means Clustering), and an interactive executive Streamlit dashboard.

---

## Executive Summary & Business Context
In high-demand quick commerce environments (such as Bengaluru, which handles upwards of 400k–500k daily orders), network design dictates profitability. 
* **The Problem:** Poorly positioned dark stores lead to excessive transit times (failing the 10-minute SLA) or over-saturation in competitive zones, destroying margins.
* **The Solution:** A hybrid pipeline combining **real-world competitor intelligence** (Blinkit, Zepto, Instamart) with **synthetic gaussian-distributed customer demand** to optimally place dark stores using K-Means clustering, all while enforcing Lean Six Sigma capacity controls.

---

## Tech Stack & Architecture
* **Python (Core Engine):** Data manipulation and statistical generation (`pandas`, `numpy`)
* **Machine Learning:** Spatial clustering via `scikit-learn` (K-Means++)
* **Database & Querying:** Relational data management using `SQLite` and advanced SQL
* **Control Tower Dashboard:** Interactive GIS mapping and executive UI via `Streamlit` and `Folium`
* **Methodology:** Lean Six Sigma DMAIC Framework (Define, Measure, Analyze, Improve, Control)

---
