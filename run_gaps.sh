#!/bin/bash
python gaps_dates.py
# Archivo con los gaps
archivo="gaps_dates.txt"

# Nombre del directorio actual
current_dir=$(basename "$(pwd)")

# Leer línea por línea
while read -r start end; do
    # Ejecutar el comando para cada línea
    licsar_make_frame.sh -P -f current_dir="$current_dir" 1 1 "$start" "$end"
done < "$archivo"
