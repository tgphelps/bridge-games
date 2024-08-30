#!/bin/sh

if [ $# != 1 ] ; then
    echo 'usage: store-session.sh <session-name.txt>'
    exit 1
fi
BASE=$(echo $1 | awk -F"." '{print $1}')
EXT=$(echo $1 | awk -F"." '{print $2}') 
echo name is $BASE $EXT
if [ $EXT != txt ] ; then
    echo bad filename
    exit 1
fi
python3 store-deals.py -s $BASE $1