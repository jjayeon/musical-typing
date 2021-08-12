#!/bin/bash

if [[ "$1" -eq "" ]]
then
    URL="https://tonetype.tech"
else
    URL=$1
fi

GET_ROUTES=("/" "/play/" "/user/" "/user/register/" "/user/login/")
POST_ROUTES=("/user/register/" "/user/login/" "/admin/" "/user/logout/")

CURL_CMD='curl -s -o /dev/null -w "%{http_code}"'

HEAD="-I"

POST='-X POST -d "username=admin&password=admin&name=songname&info={}"'

EXIT=0

check_route () {
    if [[ $RESPONSE -eq 200 || $RESPONSE -eq 418 || $RESPONSE -eq 302 ]]
    then
	echo "response $RESPONSE ok"
    else
	echo "response $RESPONSE not good"
	EXIT=1
    fi
}

echo "GET requests"
for ROUTE in ${GET_ROUTES[@]}; do
    REQUEST=$URL$ROUTE
    echo "curling $REQUEST"
    RESPONSE=$(eval $CURL_CMD $HEAD $REQUEST)
    check_route
done

echo "POST requests"
for ROUTE in ${POST_ROUTES[@]}; do
    REQUEST=$URL$ROUTE
    echo "curling $REQUEST"
    RESPONSE=$(eval $CURL_CMD $POST $REQUEST)
    check_route
done

if [[ $EXIT -eq 1 ]]
then
    docker-compose logs
fi

exit $EXIT
