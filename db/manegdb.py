import pandas as pd
import sqlite3


# Load the CSV file into a pandas DataFrame
csv_file_path = r'C:\Users\99888\flight\db\flight_dataset.csv'  # Use raw string notation to avoid backslash issues
df = pd.read_csv(csv_file_path)

# Create a connection to the database (using SQLite for this example)
df.columns = df.columns.str.strip()


connection = sqlite3.connect('flight.db')
# Write the DataFrame to the SQL table
table_name = 'flights'
df.to_sql(table_name,connection, if_exists='replace', index=False)

print(f"Data successfully imported into the '{table_name}' table.")
