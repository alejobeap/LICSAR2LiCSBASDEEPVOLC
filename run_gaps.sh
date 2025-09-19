#!/bin/bash

# Generar gaps_dates.txt
python gaps_dates.py

# Archivo con los gaps
archivo="gaps_dates.txt"

# Comprobar que el archivo existe y no está vacío
if [[ -s "$archivo" ]]; then
    # Nombre del directorio actual
    current_dir=$(basename "$(pwd)")

    # Leer línea por línea
    while read -r start end; do
        # Ejecutar el comando para cada línea
        licsar_make_frame.sh -P -f "$current_dir" 1 1 "$start" "$end"
    done < "$archivo"
else
    echo "No hay gaps en el archivo $archivo. No se ejecutará nada."
fi
