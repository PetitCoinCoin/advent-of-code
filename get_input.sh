#!/bin/sh

SESSION_COOKIE=`cat .aoc_tiles/session.cookie`
BASE_URL=https://adventofcode.com


help() {
    cat << EOF
    Usage: Get input from AOC for day of year (default to today)
    Used in a cron with '0 6 1-12 12 *'

    Options:
    -d            Day of puzzle (default to current day)
    -y            Year of event (default to current year)
    -l            Language used for this day (default to py)
EOF
}

while getopts "d:y:l:" arg; do
  case $arg in
    d) D=$OPTARG;;
    y) Y=$OPTARG;;
    l) L=$OPTARG;;
    *) help
       exit 1 ;;
  esac
done

DAY="${D:-`date +%-d`}"
YEAR="${Y:-`date +%Y`}"
LANGUAGE="${L:-py}"

URL="${BASE_URL}/${YEAR}/day/${DAY}/input"
FILENAME="day_$(printf "%02d" $DAY)"
INPUT_DESTDIR="./${YEAR}/inputs/${FILENAME}.txt"
CODE_DESTDIR="./${YEAR}/${FILENAME}.${LANGUAGE}"

if [ ! -s "${INPUT_DESTDIR}" ]; then touch "${INPUT_DESTDIR}"; fi
if [ ! -s "${CODE_DESTDIR}" ]
  then
    if [ -e ./template.${LANGUAGE} ]
      then cp ./template.${LANGUAGE} ${CODE_DESTDIR}
      else echo "No .${LANGUAGE} template available. Creating empty file." && touch "${CODE_DESTDIR}"
    fi
fi

RESP=`curl ${URL} -H "Cookie: session=${SESSION_COOKIE}"`
echo "${RESP}" > "${INPUT_DESTDIR}"
