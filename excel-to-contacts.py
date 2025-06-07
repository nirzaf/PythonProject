import pandas as pd
import random
import re

# --- Sample Data for Random Name Generation (Islamic Names) ---
# You can expand these lists for more variety
FIRST_NAMES = [
    "Mohammed", "Ahmed", "Ali", "Omar", "Yusuf", "Ibrahim", "Hassan", "Hussein", "Khalid", "Mustafa",
    "Abdullah", "Abdulrahman", "Saad", "Faisal", "Tariq", "Zayd", "Bilal", "Hamza", "Idris", "Ismail",
    "Fatima", "Aisha", "Khadija", "Zainab", "Maryam", "Amina", "Hafsa", "Safiya", "Ruqayyah", "Sumayyah",
    "Layla", "Noor", "Hana", "Sara", "Yasmin", "Farah", "Samira", "Nadia", "Iman", "Salma",
    "Jamal", "Karim", "Rashid", "Malik", "Nasir", "Aziz", "Hakim", "Rafiq", "Tahir", "Waqar",
    "Zubair", "Anwar", "Imran", "Jawad", "Naveed", "Qadir", "Salim", "Umar", "Wasim", "Yasir",
    "Asad", "Bashir", "Dawood", "Fahad", "Ghazi", "Haroon", "Irfan", "Jameel", "Kamran", "Latif",
    "Munir", "Nabeel", "Qasim", "Raheem", "Shahid", "Taimur", "Usama", "Waheed", "Zahir", "Adnan",
    "Fatimah", "Ayesha", "Khadijah", "Zaynab", "Mariam", "Aminah", "Hafsah", "Safiyyah", "Ruqayyah", "Sumayya",
    "Leila", "Nur", "Hannah", "Sarah", "Yasmeen", "Farha", "Sameera", "Nadiyah", "Imaan", "Salmah",
    "Asiya", "Basimah", "Dalal", "Farida", "Ghada", "Halima", "Ibtisam", "Jameela", "Karima", "Lubna",
    "Madiha", "Nabeela", "Qamra", "Rabia", "Safia", "Tahira", "Uzma", "Wafa", "Zara", "Aliyah",
    "Bushra", "Dalia", "Fariha", "Huda", "Inaya", "Jannah", "Kenza", "Latifa", "Malika", "Nabila",
    "Qamar", "Rania", "Sabrina", "Tala", "Umm", "Warda", "Zahra", "Amal", "Badriyah", "Dina",
    "Amira", "Rami", "Samah", "Najib", "Samiya", "Rabab", "Munira", "Gamal", "Mona", "Rashida",
    "Sahar", "Faris", "Yara", "Rana", "Hatem", "Lina", "Ramiya", "Nour", "Majid", "Rania",
    "Abeer", "Sami", "Mazin", "Nada", "Salem", "Nidal", "Maysa", "Rafif", "Jad", "Sawsan",
    "Ayman", "Hala", "Nashwa", "Tamer", "Nihal", "Ruba", "Hossam", "Amani", "Khalil", "Dina",
    "Fadi", "Rima", "Shadi", "Maha", "Nouran", "Ola", "Heba", "Tala", "Rashed", "Siham"
]
MIDDLE_NAMES = [
    "Ali", "Hassan", "Hussein", "Ahmed", "Khan", "Mohammed", "Abdul", "Din", "Uddin", "Al",
    # Common components or names
    "Noor", "Zahra", "Banu", "Begum", "Sultana", "Khatun",  # Female specific or common honorifics used as middle
    "Ibn", "Bin",  # Patronymic (son of) - less common in simple name generation
    "Bint",  # Matronymic (daughter of) - less common in simple name generation
    "El", "Al-",  # Common prefixes
    # Additional middle names
    "Abid", "Adil", "Akbar", "Amir", "Anwar", "Arif", "Asif", "Azam", "Badr", "Basim",
    "Deen", "Ehsan", "Faiz", "Fareed", "Fawaz", "Habib", "Hadi", "Hafiz", "Hakeem", "Halim",
    "Hamid", "Haris", "Hasan", "Hashim", "Haytham", "Hikmat", "Hisham", "Ihsan", "Imad", "Isa",
    "Jabbar", "Jalal", "Jamal", "Jamil", "Jawad", "Jibril", "Kamal", "Kareem", "Khalil", "Latif",
    "Mahdi", "Mahmoud", "Majid", "Mansoor", "Marwan", "Mubarak", "Mubin", "Mumtaz", "Munir", "Musa",
    "Naeem", "Nasir", "Numan", "Nur", "Qasim", "Rafiq", "Raheem", "Rashid", "Raza", "Ridwan",
    "Sabir", "Sadiq", "Saeed", "Salah", "Saleem", "Salim", "Samad", "Sami", "Samir", "Shakir",
    "Sharif", "Shihab", "Siddiq", "Tahir", "Talib", "Taqi", "Tariq", "Tawfiq", "Wafi", "Wajid",
    "Waleed", "Wasim", "Yaseen", "Yasir", "Yousef", "Yusuf", "Zafar", "Zahid", "Zaid", "Zain",
    # Female middle names
    "Aaliyah", "Afifa", "Alima", "Amira", "Anisa", "Arwa", "Asma", "Aziza", "Bahija", "Basima",
    "Fadila", "Faiza", "Farida", "Habiba", "Hafsa", "Hajra", "Halima", "Hamida", "Hanifa", "Hasna",
    "Huda", "Ihsan", "Inaya", "Jamilah", "Karima", "Khalida", "Latifa", "Lubna", "Madiha", "Manal",
    "Maryam", "Munira", "Nabila", "Nadira", "Naima", "Najma", "Nasreen", "Nawra", "Nazira", "Nusrat",
    "Qadira", "Rabia", "Rahima", "Rashida", "Razia", "Sabira", "Sadiqa", "Safiya", "Sahar", "Saida",
    "Sakina", "Salima", "Samira", "Shahida", "Shakira", "Shamsa", "Shirin", "Siddiqah", "Tahira", "Taliba",
    "Tamara", "Taqwa", "Thana", "Umayma", "Wafaa", "Wahida", "Warda", "Wasima", "Yumna", "Zahira",
    "Zahra", "Zakiya", "Zainab", "Zubaidah",
    "Rasheed", "Haleem", "Adeel", "Sami", "Sajid", "Naseem", "Imran", "Younis", "Shahzad", "Zeeshan",
    "Farooq", "Sadiq", "Saif", "Kareem", "Tariq", "Amin", "Rafique", "Feroz", "Waseem", "Hafiz",
    "Riaz", "Aslam", "Sultan", "Aftab", "Rauf", "Naeem", "Waheed", "Fawad", "Shabbir", "Qadeer",
    "Mehmood", "Rashida", "Nighat", "Shazia", "Sadia", "Lubna", "Shamim", "Mumtaz", "Nazia", "Parveen"
]
LAST_NAMES = [
    "Khan", "Hussain", "Ahmed", "Ali", "Mohammed", "Syed", "Sheikh", "Malik", "Mirza", "Beg",
    "Qureshi", "Siddiqui", "Ansari", "Farooqi", "Usmani", "Chaudhry", "Abbasi", "Jafari", "Kazmi", "Rizvi",
    "Hassan", "Rahman", "Abdullah", "Iqbal", "Sharif", "Bakr", "Omar", "Osman", "Zaman", "Alvi",
    "Abbas", "Abbassi", "Abidi", "Abubaker", "Abubakar", "Adil", "Afridi", "Agha", "Ahmad", "Ahmadi",
    "Akbar", "Akbari", "Akhtar", "Akhundzada", "Alavi", "Alim", "Amiri", "Ansar", "Anwari", "Arif",
    "Ashraf", "Askari", "Asker", "Aslam", "Awan", "Ayub", "Azad", "Azam", "Azhar", "Aziz",
    "Azizi", "Babar", "Badri", "Bahadur", "Bahri", "Baloch", "Baluch", "Bangash", "Baqri", "Bashar",
    "Bashir", "Bhatti", "Bukhari", "Butt", "Chishti", "Choudhary", "Daoud", "Darwish", "Dehlavi", "Durrani",
    "Ebrahimi", "Elahi", "Emami", "Farhat", "Farid", "Farooq", "Fawzi", "Ghafoor", "Ghani", "Ghaznavi",
    "Ghazali", "Ghouri", "Gilani", "Gul", "Habibi", "Hafeez", "Hafiz", "Hakimi", "Hamid", "Hanif",
    "Haq", "Haroon", "Hashemi", "Hashmi", "Hassani", "Hayat", "Hayyat", "Hekmat", "Hosseini", "Humayun",
    "Hussaini", "Ibrahim", "Idrisi", "Imam", "Isfahani", "Ismail", "Israili", "Jabbar", "Jafri", "Jalali",
    "Jamali", "Javid", "Jawad", "Javed", "Jilani", "Junaid", "Kakar", "Kalam", "Kaleem", "Karimi",
    "Kashani", "Kazemi", "Kazi", "Kermani", "Khalid", "Khalil", "Khatib", "Khattak", "Khawaja", "Khorasani",
    "Khoso", "Kirmani", "Kohistani", "Kundi", "Lahori", "Lodhi", "Lodin", "Lone", "Madani", "Mahdi",
    "Mahmood", "Mahmoud", "Mahmudi", "Majeed", "Majidi", "Makhdoom", "Maleki", "Mandvi", "Mansoor", "Mansouri",
    "Marwat", "Masood", "Mazari", "Mirwais", "Mohammadi", "Mohsin", "Moin", "Moosavi", "Mughal", "Mukhtar",
    "Murad", "Mushtaq", "Nabi", "Nadeem", "Naderi", "Nagi", "Najafi", "Najjar", "Naqvi", "Naseri",
    "Nasir", "Nasseri", "Nawaz", "Niazi", "Noorani", "Noor", "Nouri", "Pashtun", "Pasha", "Patel",
    "Qadir", "Qadri", "Qasemi", "Qazi", "Rabbani", "Raees", "Rafiq", "Rahbar", "Rahimi", "Rahim",
    "Rahmani", "Rais", "Rajput", "Ramzi", "Rasheed", "Rashid", "Rauf", "Raza", "Rehman", "Rezaei",
    "Riaz", "Roshani", "Roshan", "Rostami", "Sadat", "Sadeghi", "Sadeq", "Saeed", "Safavi", "Safi",
    "Sahni", "Sajjad", "Saleh", "Salim", "Sami", "Samir", "Sarwar", "Sattar", "Sattari", "Shaikh",
    "Shakoor", "Shams", "Sharifi", "Sherazi", "Siddiq", "Sulaimani", "Sultani", "Suri", "Tabatabai", "Taheri",
    "Taimuri", "Talib", "Talpur", "Tamimi", "Tanvir", "Taqvi", "Tareen", "Tarin", "Tirmizi", "Turabi",
    "Umar", "Umer", "Usama", "Wali", "Wani", "Warsi", "Wazir", "Yacoub", "Yaqoob", "Yasir",
    "Yazdani", "Younus", "Yousaf", "Yousafzai", "Yousuf", "Yousufzai", "Yousufi", "Zahedi", "Zahid", "Zaidi",
    "Zain", "Zaman", "Zamani", "Zia", "Zubair", "Zubairi",
    "Ansar", "Barakat", "Zaman", "Rasheed", "Shah", "Qadir", "Haneef", "Naseer", "Awan", "Chishti",
    "Dar", "Farid", "Ghani", "Hashmi", "Iqbal", "Jalil", "Khalid", "Latif", "Mahmood", "Nawaz",
    "Osman", "Parvez", "Qamar", "Rafique", "Sadiq", "Tahir", "Usman", "Waqar", "Yasin", "Zahid"
]


