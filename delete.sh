#!/bin/bash
for  file  in  *; do
if [ -f ../liber_liber/"$file" ]; then
	rm -f ../liber_liber/"$file"
fi
done
exit 0