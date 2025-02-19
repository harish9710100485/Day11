import pandas as pd
import numpy as np
import warnings
import csv
import os
import random
from xgboost import XGBRegressor

warnings.filterwarnings("ignore")

# Load Data
file_path = r"C:\Users\haris\Desktop\Day8\Sales_Data_for_Analysis.tsv"  # Update with actual path

if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    exit()

# Read dataset
df = pd.read_csv(file_path, sep="\t")

df.columns = df.columns.str.strip()
df.rename(columns={
    "PERIOD": "year", "QTY": "Quantity", "TOTAL PRICE (INR)": "Item Total",
    "CURRENCY": "Currency", "EX RATE": "Exchange Rate", "PART NO": "PART NO"
}, inplace=True)

required_columns = ["PART NO", "year", "Currency", "Item Total", "Exchange Rate"]
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"Error: Missing columns: {missing_columns}")
    exit()

# Clean Data
df.dropna(subset=["PART NO"], inplace=True)
df["year"] = pd.to_datetime(df["year"], errors="coerce", dayfirst=True).dt.year
df.dropna(subset=["year"], inplace=True)
df["year"] = df["year"].astype(int)
df["Currency"] = df["Currency"].str.strip().str.upper()

# Convert USD to INR
df["Exchange Rate"].fillna(75, inplace=True)
df.loc[df["Currency"] == "USD", "Item Total"] *= df["Exchange Rate"]
df["Currency"] = "INR"

if df.empty:
    print("No valid data available. Exiting.")
    exit()

latest_year = df["year"].max()

# Group Data
grouped = df.groupby(["PART NO", "year"])[["Quantity", "Item Total"]].sum().reset_index()

predictions = []
customer_names = ["CustomerA", "CustomerB", "CustomerC", "CustomerD", "CustomerE"]

def get_quarter(month):
    return "Q1" if month <= 3 else "Q2" if month <= 6 else "Q3" if month <= 9 else "Q4"

for part_no in grouped["PART NO"].unique():
    part_data = grouped[grouped["PART NO"] == part_no].copy()

    existing_customer = df.loc[df["PART NO"] == part_no, "Customer Name"].iloc[0] if "Customer Name" in df.columns and not df.loc[df["PART NO"] == part_no, "Customer Name"].isna().all() else random.choice(customer_names)

    if part_data["Quantity"].sum() == 0 and part_data["Item Total"].sum() == 0:
        predictions.append([part_no, latest_year + 1, 0, 0, 0, 0, 0, 0, "INR", existing_customer, "Q4"])
        continue

    if len(part_data) < 3:
        pred_quantity = int(round(part_data["Quantity"].mean())) if len(part_data) > 1 else 0
        pred_total = int(round(part_data["Item Total"].mean())) if len(part_data) > 1 else 0
        predictions.append([part_no, latest_year + 1, max(0, pred_quantity), max(0, pred_total), 0, 0, 0, 0, "INR", existing_customer, "Q4"])
        continue

    try:
        X_train = part_data["year"].values.reshape(-1, 1)
        y_train_quantity = part_data["Quantity"].values
        y_train_total = part_data["Item Total"].values
        
        model_quantity = XGBRegressor(objective='reg:squarederror', n_estimators=100)
        model_quantity.fit(X_train, y_train_quantity)
        pred_quantity = max(0, int(round(model_quantity.predict([[latest_year + 1]])[0])))
        
        model_total = XGBRegressor(objective='reg:squarederror', n_estimators=100)
        model_total.fit(X_train, y_train_total)
        pred_total = max(0, int(round(model_total.predict([[latest_year + 1]])[0])))
        
        min_quantity, max_quantity = pred_quantity * 0.9, pred_quantity * 1.1
        min_total, max_total = pred_total * 0.9, pred_total * 1.1

    except Exception as e:
        print(f"Error in XGBoost for {part_no}: {e}")
        pred_quantity, pred_total = max(0, int(part_data["Quantity"].mean())), max(0, int(part_data["Item Total"].mean()))
        min_quantity, max_quantity, min_total, max_total = pred_quantity, pred_quantity, pred_total, pred_total

    predictions.append([part_no, latest_year + 1, pred_quantity, pred_total, int(min_quantity), int(max_quantity), int(min_total), int(max_total), "INR", existing_customer, "Q4"])

predictions_df = pd.DataFrame(predictions, columns=["PART NO", "year", "Predicted Quantity", "Predicted Item Total", "Min Quantity", "Max Quantity", "Min Item Total", "Max Item Total", "Currency", "Customer Name", "Quarter"])

# Save Output
output_file = r"C:\Users\haris\Desktop\Day10\prediction.tsv"
predictions_df.to_csv(output_file, index=False, sep="\t", quoting=csv.QUOTE_NONNUMERIC)

print(f"Predictions saved at: {output_file}")
print(predictions_df)
