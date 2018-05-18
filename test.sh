#!/bin/bash
for  file  in  *; do
file -b --mime-encoding "$file"
done
exit 0