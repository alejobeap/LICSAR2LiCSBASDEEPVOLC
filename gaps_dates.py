import os
import pandas as pd
from datetime import datetime

# Carpeta GEOC
directorio = "GEOC"
carpetas = [f for f in os.listdir(directorio)
            if f.startswith('2') and os.path.isdir(os.path.join(directorio, f))]

# Convertir a DataFrame
df = pd.DataFrame([c.split('_') for c in carpetas], columns=['start', 'end'])
df['start'] = pd.to_datetime(df['start'], format='%Y%m%d')
df['end'] = pd.to_datetime(df['end'], format='%Y%m%d')

# Ordenar intervalos por fecha de inicio
intervalos = df.sort_values('start')[['start', 'end']].to_records(index=False)

# Detectar gaps entre clusters
gaps = []
if len(intervalos) > 0:
    rango_fin = intervalos[0].end
    for i in range(1, len(intervalos)):
        inicio = intervalos[i].start
        fin = intervalos[i].end
        if inicio > rango_fin:
            # Gap detectado
            gap_start = rango_fin - pd.DateOffset(months=1)
            gap_end = inicio + pd.DateOffset(months=1)
            gaps.append((gap_start, gap_end))
        # Extender rango_fin al máximo del cluster
        rango_fin = max(rango_fin, fin)
    
    # Gap hasta hoy solo si el último intervalo terminó hace más de 2 semanas
    today = pd.Timestamp(datetime.today().date())
    if rango_fin < today - pd.Timedelta(weeks=2):
        gap_start = rango_fin - pd.DateOffset(months=1)
        gap_end = today + pd.DateOffset(months=1)
        gaps.append((gap_start, gap_end))

# Guardar gaps en archivo
with open('gaps_dates.txt', 'w') as f:
    for gap_start, gap_end in gaps:
        f.write(f"{gap_start.strftime('%Y-%m-%d')} {gap_end.strftime('%Y-%m-%d')}\n")

print(f"Detectados {len(gaps)} gaps. Archivo 'gaps_dates.txt' generado.")
