# main.py
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportions_ztest
from scipy import stats

# 1. Load Dataset
df = pd.read_csv("ab_data.csv")   # replace with your dataset filename
print("Data Preview:\n", df.head())

# Ensure correct dtypes
df['converted'] = df['converted'].astype(int)

# 2. Load into SQLite (for SQL analysis)
conn = sqlite3.connect(":memory:")  # in-memory database
df.to_sql("Users", conn, index=False, if_exists="replace")

# SQL Queries
query1 = """
SELECT "group", AVG(converted) AS ConversionRate
FROM Users
GROUP BY "group";
"""

query2 = """
SELECT "group", COUNT(*) AS NumUsers
FROM Users
GROUP BY "group";
"""

conversion_rate_sql = pd.read_sql(query1, conn)
num_users_sql = pd.read_sql(query2, conn)

print("\nConversion Rate by Group (SQL):\n", conversion_rate_sql)
print("\nNumber of Users by Group (SQL):\n", num_users_sql)

# 3. Python-side Analysis
conv_rates = df.groupby("group")["converted"].mean()
num_users = df.groupby("group")["user_id"].nunique()
print("\nConversion Rates (Python):\n", conv_rates)
print("\nNumber of Users (Python):\n", num_users)

# Two-proportion Z-test
group_control = df[df["group"] == "control"]["converted"]
group_treatment = df[df["group"] == "treatment"]["converted"]

successes = [group_control.sum(), group_treatment.sum()]
nobs = [group_control.count(), group_treatment.count()]

z_stat, p_val = proportions_ztest(successes, nobs)
print("\nZ-test Results:")
print(f"Z-statistic = {z_stat:.4f}, p-value = {p_val:.4f}")

# T-test (conversion binary, just to show usage)
t_stat, t_pval = stats.ttest_ind(group_control, group_treatment)
print("\nT-test Results:")
print(f"T-statistic = {t_stat:.4f}, p-value = {t_pval:.4f}")


# 4. Visualization
# Conversion Rate Plot
plt.figure(figsize=(6, 4))
conv_rates.plot(kind="bar", color=["skyblue", "salmon"], edgecolor="black")
plt.title("Conversion Rate by Group")
plt.ylabel("Conversion Rate")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Number of Users Plot
plt.figure(figsize=(6, 4))
num_users.plot(kind="bar", color=["skyblue", "salmon"], edgecolor="black")
plt.title("Number of Users by Group")
plt.ylabel("Users Count")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()



