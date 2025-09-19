#!/bin/bash

LiCSARweb="/gws/nopw/j04/nceo_geohazards_vol1/public/LiCSAR_products"
frameID="$1"
CARPETA="$1"

mkdir -p "$CARPETA"
cd "$CARPETA"

# Extraer trackID numérico (antes de la primera letra)
digits="${frameID%%[A-Za-z]*}"
trackID=$((10#$digits))

echo "############# GACOS link ##############"
epochdir="$LiCSARweb/$trackID/$frameID/epochs"
gacosdir="GACOS"
mkdir -p "$gacosdir"

if [[ -d "$epochdir" ]]; then
  for epoch_path in "$epochdir"/*; do
    gacosfile=$(ls "$epoch_path"/*sltd*.geo.tif 2>/dev/null | head -n 1)
    if [[ -f "$gacosfile" ]]; then
      dest="$gacosdir/$(basename "$gacosfile")"
      [[ ! -e "$dest" ]] && ln -s "$gacosfile" "$dest"
    fi
  done
fi

echo "############# ERA5 link ##############"
era5dir="ERA5"
mkdir -p "$era5dir"

if [[ -d "$epochdir" ]]; then
  for epoch_path in "$epochdir"/*; do
    era5file=$(ls "$epoch_path"/*icams*.sltd.geo.tif 2>/dev/null | head -n 1)
    if [[ -f "$era5file" ]]; then
      dest="$era5dir/$(basename "$era5file")"
      [[ ! -e "$dest" ]] && ln -s "$era5file" "$dest"
    fi
  done
fi

echo "############# Interferograms ##############"

TIFS="$LiCSARweb/$trackID/$frameID/interferograms"

# Comprobar que el directorio exista y tenga subdirectorios
if [[ -d "$TIFS" && $(ls -A "$TIFS") ]]; then
    mkdir -p GEOC

    for pair_path in "$TIFS"/*_*; do
        [[ -d "$pair_path" ]] || continue
        pairname=$(basename "$pair_path")
        target_dir="GEOC/$pairname"
        mkdir -p "$target_dir"

        # Crear enlaces simbólicos de los .tif si existen
        for tif in "$pair_path"/*.tif; do
            [[ -f "$tif" ]] && ln -s "$tif" "$target_dir/"
        done
    done
else
    echo "No se encontraron interferogramas en $TIFS, se salta esta sección."
fi


echo "############# Baselines ##############"
mkdir -p GEOC
echo ${PWD}
cd GEOC
baselines_src="$LiCSARweb/$trackID/$frameID/metadata/baselines"
if [[ -d "$baselines_src" ]]; then
   ln -s "$baselines_src" ${PWD}/
fi

metadata_src="$LiCSARweb/$trackID/$frameID/metadata"

if [[ -d "$metadata_src" ]]; then
    for item in "$metadata_src"/*; do
        ln -s "$item" "${PWD}/"
    done
fi


echo "############# Master MLI ##############"

# Obtener la primera fecha (subdirectorio) en $epochdir
master=$(ls -1 "$epochdir" 2>/dev/null | head -n1)

# Crear link del master MLI si existe
master_file="$epochdir/$master/$master.geo.mli.tif"
if [[ -f "$master_file" ]]; then
    ln -s "$master_file" ${PWD}/
else
    # Si no existe master, enlazar la última imagen disponible
    lastimg=$(ls "$epochdir"/*/*.geo.mli.tif 2>/dev/null | tail -n1)
    [[ -n "$lastimg" ]] && ln -s "$lastimg" ${PWD}/
fi





