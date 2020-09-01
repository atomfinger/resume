#!/bin/bash
cd output;
echo $(pwd);
echo $(ls);
NUM_OF_PAGES=$(pdfinfo resume.pdf | grep 'Pages' | awk '{print $2}');
echo 'Num of pages found';
if (( $NUM_OF_PAGES > 1 )); then
    echo "Too many pages ($NUM_OF_PAGES)";
    return 1;
fi
return 0;