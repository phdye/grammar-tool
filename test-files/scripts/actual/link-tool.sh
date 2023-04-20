#!/bin/bash

find * -type d \
    | awk '{ printf "rm -rf %s/tool ; ln -s ../tool %s/.\n", $1, $1 }' \
    | sh
