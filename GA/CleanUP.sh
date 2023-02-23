#!/bin/bash
file=$1
sed -i '/^\s*$/d' $file

if [ -d /tmp/blank ]; then
    rm -rf /tmp/blank
fi

mkdir /tmp/blank
sleep 10
echo "begin-at `date`" >> time.log
cat $file | while read line
do
  rsync --delete-before -a -H -v --progress --stats /tmp/blank/ $line
  rmdir $line
done
echo "finish-at `date`" >> time.log
