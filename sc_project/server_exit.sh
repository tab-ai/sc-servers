#!/bin/bash

echo `ps -ef | grep "<defunct>" | grep -v "grep --color=auto" | awk '{print $3}' | xargs kill -9`
echo `ps -ef | grep runserver | grep -v "grep --color=auto" | awk '{print $2}' | xargs kill -9`

echo "서버 중지 완료"
