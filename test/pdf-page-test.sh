#!/bin/sh
cd output;
echo $(pwd)
echo $(ls)
NUM_OF_PAGES=$(pdfinfo resume.pdf | grep 'Pages' | awk '{print $2}');
if (( $NUM_OF_PAGES > 1 )); then
    return 1;
fi
return 0;