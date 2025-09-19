import sys
import re
import pandas as pd
import volcdb

# If no argument is given, use current directory name
if len(sys.argv) != 2:
    frame_id = os.path.basename(os.getcwd())
    print(f"No frame_id provided, using current directory: {frame_id}")
else:
    frame_id = sys.argv[1]

print(f"Frame ID: {frame_id}")

# Obtener DataFrame directamente desde volcdb
volcanoes = volcdb.get_volcanoes_in_frame(frame_id)

# Función para limpiar nombres: reemplaza cualquier secuencia de espacio o punto por un solo "_"
def limpiar_nombre(name):
    return re.sub(r'[ .]+', '_', str(name).strip())

# Tamaño aproximado del clip en grados (~12.5 km por lado, área ~25 km²)
clip_delta = 25 / 111.0  # 1° ≈ 111 km

output_lines = []

for _, row in volcanoes.iterrows():
    # Saltar filas con lat/lon nulos
    if pd.isnull(row['lat']) or pd.isnull(row['lon']):
        continue

    name = limpiar_nombre(row['name'])
    lat = float(row['lat'])
    lon = float(row['lon'])
    alt = int(row['alt']) if not pd.isnull(row['alt']) else 0

    lonmin = lon - clip_delta
    lonmax = lon + clip_delta
    latmin = lat - clip_delta
    latmax = lat + clip_delta

    clip_area = f"{lonmin:.6f}/{lonmax:.6f}/{latmin:.6f}/{latmax:.6f}"
    output_lines.append(f"{name} {lon:.6f} {lat:.6f} {clip_area} {alt:d} {frame_id}")

# Guardar en archivo
output_file = f"{frame_id}_clips.txt"
with open(output_file, 'w') as f:
    for line in output_lines:
        f.write(line + "\n")

print(f"Archivo generado: {output_file}")

