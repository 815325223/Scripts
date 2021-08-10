file=/data/flowcell_for_deletion
echo "begin-at `date`"
for i in `cat ${file}`;do rsync --delete-before -a -H -v --stats /opt/blank/ $i;echo "rm $i finished at `date`"; done
if diff /dev/null ${file} | tail -1 | grep '^\\ No newline' > /dev/null;then
  echo >> ${file}
fi
cat ${file} | while read line
do
  rm -rf $line
done
sleep 3
rm -rf ${file}
echo "finish-at `date`"
