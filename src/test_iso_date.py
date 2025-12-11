from utils.operacionesDataframe import format_iso_date
import pandas as pd


df = pd.read_csv('csv/2025-03-28_suzuki_final.csv')

# print(df.type)

df['fecha_formateada'] = df['created_at'].apply(format_iso_date)

print(df[['created_at', 'fecha_formateada']].head(30))


