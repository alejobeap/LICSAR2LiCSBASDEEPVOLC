import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

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
coberturas = []
if len(intervalos) > 0:
    rango_ini = intervalos[0].start
    rango_fin = intervalos[0].end

    for i in range(1, len(intervalos)):
        inicio = intervalos[i].start
        fin = intervalos[i].end
        if inicio <= rango_fin:  
            # Se solapan → extender
            rango_fin = max(rango_fin, fin)
        else:
            # Cerrar cobertura anterior
            coberturas.append((rango_ini, rango_fin))
            # Gap entre bloques
            gaps.append((rango_fin, inicio))
            # Nuevo bloque
            rango_ini, rango_fin = inicio, fin

    # Última cobertura
    coberturas.append((rango_ini, rango_fin))

    # Gap hasta hoy si aplica
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


# ============================
fig, ax = plt.subplots(figsize=(10, 2))

# Dibujar coberturas
for start, end in coberturas:
    ax.plot([start, end], [1, 1], color="green", linewidth=6, solid_capstyle="butt")

# Dibujar gaps
for start, end in gaps:
    ax.plot([start, end], [1, 1], color="red", linewidth=6, solid_capstyle="butt")

# Línea de "hoy"
today = pd.Timestamp(datetime.today().date())
ax.axvline(today, color="blue", linestyle="--", linewidth=1)
ax.text(today, 1.1, "Hoy", color="blue", ha="center")

# Formato del gráfico
ax.set_yticks([])
ax.set_ylim(0.5, 1.5)
ax.set_title("Coberturas y Gaps en GEOC", fontsize=12)
ax.grid(axis="x", linestyle="--", alpha=0.5)

# Guardar
plt.tight_layout()
plt.savefig("timeline.png", dpi=150)
plt.close()

print("Gráfico guardado como 'timeline.png'")
