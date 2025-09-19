import os
import pandas as pd

# Carpeta GEOC
directorio = "GEOC"
carpetas = [f for f in os.listdir(directorio) 
            if f.startswith('2') and os.path.isdir(os.path.join(directorio, f))]

# Convertir a DataFrame
df = pd.DataFrame([c.split('_') for c in carpetas], columns=['start', 'end'])
df['start'] = pd.to_datetime(df['start'], format='%Y%m%d')
df['end'] = pd.to_datetime(df['end'], format='%Y%m%d')
df = df.sort_values('start').reset_index(drop=True)

# Detectar huecos (islas)
islas = []
for i in range(len(df)-1):
    if df.loc[i, 'end'] < df.loc[i+1, 'start'] - pd.Timedelta(days=1):
        islas.append((df.loc[i, 'end'], df.loc[i+1, 'start']))

# Guardar fechas de gaps en archivo, ajustando un mes antes y un mes después
with open('gaps_dates.txt', 'w') as f:
    for gap_start, gap_end in islas:
        gap_start_adj = gap_start - pd.DateOffset(months=1)
        gap_end_adj = gap_end + pd.DateOffset(months=1)
        f.write(f"{gap_start_adj.strftime('%Y-%m-%d')} {gap_end_adj.strftime('%Y-%m-%d')}\n")

print("Archivo 'gaps_dates.txt' generado con las fechas de los gaps ajustadas un mes antes y después.")
