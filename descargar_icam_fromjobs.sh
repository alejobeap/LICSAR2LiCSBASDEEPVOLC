#!/usr/bin/env bash
# Descargar icams inside folder
# P. Espin
# This script extracts final folder names and processes each using icams_one_epoch.sh.

# Get the current and parent directory names
parent_dir=$(basename "$(dirname "$(pwd)")")
current_dir=$(basename "$(pwd)")

# Extract and process the identifier from the current directory name
tr=$(echo "$current_dir" | cut -d '_' -f1 | sed 's/^0*//' | rev | cut -c 2- | rev)

# Ensure old lista.txt is removed before creating a new one
if [ -f "lista.txt" ]; then
    rm -f "lista.txt"
fi

ls -d /gws/nopw/j04/nceo_geohazards_vol1/public/LiCSAR_products/$tr/$current_dir/epochs/20* | awk -F'/' '{print $NF}' > lista.txt


if [ $? -ne 0 ]; then
    echo "Error: Failed to generate lista.txt. Check the directory path."
    exit 1
fi

mkdir log_ERA5
# Process each folder listed in lista.txt
while read -r line; do
    echo -e "$line"
    sbatch --qos=high --output=log_ERA5/ICAMS_${line}_${current_dir}.out --error=log_ERA5/ICAMS_${line}_${current_dir}.err --job-name=ICAMS_${line}_${current_dir} -n 8 --time=23:59:00 --mem=65536 -p comet --account=comet_lics --partition=standard --wrap="./icams_one_epoch.sh "$current_dir" "$line""
done < lista.txt
