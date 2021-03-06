#!/bin/bash


function SFO-year () {
  if [ $# == 0 ];
  then
    echo "Get weather data for SF airport from weather underground for a given year"
    return 0
  fi
  YEAR=$1
  MONTHS=12
  if [ $YEAR == 2015 ];
  then
    MONTHS=6
  fi
  for MONTH in $(seq 1 $MONTHS);
  do
    mkdir -p SFO/$YEAR/$MONTH
    for DAY in {1..31};
    do
      FILE=SFO/$YEAR/$MONTH/$DAY.csv
      wget \
        -q -O $FILE \
        "http://www.wunderground.com/history/airport/KSFO/$YEAR/$MONTH/$DAY/DailyHistory.html?req_city=San%20Francisco&req_statename=California&format=1"
      if [ -f $FILE ];
      then
        sed -i.bak "s/<br \/>//" $FILE
        sed -i.bak "s/PST// ; s/PDT//" $FILE
      fi
    done
  done
  rm -f SFO/$YEAR/*/*.bak
  return 0
}


function SFO-cleanup () {
  echo "Get remaining weather data for SF airport from weather underground"

  for FILE in $(find SFO | xargs grep -d skip -l available);
  do
    DATE=$(echo $FILE | sed 's/.csv// ; s/SFO\///')
    wget \
      -q -O $FILE \
      "http://www.wunderground.com/history/airport/KSFO/$DATE/DailyHistory.html?req_city=San+Francisco&req_state=&req_statename=California&reqdb.zip=&reqdb.magic=&reqdb.wmo=&format=1"
      if [ -f $FILE ];
      then
        sed -i.bak "s/<br \/>//" $FILE
        sed -i.bak "s/PST// ; s/PDT//" $FILE
      fi
  done

  for FILE in $(find SFO | xargs grep -d skip -l available);
  do
    echo $FILE
    DATE=$(echo $FILE | sed 's/.csv// ; s/SFO\///')
    wget \
      -q -O $FILE \
      "http://www.wunderground.com/history/airport/KSFO/$DATE/DailyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=&format=1"
      if [ -f $FILE ];
      then
        sed -i.bak "s/<br \/>//" $FILE
        sed -i.bak "s/PST// ; s/PDT//" $FILE
      fi
  done
  rm -f SFO/*/*/*.bak
  return 0
}

function SFM-year () {
  if [ $# == 0 ];
  then
    echo "Get weather data for SF midtown from weather underground for a given year"
    return 0
  fi
  YEAR=$1
  MONTHS=12
  if [ $YEAR == 2015 ];
  then
    MONTHS=6
  fi
  for MONTH in $(seq 1 $MONTHS);
  do
    mkdir -p SFM/$YEAR/$MONTH
    for DAY in {1..31};
    do
      FILE=SFM/$YEAR/$MONTH/$DAY.csv
      wget \
        -q -O $FILE \
        "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=KCASANFR49&day=$DAY&month=$MONTH&year=$YEAR&graphspan=day&format=1"
      if [ -f $FILE ];
      then
        sed -i.bak 's/<br>// ; /^$/d ; s/,$//' $FILE
      fi
    done
  done
  rm -f SFM/$YEAR/*/*.bak
  return 0
}

function SFM-test () {
  if [ $# != 3 ];
  then
    echo "Get weather data for SF midtown from weather underground for a given year"
    return 0
  fi
  YEAR=$1
  MONTH=$2
  DAY=$3
  mkdir -p sfm_test/$YEAR/$MONTH
  FILE=sfm_test/$YEAR/$MONTH/$DAY.csv
  CMD='wget -q -O '$FILE' "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=KCASANFR49&day='$DAY'&month='$MONTH'&year='$YEAR'&graphspan=day&format=1"'
  echo $CMD
  if [ -f $FILE ];
  then
    sed -i.bak 's/<br>// ; /^$/d ; s/,$//' $FILE
  fi
  return 0
}

#midtown
#FSO