def generate_random_name(name_list):
    """Selects a random name from the provided list."""
    if not name_list:
        return ""
    return random.choice(name_list)


def clean_phone_number(phone_number):
    """
    Cleans and formats a phone number by removing non-numeric characters,
    except for the leading '+' sign.

    Args:
        phone_number: The phone number to clean

    Returns:
        A cleaned phone number with only digits and possibly a leading '+'
    """
    if not isinstance(phone_number, str):
        # Convert to string if it's not already
        phone_number = str(phone_number)

    # Keep the leading '+' if it exists
    has_plus = phone_number.startswith('+')

    # Remove all non-numeric characters
    cleaned_number = re.sub(r'[^0-9]', '', phone_number)

    # Add back the '+' if it was there originally
    if has_plus:
        cleaned_number = '+' + cleaned_number

    return cleaned_number


def convert_excel_to_custom_csv(input_file_path, phone_column_identifier, output_csv_path):
    """
    Converts an Excel or CSV file to a new CSV file with specified columns and generated data.

    Args:
        input_file_path (str): Path to the input Excel or CSV file.
        phone_column_identifier (str or int): Name or index of the column containing phone numbers.
        output_csv_path (str): Path to save the generated CSV file.
    """
    try:
        # Try reading as Excel first
        df_input = None
        try:
            df_input = pd.read_excel(input_file_path, sheet_name=0)  # Read the first sheet
            print(f"Successfully read '{input_file_path}' as an Excel file.")
        except Exception as e_excel:
            print(f"Could not read '{input_file_path}' as Excel: {e_excel}")
            # If Excel read fails, try reading as CSV, especially if the extension suggests it
            if input_file_path.lower().endswith('.csv'):
                try:
                    df_input = pd.read_csv(input_file_path)
                    print(f"Successfully read '{input_file_path}' as a CSV file.")
                except Exception as e_csv:
                    print(f"Also could not read '{input_file_path}' as CSV: {e_csv}")
                    return
            else:
                print("Please ensure the input file is a valid Excel (.xlsx, .xls) or CSV (.csv) file.")
                return

        if df_input is None:
            print(f"Failed to read the input file: {input_file_path}")
            return

        # Extract phone numbers
        phone_numbers_series = None
        if isinstance(phone_column_identifier, str):  # If column name is provided
            if phone_column_identifier not in df_input.columns:
                print(f"Error: Column '{phone_column_identifier}' not found in the input file.")
                print(f"Available columns are: {df_input.columns.tolist()}")
                return
            phone_numbers_series = df_input[phone_column_identifier]
        elif isinstance(phone_column_identifier, int):  # If column index is provided
            if phone_column_identifier >= len(df_input.columns) or phone_column_identifier < 0:
                print(f"Error: Column index {phone_column_identifier} is out of bounds for the input file.")
                print(
                    f"File has {len(df_input.columns)} columns (0-indexed). Available columns: {df_input.columns.tolist()}")
                return
            phone_numbers_series = df_input.iloc[:, phone_column_identifier]
        else:
            print("Error: 'phone_column_identifier' must be a string (column name) or an integer (column index).")
            return

        output_data_rows = []
        generated_names_set = set()

        for phone_number in phone_numbers_series:
            # Clean the phone number to ensure it contains only digits (and possibly a leading '+')
            cleaned_phone_number = clean_phone_number(phone_number)

            # Generate unique name
            max_attempts = 10
            for _ in range(max_attempts):
                first_name = generate_random_name(FIRST_NAMES)
                middle_name = generate_random_name(MIDDLE_NAMES)
                last_name = generate_random_name(LAST_NAMES)
                # Avoid first name and middle name being the same, if middle name is also a common first name
                if first_name == middle_name and middle_name in FIRST_NAMES:
                    temp_middle_names = [m for m in MIDDLE_NAMES if m != first_name]
                    if temp_middle_names:
                        middle_name = generate_random_name(temp_middle_names)
                    else:
                        middle_name = ""
                full_name_tuple = (first_name, middle_name, last_name)
                if full_name_tuple not in generated_names_set:
                    generated_names_set.add(full_name_tuple)
                    break
            else:
                # If all attempts fail, allow duplicate (very unlikely)
                pass

            row = {
                "Name Prefix": "QTS",
                "FirstName": first_name,
                "Middle Name": middle_name,
                "Last Name": last_name,
                "Phonetic First Name": first_name,  # Same as generated FirstName
                "Phonetic Last Name": last_name,  # Same as generated LastName
                "Phone 1 - Value": cleaned_phone_number,
                "Organization Name": "Quadrate Tech Solutions",
                "Organization Title": "QTS",
                "Website 1 - Value": "https://quadrate.lk"
            }
            output_data_rows.append(row)

        if not output_data_rows:
            print("No data processed. The phone number column might be empty or the input file is empty.")
            # Create an empty CSV with headers if no data rows
            df_output = pd.DataFrame(columns=[
                "Name Prefix", "FirstName", "Middle Name", "Last Name",
                "Phonetic First Name", "Phonetic Last Name", "Phone 1 - Value",
                "Organization Name", "Organization Title", "Website 1 - Value"
            ])
        else:
            df_output = pd.DataFrame(output_data_rows)

        # Ensure the column order is as requested
        column_order = [
            "Name Prefix", "FirstName", "Middle Name", "Last Name",
            "Phonetic First Name", "Phonetic Last Name", "Phone 1 - Value",
            "Organization Name", "Organization Title", "Website 1 - Value"
        ]
        df_output = df_output[column_order]

        # Save the output DataFrame to a CSV file
        df_output.to_csv(output_csv_path, index=False, encoding='utf-8')
        print(f"Successfully converted and saved data to '{output_csv_path}'")

    except FileNotFoundError:
        print(f"Error: The input file '{input_file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# --- Configuration and Execution ---
if __name__ == "__main__":
    # IMPORTANT: Modify these values according to your needs.

    # 1. Set the path to your input Excel or CSV file.
    #    Example: "data/my_phone_list.xlsx" or "phone_numbers.xlsx - Sheet1.csv"
    #    If the file is in the same directory as the script, just its name is enough.
    INPUT_FILE_PATH = "phone_numbers.xlsx"  # <--- CHANGE THIS

    # 2. Specify the column containing phone numbers.
    #    This can be the column's name (string) or its index (integer, 0-based).
    #    Example: If phone numbers are in a column named "Contact", use "Contact".
    #    Example: If phone numbers are in the first column, use 0.
    #             If in the second column, use 1, and so on.
    PHONE_NUMBER_COLUMN = 0  # <--- CHANGE THIS (e.g., "Phone" or 0)

    # 3. Set the desired name for the output CSV file.
    OUTPUT_CSV_PATH = "qts_contacts.csv"  # <--- CHANGE THIS (if needed)

    print("--- Starting Excel to Custom CSV Conversion (Islamic Names) ---")
    print(f"Input file: {INPUT_FILE_PATH}")
    print(f"Phone number column identifier: {PHONE_NUMBER_COLUMN}")
    print(f"Output CSV file: {OUTPUT_CSV_PATH}")
    print("-------------------------------------------------")

    convert_excel_to_custom_csv(INPUT_FILE_PATH, PHONE_NUMBER_COLUMN, OUTPUT_CSV_PATH)

    print("-------------------------------------------------")
    print("--- Conversion process finished ---")
