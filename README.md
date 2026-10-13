# 🚚 AI-Powered Supply Chain Analytics & Logistics Optimization Platform

### Python | Machine Learning | Power BI | Logistics Analytics

An end-to-end data analytics and machine learning project designed to analyze logistics operations, identify delivery delays, evaluate transportation performance, and support data-driven supply chain decisions.

> **Project Status:** Version 1 Completed  
> **Dashboard:** 4 Interactive Power BI Pages  
> **Machine Learning:** Delivery Delay Prediction using Python

---

## 📌 Project Overview

Supply chain and logistics operations generate large amounts of data related to deliveries, transportation costs, vehicle utilization, weather conditions, and delivery performance.

Analyzing this data can help businesses identify operational inefficiencies, understand delivery delays, and improve logistics decision-making.

This project combines:

- Python-based data cleaning and preprocessing
- Exploratory Data Analysis (EDA)
- Machine Learning for delivery delay prediction
- Logistics performance analysis
- Interactive Power BI dashboards
- Business intelligence and operational reporting

The project demonstrates how descriptive analytics and predictive modeling can be used together to understand logistics challenges.

---

## 🎯 Business Problem

Logistics organizations frequently face challenges such as:

- Unexpected delivery delays
- High transportation costs
- Differences in delivery partner performance
- Weather-related delivery disruptions
- Inefficient transportation operations
- Limited visibility into logistics performance

This project analyzes historical logistics data to investigate these challenges and support informed operational decisions.

---

## 🎯 Project Objectives

1. Analyze historical delivery data to identify operational patterns.
2. Investigate factors associated with delivery delays.
3. Develop machine learning models for delivery delay prediction.
4. Evaluate logistics performance across vehicles, regions, and delivery partners.
5. Analyze transportation costs and delivery efficiency.
6. Build interactive Power BI dashboards for operational reporting.

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| Programming | Python |
| Data Manipulation | Pandas, NumPy |
| Data Visualization | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn |
| Business Intelligence | Power BI |
| Data Modeling | Power Query, DAX |
| Development Environment | Jupyter Notebook, VS Code |
| Version Control | Git, GitHub |
| Data Source | Excel, CSV |

---

## 📂 Dataset Overview

The project uses a multi-sheet Excel dataset containing historical logistics and delivery information.

The dataset includes operational attributes related to:

- Delivery information
- Delivery partners
- Vehicle types
- Delivery modes
- Weather conditions
- Delivery regions
- Transportation distance
- Package weight
- Delivery costs
- Customer ratings
- Delivery delays

### Data Preparation

The dataset was prepared using Python.

Key preprocessing activities included:

- Inspecting data quality
- Standardizing inconsistent text values
- Processing date fields
- Removing unusable placeholder-valued fields
- Preparing data for exploratory analysis
- Preparing features for machine learning
- Exporting processed datasets

---

## 🔍 Exploratory Data Analysis

Exploratory Data Analysis was performed to understand delivery patterns and operational performance.

The analysis investigated:

- Delivery performance across different regions
- Delivery delays under different weather conditions
- Vehicle-type performance
- Delivery partner performance
- Transportation distance
- Delivery costs
- Customer ratings

The analysis helps identify operational patterns that can be explored further through predictive modeling and business intelligence.

---

## 🤖 Machine Learning — Delivery Delay Prediction

A machine learning workflow was developed in Python to predict delivery delays using historical logistics data.

### Machine Learning Workflow

1. Data preprocessing
2. Feature preparation
3. Training and testing data preparation
4. Model development
5. Model evaluation
6. Model comparison and optimization
7. Prediction generation

### Objective

Identify deliveries that may be at risk of delay based on available operational characteristics.

### Model Evaluation

The machine learning workflow can be evaluated using:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

**Note:** Actual model performance metrics will be documented after verification against the final notebook results.

> **Important:** Delivery delay prediction is implemented in the Python notebook. The current Power BI dashboard does not yet include machine learning prediction visualizations.

---

## 📊 Power BI — Supply Chain Analytics Dashboard

An interactive four-page Power BI dashboard was developed to analyze logistics operations and communicate operational insights.

### Dashboard Pages

