#!/bin/bash
for  file  in  *.txt; do
cat -v "$file" > "$file"
done
exit 0
