#!/bin/bash

if [[ "$1" -eq "" ]]
then
    URL="https://tonetype.tech"
else
    URL=$1
fi

ROUTES=("/" "/play/" "/user/" "/user/register/" "/user/login/")
EXIT=0

CURL_CMD='curl -s -o /dev/null -w "%{http_code}"'

HEAD="-I"

POST='-X POST -d "username=JonSmith&password=pw123"'

check_route () {
    if [[ $RESPONSE -eq 200 || $RESPONSE -eq 418 || $RESPONSE -eq 302 ]]
    then
	echo "response $RESPONSE ok"
    else
	echo "response $RESPONSE not good"
	EXIT=1
    fi
}

for ROUTE in ${ROUTES[@]}; do
    REQUEST=$URL$ROUTE
    echo "curling $REQUEST"
    RESPONSE=$(eval $CURL_CMD $HEAD $REQUEST)
    check_route
done

echo "curling register POST ${URL}/user/register/"
RESPONSE=$(eval $CURL_CMD $POST "${URL}/user/register/")
check_route

echo "curling login POST ${URL}/user/login/"
RESPONSE=$(eval $CURL_CMD $POST "${URL}/user/login/")
check_route

echo "curling logout POST ${URL}/logout/"
RESPONSE=$(eval $CURL_CMD $POST "$URL/logout/")
check_route

exit $EXIT
