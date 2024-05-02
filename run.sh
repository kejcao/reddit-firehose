#!/bin/bash

while :; do
	python3 firehose.py unixporn
	python3 firehose.py earthporn
	sleep $((60*30))
done
