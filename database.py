import pandas as pd
import sqlite3

def read_data_from_csv_file():
    df = pd.read_excel('data_second_set_0522.xlsx',sheet_name="Consolidated_Data")
    df =  df[['ID','Vendor','Material','Material Description','Image Src']]
    df = df.dropna().reset_index(drop=True)
    return df

def create_schema():
    
    conn = sqlite3.connect('app_database.db',check_same_thread=False)
    c = conn.cursor()
    c.execute('''
          CREATE TABLE IF NOT EXISTS Clients
          ([user_id] INTEGER PRIMARY KEY, [name] TEXT, [email] TEXT UNIQUE, [password] TEXT)
          ''')
    c.execute('''
          CREATE TABLE IF NOT EXISTS Users
          ([user_id] INTEGER PRIMARY KEY, [Name] TEXT, [Age] INTEGER , [event] TEXT , [TIME] TEXT , [VENUE] TEXT, 
          [description] TEXT, [base_color] TEXT, [acsent_color] TEXT, [material] TEXT , [pattern_color] TEXT, 
          [kind_of_pattern] TEXT, [recommendation_type] TEXT )
          ''')
    c.execute('''
          CREATE TABLE IF NOT EXISTS UsersToProducts
          ([id] INTEGER PRIMARY KEY, [user_id] INTEGER , [product_id] INTEGER)
          ''')
    conn.commit()
    print("Schema Generated/Loaded Successfully")
    return c , conn


