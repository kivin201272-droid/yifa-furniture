import pandas as pd
import json

df = pd.read_excel('素材库/价钱/Furniture_Price_List_Adjusted (1).xlsx')
# Assuming it has the same structure as the CSV
# We can dump it to a temporary CSV or just output the missing codes
print("Columns:", df.columns.tolist())
df.to_csv('素材库/价钱/Furniture_Price_List_Adjusted_Excel.csv', index=False)
