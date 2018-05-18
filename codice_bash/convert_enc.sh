#!/bin/bash
#enter input encoding here
#FROM_ENCODING="value_here"
#output encoding(UTF-8)
TO_ENCODING="UTF-8"
#loop to convert multiple files 
for  file  in  *.txt; do
#convert
FROM_ENCODING=$(file -b --mime-encoding "$file")
if [ "$FROM_ENCODING" = "binary" ];	then
	FROM_ENCODING=$(chardet3 "$file" | awk '{print $(NF-3)}')
	recode $FROM_ENCODING "$file"
	cp "$file" ../convertiti/"$file"
fi
if [ "$FROM_ENCODING" = "unknown-8bit" ];	then
	FROM_ENCODING=$(chardet3 "$file" | awk '{print $(NF-3)}')
	recode $FROM_ENCODING "$file"
	cp "$file" ../convertiti/"$file"
fi
CONVERT=" iconv  -f   $FROM_ENCODING  -t   $TO_ENCODING"
$CONVERT   "$file"   -o  ../convertiti/"$file"
done
exit 0