| Page | Description |
|------|-------------|
| Executive Overview | High-level delivery performance, operational KPIs, costs, and regional comparisons |
| Delay Analysis | Delivery delays across partners, weather conditions, vehicles, and distance bands |
| Logistics Performance | Delivery volumes, transportation distances, delivery modes, and customer ratings |
| Cost & Risk Analysis | Transportation costs, cost efficiency, and costs associated with delayed deliveries |

### Dashboard Features

- Interactive KPI cards
- DAX measures
- Operational performance visualizations
- Dynamic slicers
- Page navigation
- Delivery delay analysis
- Transportation cost analysis

### 📊 Explore the Dashboard

For detailed explanations of all four dashboard pages, KPIs, visualizations, and interactive features:

**[View Power BI Dashboard Documentation](Visualization/README.md)**

---

## 🔄 End-to-End Project Workflow

```text
Historical Logistics Dataset
           |
           v
Data Inspection & Cleaning
           |
           v
Data Preprocessing
           |
           v
Exploratory Data Analysis
           |
           +----------------------+
           |                      |
           v                      v
Machine Learning          Prepared Reporting Data
           |                      |
           v                      v
Delay Prediction          Power BI Dashboard
           |                      |
           v                      v
Model Evaluation          Logistics Performance
           |                      |
           +-----------+----------+
                       |
                       v
            Data-Driven Insights
```

---

## 📁 Repository Structure

```text
AI-Powered-Supply-Chain-Analytics/
│
├── README.md
│
├── data/
│
├── notebooks/
│   └── AI-Powered_Supply_Chain_Analytics.ipynb
│
├── outputs/
│
├── Visualization/
│   │
│   ├── README.md
│   │
│   ├── data/
│   │
│   ├── PowerBI_File/
│   │   └── Supply_Chain_Analytics_Dashboard.pbix
│   │
│   └── Screenshots/
│       ├── Executive_Overview.png
│       ├── Delay_Analysis.png
│       ├── Logistics_Performance.png
│       └── Cost_and_Risk_Analysis.png
│
└── .gitignore
```

*Folder contents and filenames should match the actual repository.*

---

## 🚀 How to Explore the Project

### 1. Explore Python Analysis

Open the Jupyter Notebook located in the `notebooks/` folder.

Review the data preparation, exploratory analysis, and machine learning workflow.

### 2. Explore Processed Data

Review the available datasets and generated outputs.

### 3. Explore Power BI Dashboard

Navigate to:

`Visualization/PowerBI_File/`

Download the `.pbix` file and open it using Power BI Desktop.

### 4. Review Dashboard Documentation

Read the detailed documentation available in:

`Visualization/README.md`

---

## 📌 Project Implementation Status

| Component | Status |
|-----------|--------|
| Data Cleaning | ✅ Completed |
| Exploratory Data Analysis | ✅ Completed |
| Delivery Delay Prediction Workflow | ✅ Completed |
| Machine Learning Evaluation | ✅ Implemented |
| Power BI Executive Overview | ✅ Completed |
| Power BI Delay Analysis | ✅ Completed |
| Power BI Logistics Performance | ✅ Completed |
| Power BI Cost & Risk Analysis | ✅ Completed |
| Prediction Visualization in Power BI | 🔜 Planned |
| Advanced Dashboard Enhancements | 🔜 Planned |
| Live ML Prediction Application | 🔜 Future Enhancement |

---

## 🔮 Future Enhancements

Potential improvements include:

- Integrating machine learning prediction outputs into Power BI
- Developing a dedicated Prediction Analysis dashboard page
- Enhancing dashboard interactivity and visualizations
- Adding more advanced operational insights
- Developing an interactive machine learning prediction application
- Exploring demand forecasting with suitable historical demand data
- Exploring vehicle routing optimization with appropriate routing data

---

## 📚 Project Learnings

This project demonstrates practical experience in:

- Data cleaning and preprocessing
- Exploratory Data Analysis
- Machine learning model development
- Delivery delay prediction
- Logistics performance analysis
- Power BI dashboard development
- DAX calculations
- Data storytelling
- End-to-end analytics project organization

---

## ⚠️ Project Limitations

This project is an analytics prototype based on historical logistics data.

Machine learning predictions are not guaranteed outcomes.

The current dashboard provides descriptive logistics analysis and does not include live prediction functionality.

Demand forecasting and vehicle routing optimization remain potential future extensions.

---

### ⭐ Project Focus

**Python • Machine Learning • Supply Chain Analytics • Power BI • Business Intelligence • Data-Driven Decision Making**
