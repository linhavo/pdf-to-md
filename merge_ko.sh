#!/bin/bash

OUTPUT="outputs/KO/KO_combined.md"

> "$OUTPUT"

for f in outputs/KO/1_Basic_KO.md \
          outputs/KO/2_ILP.md \
          outputs/KO/3_SPT_KO.md \
          outputs/KO/4_Flows_KO.md \
          outputs/KO/5_Knapsack.md \
          outputs/KO/6_TSP.md \
          outputs/KO/7_Sched_KO.md \
          outputs/KO/8_CP_KO.md; do
  cat "$f" >> "$OUTPUT"
  echo -e "\n\n---\n" >> "$OUTPUT"
done

echo "Created $OUTPUT"
