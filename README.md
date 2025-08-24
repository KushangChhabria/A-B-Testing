# A/B Testing of Website Features

This repository demonstrates end-to-end A/B testing workflows using Python and SQL, including data analysis, hypothesis testing, and visualization.

---

## Project Structure
- ab_data.csv: Real dataset of users with group assignment and conversions
- real_data.py: Analysis on real dataset: SQL, Python, statistical tests
- synthetic_data.py: Analysis on generated dataset: SQL, Python, statistical tests

---

## 1. Real Dataset Analysis

**Description:**  
Analyzed a real dataset of website users to compare an old landing page (control) vs a new landing page (treatment). Goal: check if the new page improves conversions.

**Key Features:**  
- SQL queries to calculate conversion rates and number of users per group.  
- Python analysis of conversion rates.  
- Z-test and T-test for hypothesis testing and p-value interpretation.  
- Visualization of conversion rates using bar charts.  

**Results:**  
- Control conversion: ~12.04%  
- Treatment conversion: ~11.89%  
- Z-test p-value: 0.216 → No statistically significant uplift  
- **Insight:** The new page does not improve conversions.  

---

## 2. Synthetic Dataset Analysis

**Description:**  
Created a synthetic dataset to simulate an A/B test with a **12% relative uplift**. Useful to demonstrate the workflow from data generation to actionable insights.

**Key Features:**  
- Synthetic data generation with user IDs, group assignment, and conversion outcomes.  
- SQL queries for conversion metrics.  
- Z-test to confirm statistical significance of uplift.  
- Bar chart visualizations.  
- Executive summary showing target vs actual uplift.  

**Results:**  
- Control conversion: 10%  
- Treatment conversion: 11.2% (12% relative uplift)  
- Z-test p-value: < 0.05 → Statistically significant  
- **Insight:** Treatment variant would be recommended for rollout.  

---

## Skills Demonstrated
- Python: pandas, numpy, matplotlib, statsmodels  
- SQL: SQLite queries for aggregation and metrics  
- Statistics: Z-test, T-test, hypothesis testing, p-value interpretation  
- Data Visualization: Conversion rate charts  
- Business Analysis: Data-driven recommendations based on A/B test results  

---

## Usage

1. Clone the repository:
```bash
git clone https://github.com/<your-username>/A-B-Testing-Project.git
cd A-B-Testing-Project
```
2. Run the real data analysis:
```bash
python real_data.py
```
3. Run the synthetic data analysis:
```bash
python synthetic_data.py
```

