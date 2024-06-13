#!/bin/bash

# Script for downloading convergence results for SWIFT paper
branch_stem="r48987_swift_paper"
compiler="intel_64-bit_fast-debug"
results_location="/data/users/tbendall/cylc-run"
to_path="/data/users/tbendall/results/swift_paper"
machine="meto-spice"

schemes=("cosmic" "swift")

# ---------------------------------------------------------------------------- #
# Download results for 2D tests
# ---------------------------------------------------------------------------- #

test_type='two_d'
dts=("2p0" "0p2")
results_dirname_stem="${results_location}/${branch_stem}-transport-${machine}-${test_type}/work/1"

resolution="BiP128x128-1000x1000"

for ((i=1; i<7; i++))
do
  for dt_idx in "${!dts[@]}"
  do

    res="${resolution}_dt-${dts[dt_idx]}"

    for scheme_idx in "${!schemes[@]}"
    do
      scheme=${schemes[scheme_idx]}

      from_file="${results_dirname_stem}/run_transport_${scheme}_test_${i}_${res}_${compiler}/PET00.transport.Log"
      tmp_file="${to_path}/tmp.log"
      to_file="${to_path}/${scheme}_test_${i}_${res}.log"

      if [ -e ${to_file} ]; then
        rm ${to_file}
      fi

      touch ${to_file}

      cp ${from_file} ${tmp_file}

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
# Download results for 3D tests
# ---------------------------------------------------------------------------- #

test_type='three_d'
dts=("2p5" "0p25")
results_dirname_stem="${results_location}/${branch_stem}-transport-${machine}-${test_type}/work/1"

resolution="BiP64x64-1000x1000"

for dt_idx in "${!dts[@]}"
do

  res="${resolution}_dt-${dts[dt_idx]}"

  for scheme_idx in "${!schemes[@]}"
  do
    scheme=${schemes[scheme_idx]}

    from_file="${results_dirname_stem}/run_transport_${scheme}_skam3d_${res}_${compiler}/PET0.transport.Log"
    tmp_file="${to_path}/tmp.log"
    to_file="${to_path}/${scheme}_skam3d_${res}.log"

    if [ -e ${to_file} ]; then
      rm ${to_file}
    fi

    touch ${to_file}

    cp ${from_file} ${tmp_file}

    # Scrape data
    grep -r "Min-final" ${tmp_file} >> ${to_file}
    grep -r "Max-final" ${tmp_file} >> ${to_file}
    grep -r "L2-final" ${tmp_file} >> ${to_file}
    grep -r "Rel-L2-error" ${tmp_file} >> ${to_file}

    rm ${tmp_file}
  done
done

