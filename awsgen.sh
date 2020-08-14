#!/bin/bash 
# awsgen.sh - awsgen.py + curl 

for i in $(python3 awsgen.py $1)
do
  code=$(curl -i -s $i -I|grep -i 'http'|awk '{print $2}')
  # 200 status code: exist and have a public read access
  # 403 status code: exist but the access is diened
  if [[ $code == 200 || $code == 403 ]] 
  then
    echo "[$code] $i"
  fi
done
