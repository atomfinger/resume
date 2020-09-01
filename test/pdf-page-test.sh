#!/bin/bash
cd output;
echo $(pwd);
echo $(ls);
NUM_OF_PAGES=$(pdfinfo resume.pdf | grep 'Pages' | awk '{print $2}');
echo "Num of pages found $NUM_OF_PAGES";
if (($NUM_OF_PAGES > 1)); then
    echo "Too many pages ($NUM_OF_PAGES)";
    exit 1;
fi
exit 0;