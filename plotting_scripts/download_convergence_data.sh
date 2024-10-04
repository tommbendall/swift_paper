#!/bin/bash

# Script for downloading convergence results for SWIFT paper
branch_stem="r3751_swift_rev_plus"
compiler="intel_fast-debug-64bit"
results_location="/home/d03/tbendall/cylc-run"
to_path="/data/users/tbendall/results/swift_revision"
machine="xc40"
run="run2"

schemes=("cosmic" "swift")

# ---------------------------------------------------------------------------- #
# Download results for constant dt
# ---------------------------------------------------------------------------- #

dts=("0p05" "0p05" "0p05" "0p05" "0p025" "0p025")
results_dirname_stem="${results_location}/${branch_stem}/${run}/work/1/run_transport_"

# TESTS 1 - 4
resolutions=("BiP256x256-1000x1000" \
             "BiP512x512-1000x1000" \
             "BiP300x300-1000x1000" \
             "BiP400x400-1000x1000" \
             "BiP600x600-1000x1000" \
             "BiP700x700-1000x1000")

for ((i=1; i<3; i++))
do
  j=$(( 2*i ))
  for res_idx in "${!resolutions[@]}"
  do

    res="${resolutions[res_idx]}_${dts[j-1]}"

    for scheme_idx in "${!schemes[@]}"
    do
      scheme=${schemes[scheme_idx]}

      from_file="xcel00:${results_dirname_stem}${scheme}_test_${j}_conv_${res}_${machine}_${compiler}/PET00.transport.Log"
      tmp_file="${to_path}/tmp.log"
      to_file="${to_path}/${scheme}_test_${j}_conv_${res}.log"

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

for ((i=3; i<4; i++))
do
  j=$(( 2*i ))
  for res_idx in "${!resolutions[@]}"
  do

    res="${resolutions[res_idx]}_${dts[j-1]}"

    for scheme_idx in "${!schemes[@]}"
    do
      scheme=${schemes[scheme_idx]}

      from_file="xcel00:${results_dirname_stem}${scheme}_test_${j}_conv_${res}_${machine}_${compiler}/PET*0.transport.Log"
      tmp_file="${to_path}/tmp.log"
      to_file="${to_path}/${scheme}_test_${j}_conv_${res}.log"

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

dts=("4p0" "2p0" "1p0" "0p5")

# TESTS 2, 4, 6
resolutions=("BiP64x64-1000x1000" \
             "BiP128x128-1000x1000" \
             "BiP256x256-1000x1000" \
             "BiP512x512-1000x1000")

for ((i=1; i<4; i++))
do
  j=$(( 2*i ))
  for res_idx in "${!resolutions[@]}"
  do

    res="${resolutions[res_idx]}_${dts[res_idx]}"

    for scheme_idx in "${!schemes[@]}"
    do
      scheme=${schemes[scheme_idx]}

      from_file="xcel00:${results_dirname_stem}${scheme}_test_${j}_conv_${res}_${machine}_${compiler}/PET00.transport.Log"
      tmp_file="${to_path}/tmp.log"
      to_file="${to_path}/${scheme}_test_${j}_conv_${res}.log"

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

dts=("0p4" "0p2" "0p1" "0p05")

# TESTS 2, 4, 6
resolutions=("BiP64x64-1000x1000" \
             "BiP128x128-1000x1000" \
             "BiP256x256-1000x1000" \
             "BiP512x512-1000x1000")

for ((i=1; i<4; i++))
do
  j=$(( 2*i ))
  for res_idx in "${!resolutions[@]}"
  do

    res="${resolutions[res_idx]}_${dts[res_idx]}"

    for scheme_idx in "${!schemes[@]}"
    do
      scheme=${schemes[scheme_idx]}

      from_file="xcel00:${results_dirname_stem}${scheme}_test_${j}_conv_${res}_${machine}_${compiler}/PET00.transport.Log"
      tmp_file="${to_path}/tmp.log"
      to_file="${to_path}/${scheme}_test_${j}_conv_${res}.log"

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
# Download results for 3D big CFL
# ---------------------------------------------------------------------------- #

dts=("2p5" "2p0" "1p25")
short_res_all=("64" "80" "128")

resolutions=("BiP1000x1000-64" \
             "BiP1000x1000-80" \
             "BiP1000x1000-128")

for res_idx in "${!short_res_all[@]}"
do

  res="${short_res_all[res_idx]}_${dts[res_idx]}"
  full_res="${resolutions[res_idx]}"

  for scheme_idx in "${!schemes[@]}"
  do
    scheme=${schemes[scheme_idx]}

    from_file="xcel00:${results_dirname_stem}${scheme}_skam3d_conv_${res}-${full_res}_${machine}_${compiler}/PET*0.transport.Log"
    tmp_file="${to_path}/tmp.log"
    to_file="${to_path}/${scheme}_skam3d_conv_${res}.log"

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

# ---------------------------------------------------------------------------- #
# Download results for 3D small CFL
# ---------------------------------------------------------------------------- #

dts=("0p25" "0p2" "0p125")
short_res_all=("64" "80" "128")

resolutions=("BiP1000x1000-64" \
             "BiP1000x1000-80" \
             "BiP1000x1000-128")

for res_idx in "${!short_res_all[@]}"
do

  res="${short_res_all[res_idx]}_${dts[res_idx]}"
  full_res="${resolutions[res_idx]}"

  for scheme_idx in "${!schemes[@]}"
  do
    scheme=${schemes[scheme_idx]}

    from_file="xcel00:${results_dirname_stem}${scheme}_skam3d_conv_${res}-${full_res}_${machine}_${compiler}/PET*0.transport.Log"
    tmp_file="${to_path}/tmp.log"
    to_file="${to_path}/${scheme}_skam3d_conv_${res}.log"

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
