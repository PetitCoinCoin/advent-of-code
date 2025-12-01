#!/bin/sh

SESSION_COOKIE=`cat .aoc_tiles/session.cookie`
BASE_URL=https://adventofcode.com


help() {
    cat << EOF
    Usage: Get input from AOC for day of year (default to today)
    Used in a cron with '1 6 1-12 12 *' (I'll need at least a minute to read, understand and write)

    Options:
    -d            Day of puzzle (default to current day)
    -y            Year of event (default to current year)
EOF
}

while getopts "d:y:" arg; do
  case $arg in
    d) D=$OPTARG;;
    y) Y=$OPTARG;;
    *) help
       exit 1 ;;
  esac
done

DAY="${D:-`date +%-d`}"
YEAR="${Y:-`date +%Y`}"
URL="${BASE_URL}/${YEAR}/day/${DAY}/input"
DESTDIR="./${YEAR}/inputs/day_$(printf "%02d" $DAY).txt"

if [ ! -s "${DESTDIR}" ]; then touch "${DESTDIR}"; fi

RESP=`curl ${URL} -H "Cookie: session=${SESSION_COOKIE}"`
echo "${RESP}" > "${DESTDIR}"
