#!/bin/bash
for  file  in  *.odt; do
odt2txt "$file" > "${file%.odt}.txt"
rm "$file"
done
exit 0
