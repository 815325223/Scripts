#!/bin/bash
SourceFile=./GAinternal.csv
SequencerList=$2
OutputFile=$3
SuzhouDir=/data/sz_seqdata
GuangzhouDir=/data/gz_seqdata
TianjinDir=/data/tj_seqdata

## filter location
filter(){
  cat ${SequencerList} | while read -r line1
  do
    cat ${SourceFile} | while read -r line2
    do
      if [[ "${line2,,}" =~ "${line1,,}" ]]; then
        echo $line2 >> $OutputFile
      fi
    done
  done
}

## convert Windows path to Linux path
convert(){
  if [ -f suzhou.step1 ]; then
    tr '\\' '/' < suzhou.step1 | sed "s#//GWAZUPROSMB3A/SeqData#${SuzhouDir}#g" > suzhou.step2
  else
    echo "suzhou.step1 not exist!"
  fi

  if [ -f guangzhou.step1 ]; then
  tr '\\' '/' < guangzhou.step1 | sed "s#//GWAZUPROSMB3A/SeqData#${GuangzhouDir}#g" > guangzhou.step2
  else
    echo "guangzhou.step1 not exist!"
  fi

  if [ -f tianjin.step1 ]; then
  tr '\\' '/' < tianjin.step1 | sed "s#//GWAZUPROSMB3A/SeqData#${TianjinDir}#g" > tianjin.step2
  else
    echo "tianjin.step1 not exist!"
  fi
}

## replace the correct sequencer name
regex(){
  if [ -f suzhou.step2 ]; then
    cat ${SequencerList} | while read -r line1
    do
      cat suzhou.step2 | while read -r line3
      do
        if [[ "${line3,,}" =~ "${line1,,}" ]]; then
          echo $line3 | sed "s#/\([^/]*\)/\([^/]*\)/\([^/]*\)/#/\1/\2/${line1}/#" >> suzhou.final
        fi
      done
    done
  else
    echo "suzhou.step2 not exist!"
  fi

  if [ -f guangzhou.step2 ]; then
    cat ${SequencerList} | while read -r line1
    do
      cat guangzhou.step2 | while read -r line3
      do
        if [[ "${line3,,}" =~ "${line1,,}" ]]; then
          echo $line3 | sed "s#/\([^/]*\)/\([^/]*\)/\([^/]*\)/#/\1/\2/${line1}/#" >> guangzhou.final
        fi
      done
    done
  else
    echo "guangzhou.step2 not exist!"
  fi

  if [ -f tianjin.step2 ]; then
    cat ${SequencerList} | while read -r line1
    do
      cat tianjin.step2 | while read -r line3
      do
        if [[ "${line3,,}" =~ "${line1,,}" ]]; then
          echo $line3 | sed "s#/\([^/]*\)/\([^/]*\)/\([^/]*\)/#/\1/\2/${line1}/#" >> tianjin.final
        fi
      done
    done
  else
    echo "tianjin.step2 not exist!"
  fi
}

case $1 in
  filter)
    filter
    ;;
  convert)
    convert
    ;;
  regex)
    regex
    ;;
  *)
  echo -e "Usage:\nsh Sort.sh filter szseqlist suzhou.step1\nsh Sort.sh convert\nsh Sort.sh regex szseqlist"
  ;;
esac
