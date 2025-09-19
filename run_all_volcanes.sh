#!/bin/bash

# Archivo con la lista de clips
input_file="156D_11424_131313_clips.txt"

# Iterar sobre cada línea
while read -r line; do
    clip_name=$(echo "$line" | awk '{print $1}')
    
    echo "Enviando trabajo para: $clip_name"

    # Crear un script temporal que ejecute batch_LiCSBAS.sh con el clip
    tmp_script="jasmin_run_${clip_name}.sh"
    echo -e "#!/bin/bash\nmodule load licsbas_comet_dev\n./batch_LiCSBAS.sh $clip_name" > $tmp_script
    chmod +x $tmp_script

    # Enviar el trabajo a la cola usando bsub2slurm.sh
    parent_dir=$(basename "$(dirname "$(pwd)")")
    current_dir=$(basename "$(pwd)")
    bsub2slurm.sh -o LB_${current_dir}_${clip_name}.out \
                  -e LB_${current_dir}_${clip_name}.err \
                  -J LiCSBAS_${current_dir}_${clip_name} \
                  -n 10 -W 23:59 -M 65536 -q short-serial ./$tmp_script
done < "$input_file"
