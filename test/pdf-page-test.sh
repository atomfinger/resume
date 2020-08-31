#!/bin/sh
NUM_OF_PAGES=$(exiftool -T -filename -PageCount -s3 -ext pdf ~/output/resume.pdf);
if (( $NUM_OF_PAGES > 1 )); then
    return 1;
fi
return 0;