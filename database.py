import pandas as pd

def read_data_from_csv_file():
    df = pd.read_excel('data_second_set_0522.xlsx',sheet_name="Consolidated_Data")
    df =  df[['ID','Vendor','Material','Material Description','Image Src']]
    df = df.dropna().reset_index(drop=True)
    return df


