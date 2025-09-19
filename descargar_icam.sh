#!/usr/bin/env bash
# Descargar icams inside folder
# P. Espin

# file 1 is lista from example:
# ls /gws/nopw/j04/nceo_geohazards_vol1/public/LiCSAR_products/40/040D_09102_131313/epochs/ -1 >> lista.txt

parent_dir=$(basename "$(dirname "$(pwd)")")
current_dir=$(basename "$(pwd)")

tr=$(echo $current_dir | cut -d '_' -f1 | sed 's/^0//' | sed 's/^0//' | rev | cut -c 2- | rev)

# Make sure lista.txt is fresh
if [ -f "lista.txt" ]; then
    rm -f lista.txt
fi

# Generate list of epochs
ls -d /gws/nopw/j04/nceo_geohazards_vol1/public/LiCSAR_products/$tr/$current_dir/epochs/2* \
    | awk -F'/' '{print $NF}' >> lista.txt

file="lista.txt"

# Loop over epochs
while read -r line; do
    echo "$line"
    ./icams_one_epoch.sh "$current_dir" "$line"
done < "$file"
