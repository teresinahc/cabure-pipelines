#!/bin/sh

for year in `seq 2013 $(date +'%Y')`; do
  echo "Dumping for ${year}"
  luigi --local-scheduler --module cabure RunForYear --year $year
done