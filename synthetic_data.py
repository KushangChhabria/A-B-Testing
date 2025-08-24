import pandas as pd
import numpy as np
import sqlite3
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt

# Generate Synthetic Dataset

def generate_synthetic_data(n_users=1000, control_prob=0.10, uplift=0.12):
    np.random.seed(42)
    treatment_prob = control_prob * (1 + uplift)

    df = pd.DataFrame({
        "user_id": range(1, n_users + 1),
        "group": np.random.choice(["control", "treatment"], size=n_users)
    })

    df["converted"] = df["group"].apply(
        lambda x: np.random.binomial(1, control_prob if x=="control" else treatment_prob)
    )

    return df

# SQL Analysis

def run_sql(df):
    conn = sqlite3.connect(":memory:")
    df.to_sql("Users", conn, index=False, if_exists="replace")

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
    conv_sql = pd.read_sql(query1, conn)
    num_sql = pd.read_sql(query2, conn)
    return conv_sql, num_sql

# Statistical Test

def run_ztest(df):
    group_control = df[df["group"]=="control"]["converted"]
    group_treatment = df[df["group"]=="treatment"]["converted"]

    successes = [group_control.sum(), group_treatment.sum()]
    nobs = [group_control.count(), group_treatment.count()]

    z_stat, p_val = proportions_ztest(successes, nobs)
    return z_stat, p_val

# Visualization

def plot_results(df):
    conv_rates = df.groupby("group")["converted"].mean()
    plt.figure(figsize=(6,4))
    conv_rates.plot(kind="bar", color=["skyblue","salmon"], edgecolor="black")
    plt.title("Synthetic A/B Test Conversion Rates")
    plt.ylabel("Conversion Rate")
    plt.xticks(rotation=0)
    plt.show()

# Executive Summary

def executive_summary(df, z_stat, p_val, control_prob=0.10, uplift=0.12):
    conv_rates = df.groupby("group")["converted"].mean()
    actual_uplift = (conv_rates["treatment"] - conv_rates["control"]) / conv_rates["control"] * 100

    print("\n===== Executive Summary =====")
    print(f"Control Conversion Rate: {conv_rates['control']:.2%}")
    print(f"Treatment Conversion Rate: {conv_rates['treatment']:.2%}")
    print(f"Target Uplift: {uplift*100:.1f}%")
    print(f"Actual Relative Uplift: {actual_uplift:.2f}%")
    print(f"Z-test: Z={z_stat:.3f}, p-value={p_val:.3f}")
    if p_val < 0.05:
        print("Result: Statistically significant ✅")
    else:
        print("Result: Not statistically significant ❌")
    print("=============================")


# Main Execution

if __name__ == "__main__":
    # Step 1: Generate data
    df_users = generate_synthetic_data(n_users=1000, control_prob=0.10, uplift=0.12)

    # Step 2: SQL Analysis
    conv_sql, num_sql = run_sql(df_users)
    print("\nConversion Rate by Group (SQL):\n", conv_sql)
    print("\nNumber of Users by Group (SQL):\n", num_sql)

    # Step 3: Z-test
    z_stat, p_val = run_ztest(df_users)

    # Step 4: Visualization
    plot_results(df_users)

    # Step 5: Executive Summary
    executive_summary(df_users, z_stat, p_val, control_prob=0.10, uplift=0.12)
