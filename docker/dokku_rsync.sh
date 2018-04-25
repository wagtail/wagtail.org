#!/bin/sh
set -e
if [ -z "$HOST_STRING" ]; then
    exit 1
fi

host_string=$HOST_STRING
container=$1
shift;

ssh $host_string docker-direct exec -i $container "$@"
