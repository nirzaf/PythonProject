import pandas as pd

# Read the Excel file
df = pd.read_excel('phone_numbers.xlsx')

# Display the first few rows to understand the structure
print("Excel file structure:")
print(df.head())

# Display column names
print("\nColumn names:", df.columns.tolist())

# Check data types of each column
print("\nData types:")
print(df.dtypes)

# If there's a column named "Phone Number", examine its content
if "Phone Number" in df.columns:
    print("\nPhone Number column content:")
    print(df["Phone Number"].head(10))
    print("\nPhone Number column data type:", df["Phone Number"].dtype)
    
    # Check if all values in the Phone Number column are numeric
    numeric_values = pd.to_numeric(df["Phone Number"], errors='coerce')
    non_numeric_count = numeric_values.isna().sum()
    print(f"\nNumber of non-numeric values in Phone Number column: {non_numeric_count}")
    
    if non_numeric_count > 0:
        print("\nSample of non-numeric values:")
        non_numeric_mask = numeric_values.isna()
        print(df.loc[non_numeric_mask, "Phone Number"].head(10))
else:
    # If there's no column named "Phone Number", check the first column (index 0)
    first_column_name = df.columns[0]
    print(f"\nFirst column '{first_column_name}' content:")
    print(df.iloc[:, 0].head(10))
    print(f"\nFirst column data type: {df.iloc[:, 0].dtype}")
    
    # Check if all values in the first column are numeric
    numeric_values = pd.to_numeric(df.iloc[:, 0], errors='coerce')
    non_numeric_count = numeric_values.isna().sum()
    print(f"\nNumber of non-numeric values in first column: {non_numeric_count}")
    
    if non_numeric_count > 0:
        print("\nSample of non-numeric values:")
        non_numeric_mask = numeric_values.isna()
        print(df.loc[non_numeric_mask, df.columns[0]].head(10))