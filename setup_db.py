import pandas as pd
import sqlite3
import os

def setup_database():
    print("Starting Database Setup...")
    
    # Load the dataset
    dataset_path = "data/superstore.csv"
    if not os.path.exists(dataset_path):
        print(f"Error: {dataset_path} not found!")
        return

    print("Loading CSV...")
    df = pd.read_csv(dataset_path, encoding='latin-1')
    
    # Fix date columns
    print("Cleaning dates...")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date']  = pd.to_datetime(df['Ship Date'])

    # Create useful time columns
    df['Year']          = df['Order Date'].dt.year
    df['Month']         = df['Order Date'].dt.month
    df['Month_Name']    = df['Order Date'].dt.strftime('%b')
    df['Quarter']       = df['Order Date'].dt.quarter
    df['YearMonth']     = df['Order Date'].dt.to_period('M').astype(str)
    df['Days_to_Ship']  = (df['Ship Date'] - df['Order Date']).dt.days

    # Clean column names
    df.columns = df.columns.str.strip().str.replace(' ', '_')

    # Create SQLite database
    db_path = "data/sales.db"
    print(f"Creating SQLite database at {db_path}...")
    conn = sqlite3.connect(db_path)
    df.to_sql("sales", conn, if_exists="replace", index=False)
    
    # Verify
    result = pd.read_sql("SELECT COUNT(*) AS total_rows FROM sales", conn)
    print(f"Success! Loaded {result['total_rows'][0]} rows into database.")
    conn.close()

if __name__ == "__main__":
    setup_database()
