#!/bin/bash

# Script for downloading convergence results for SWIFT paper
branch_stem="r3751_swift_rev_plus"
compiler="intel_fast-debug-64bit"
results_location="/data/d03/tbendall/cylc-run"
to_path="/data/users/tbendall/results/swift_revision"
machine="xc40"
run="run2"

schemes=("cosmic" "swift")

# ---------------------------------------------------------------------------- #
# Download results for 2D tests
# ---------------------------------------------------------------------------- #

dts=("2p0" "0p2")
results_dirname_stem="${results_location}/${branch_stem}/${run}/work/1/run_transport_"

resolution="BiP128x128-1000x1000"

for ((i=1; i<7; i++))
do
  for dt_idx in "${!dts[@]}"
  do

    res="${resolution}_${dts[dt_idx]}"

    for scheme_idx in "${!schemes[@]}"
    do
      scheme=${schemes[scheme_idx]}

      from_file="xcel00:${results_dirname_stem}${scheme}_test_${i}_${res}_${machine}_${compiler}/lfric_initial.nc"
      to_file="${to_path}/${scheme}_test_${i}_${res}_initial.nc"

      scp ${from_file} ${to_file}

      from_file="xcel00:${results_dirname_stem}${scheme}_test_${i}_${res}_${machine}_${compiler}/lfric_diag.nc"
      to_file="${to_path}/${scheme}_test_${i}_${res}_diag.nc"

      scp ${from_file} ${to_file}
    done
  done
done

# ---------------------------------------------------------------------------- #
# Download results for 3D tests
# ---------------------------------------------------------------------------- #

dts=("2p5" "0p25")
short_res="64"
full_res="BiP1000x1000-64"

for dt_idx in "${!dts[@]}"
do

  res="${short_res}_${dts[dt_idx]}"

  for scheme_idx in "${!schemes[@]}"
  do
    scheme=${schemes[scheme_idx]}

    from_file="xcel00:${results_dirname_stem}${scheme}_skam3d_${res}-${full_res}_${machine}_${compiler}/lfric_initial.nc"
    to_file="${to_path}/${scheme}_skam3d_${res}_initial.nc"

    scp ${from_file} ${to_file}

    from_file="xcel00:${results_dirname_stem}${scheme}_skam3d_${res}-${full_res}_${machine}_${compiler}/lfric_diag.nc"
    to_file="${to_path}/${scheme}_skam3d_${res}_diag.nc"

    scp ${from_file} ${to_file}
  done
done

