#!/bin/bash
#######################################################################
### Increment last digit of app version string by one and compile app
###
### usage: compile.sh <phantom compiler params>
### ie. compile.sh -i
#######################################################################
configfile=${PWD##*/}.json
version_line=$(grep '"app_version":' $configfile)
new_version=$(echo $version_line | egrep -o "([0-9]+\.?)+" | awk -F. -v OFS=. 'NF>1{$NF=sprintf("%0*d", length($NF), ($NF+1)); print}')
new_line='    "app_version": "'$new_version'",'
sed -i "s/$version_line/$new_line/" ./$configfile
echo -e "\nVersion incremented:"
grep '"app_version":' $configfile
echo -e "\nCompiling app\n\n"
phenv python /opt/phantom/bin/compile_app.pyc $1
