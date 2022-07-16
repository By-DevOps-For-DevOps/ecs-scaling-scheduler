#!/usr/bin/env bash

set -x

aws lambda invoke \
	--cli-binary-format raw-in-base64-out \
	--function-name ScalingLambda \
	--invocation-type Event \
	--payload '{ "action":"'${1}'", "cluster":"'${2}'" }' \
	response.json
