# Sales Data Prediction Script (Using XGBoost)

## Overview
This script processes sales data from a TSV file, cleans and structures the data, and then predicts future sales quantities and total prices using an XGBoost regression model. The predictions are saved in a TSV file for further analysis.

## Prerequisites
Before running the script, ensure you have the following dependencies installed:

### **Required Python Libraries**
Install the required libraries using:
```bash
pip install pandas numpy xgboost
```

### **File Requirements**
Ensure you have a properly formatted sales data file (`Sales_Data_for_Analysis.tsv`). This file should include the following columns:
- `PERIOD` (Date/Year)
- `QTY` (Quantity Sold)
- `TOTAL PRICE (INR)` (Total Price in INR)
- `CURRENCY` (Currency of transaction)
- `EX RATE` (Exchange Rate)
- `PART NO` (Product Part Number)
- `Customer Name` (Optional, fallback customers are used if missing)

## How to Use

1. **Update File Path**
   Modify the `file_path` variable in the script to match the location of your sales data file:
   ```python
   file_path = r"C:\Users\haris\Desktop\Day8\Sales_Data_for_Analysis.tsv"
   ```

2. **Run the Script**
   Execute the script using:
   ```bash
   python sales_prediction.py
   ```

3. **Output File**
   The predictions will be saved as a TSV file at:
   ```
   C:\Users\haris\Desktop\Day10\prediction.tsv
   ```

## Script Functionality

### **1. Load and Validate Data**
- Reads the TSV file into a Pandas DataFrame.
- Ensures required columns are present.
- Handles missing values and incorrect formats.

### **2. Data Cleaning & Transformation**
- Strips column names and renames them for consistency.
- Converts `PERIOD` into a numerical `year` format.
- Converts all currency values to INR (assuming missing exchange rates default to 75).
- Removes rows with missing `PART NO` values.

### **3. Sales Prediction Using XGBoost**
- Groups data by `PART NO` and `year`.
- Uses historical data to predict next year’s sales.
- If insufficient data is available, falls back to simple averaging.
- Predicts **both quantity and total sales** for each product.

### **4. Generates Predictions**
For each product (`PART NO`), the script generates:
- `Predicted Quantity` & `Predicted Item Total`
- `Min Quantity` & `Max Quantity`
- `Min Item Total` & `Max Item Total`
- `Currency` (Always INR)
- `Customer Name` (Existing or randomly assigned)
- `Quarter` (Assumed Q4 if missing monthly data)

### **5. Saves Predictions to File**
The results are saved in `prediction.tsv` as a tab-separated file.

## Example Output
| PART NO  | Year | Predicted Quantity | Predicted Item Total | Min Quantity | Max Quantity | Min Item Total | Max Item Total | Currency | Customer Name | Quarter |
|----------|------|--------------------|----------------------|--------------|--------------|----------------|----------------|----------|---------------|---------|
| ABC123   | 2025 | 500                | 750000              | 450          | 550          | 675000         | 825000         | INR      | CustomerA     | Q4      |
| XYZ987   | 2025 | 200                | 300000              | 180          | 220          | 270000         | 330000         | INR      | CustomerB     | Q4      |

## Error Handling
- If the file is missing, the script prints an error and exits.
- If required columns are missing, an error message is displayed.
- If the dataset is empty after processing, the script exits.

## Future Improvements
- Support for additional currencies.
- More robust handling of missing or incomplete data.
- Improve prediction models with seasonal analysis.

---
Author:Harish
Intern:Minerva

