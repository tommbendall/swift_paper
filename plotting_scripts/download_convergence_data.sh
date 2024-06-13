#!/bin/bash

# Script for downloading convergence results for SWIFT paper
branch_stem="r48987_swift_paper"
compiler="intel_64-bit_fast-debug"
results_location="/data/d03/tbendall/cylc-run"
to_path="/data/users/tbendall/results/swift_paper"
machine="meto-xcs"

schemes=("cosmic" "swift")

# ---------------------------------------------------------------------------- #
# Download results for constant dt
# ---------------------------------------------------------------------------- #

test_type='const_dt_paper'
dts=("0p05" "0p05" "0p05" "0p05" "0p025" "0p025")
results_dirname_stem="${results_location}/${branch_stem}-transport-${machine}-converge_${test_type}/work/1"

# TESTS 1 - 4
resolutions=("BiP256x256-1000x1000" \
             "BiP512x512-1000x1000" \
             "BiP300x300-1000x1000" \
             "BiP400x400-1000x1000" \
             "BiP600x600-1000x1000" \
             "BiP700x700-1000x1000")

for ((i=1; i<5; i++))
do
  for res_idx in "${!resolutions[@]}"
  do

    res="${resolutions[res_idx]}_dt-${dts[i-1]}"

    for scheme_idx in "${!schemes[@]}"
    do
      scheme=${schemes[scheme_idx]}

      from_file="xcslr0:${results_dirname_stem}/run_transport_${scheme}_test_${i}_conv_${res}_${compiler}/PET00.transport.Log"
      tmp_file="${to_path}/tmp.log"
      to_file="${to_path}/${scheme}_test_${i}_conv_${res}.log"

      if [ -e ${to_file} ]; then
        rm ${to_file}
      fi

      touch ${to_file}

      scp ${from_file} ${tmp_file}

      # Scrape data
      grep -r "Min-final" ${tmp_file} >> ${to_file}
      grep -r "Max-final" ${tmp_file} >> ${to_file}
      grep -r "L2-final" ${tmp_file} >> ${to_file}
      grep -r "Rel-L2-error" ${tmp_file} >> ${to_file}

      rm ${tmp_file}
    done
  done
done

# TESTS 5 - 6
resolutions=("BiP64x64-1000x1000" \
             "BiP128x128-1000x1000" \
             "BiP256x256-1000x1000" \
             "BiP50x50-1000x1000" \
             "BiP100x100-1000x1000" \
             "BiP200x200-1000x1000")

for ((i=5; i<7; i++))
do
  for res_idx in "${!resolutions[@]}"
  do

    res="${resolutions[res_idx]}_dt-${dts[i-1]}"

    for scheme_idx in "${!schemes[@]}"
    do
      scheme=${schemes[scheme_idx]}

      from_file="xcslr0:${results_dirname_stem}/run_transport_${scheme}_test_${i}_conv_${res}_${compiler}/PET00.transport.Log"
      tmp_file="${to_path}/tmp.log"
      to_file="${to_path}/${scheme}_test_${i}_conv_${res}.log"

      if [ -e ${to_file} ]; then
        rm ${to_file}
      fi

      touch ${to_file}

      touch ${to_file}

      scp ${from_file} ${tmp_file}

      # Scrape data
      grep -r "Min-final" ${tmp_file} >> ${to_file}
      grep -r "Max-final" ${tmp_file} >> ${to_file}
      grep -r "L2-final" ${tmp_file} >> ${to_file}
      grep -r "Rel-L2-error" ${tmp_file} >> ${to_file}

      rm ${tmp_file}
    done
  done
done

# ---------------------------------------------------------------------------- #
# Download results for big CFL
# ---------------------------------------------------------------------------- #

test_type='big_cfl'
dts=("4p0" "2p0" "1p0" "0p5")
results_dirname_stem="${results_location}/${branch_stem}-transport-${machine}-converge_${test_type}/work/1"

# TESTS 1 - 6
resolutions=("BiP64x64-1000x1000" \
             "BiP128x128-1000x1000" \
             "BiP256x256-1000x1000" \
             "BiP512x512-1000x1000")

for ((i=1; i<7; i++))
do
  for res_idx in "${!resolutions[@]}"
  do

    res="${resolutions[res_idx]}_dt-${dts[res_idx]}"

    for scheme_idx in "${!schemes[@]}"
    do
      scheme=${schemes[scheme_idx]}

      from_file="xcslr0:${results_dirname_stem}/run_transport_${scheme}_test_${i}_conv_${res}_${compiler}/PET*0.transport.Log"
      tmp_file="${to_path}/tmp.log"
      to_file="${to_path}/${scheme}_test_${i}_conv_${res}.log"

      touch ${to_file}

      scp ${from_file} ${tmp_file}

      # Scrape data
      grep -r "Min-final" ${tmp_file} >> ${to_file}
      grep -r "Max-final" ${tmp_file} >> ${to_file}
      grep -r "L2-final" ${tmp_file} >> ${to_file}
      grep -r "Rel-L2-error" ${tmp_file} >> ${to_file}

      rm ${tmp_file}
    done
  done
done

# ---------------------------------------------------------------------------- #
# Download results for small CFL
# ---------------------------------------------------------------------------- #

test_type='small_cfl'
dts=("0p4" "0p2" "0p1" "0p05")
results_dirname_stem="${results_location}/${branch_stem}-transport-${machine}-converge_${test_type}/work/1"

# TESTS 1 - 6
resolutions=("BiP64x64-1000x1000" \
             "BiP128x128-1000x1000" \
             "BiP256x256-1000x1000" \
             "BiP512x512-1000x1000")

for ((i=1; i<7; i++))
do
  for res_idx in "${!resolutions[@]}"
  do

    res="${resolutions[res_idx]}_dt-${dts[res_idx]}"

    for scheme_idx in "${!schemes[@]}"
    do
      scheme=${schemes[scheme_idx]}

      from_file="xcslr0:${results_dirname_stem}/run_transport_${scheme}_test_${i}_conv_${res}_${compiler}/PET*0.transport.Log"
      tmp_file="${to_path}/tmp.log"
      to_file="${to_path}/${scheme}_test_${i}_conv_${res}.log"

      touch ${to_file}

      scp ${from_file} ${tmp_file}

      # Scrape data
      grep -r "Min-final" ${tmp_file} >> ${to_file}
      grep -r "Max-final" ${tmp_file} >> ${to_file}
      grep -r "L2-final" ${tmp_file} >> ${to_file}
      grep -r "Rel-L2-error" ${tmp_file} >> ${to_file}

      rm ${tmp_file}
    done
  done
done
