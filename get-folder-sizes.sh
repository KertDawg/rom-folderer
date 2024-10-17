#!/bin/bash

Sizes=`du -a  $1| cut -d/ -f2 | sort | uniq -c | sort -nr`
readarray -t SizeArray <<< $Sizes

echo "Folder,FileCount"

for Folder in "${SizeArray[@]}"; do
    FolderArray=($Folder)
    echo "${FolderArray[1]},${FolderArray[0]}"
done
