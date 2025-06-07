import pandas as pd
import re
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import functions from the script
from excel_to_contacts import convert_excel_to_custom_csv, clean_phone_number

def test_clean_phone_number():
    """Test the clean_phone_number function with various inputs."""
    test_cases = [
        ("+7999745-12-15", "+79997451215"),
        ("+8210-7508-8471", "+821075088471"),
        ("+353838888990", "+353838888990"),
        ("123-456-7890", "1234567890"),
        ("(123) 456-7890", "1234567890"),
        ("123.456.7890", "1234567890"),
        ("123 456 7890", "1234567890"),
        (1234567890, "1234567890"),
    ]

    for input_number, expected_output in test_cases:
        cleaned = clean_phone_number(input_number)
        assert cleaned == expected_output, f"Expected {expected_output}, got {cleaned} for input {input_number}"

    print("All clean_phone_number tests passed!")

def test_excel_processing():
    """Test processing the Excel file and check the output CSV."""
    input_file = "phone_numbers.xlsx"
    output_file = "test_output.csv"
    phone_column = "Phone Number"

    # Process the Excel file
    convert_excel_to_custom_csv(input_file, phone_column, output_file)

    # Read the output CSV, ensuring phone numbers are read as strings
    df_output = pd.read_csv(output_file, dtype={"Phone 1 - Value": str})

    # Check if the "Phone 1 - Value" column exists
    assert "Phone 1 - Value" in df_output.columns, "Output CSV doesn't have 'Phone 1 - Value' column"

    # Check if all phone numbers are properly formatted (only digits and possibly a leading '+')
    for phone in df_output["Phone 1 - Value"]:
        # Convert to string if it's not already
        phone_str = str(phone)

        # Phone should match the pattern: optional '+' followed by digits only
        assert re.match(r'^\+?\d+$', phone_str), f"Phone number {phone_str} is not properly formatted"

    print(f"All phone numbers in the output CSV are properly formatted!")

    # Return the output dataframe for further inspection if needed
    return df_output

if __name__ == "__main__":
    print("Testing clean_phone_number function...")
    test_clean_phone_number()

    print("\nTesting Excel processing...")
    df_output = test_excel_processing()

    print("\nSample of processed phone numbers:")
    print(df_output["Phone 1 - Value"].head(10))
