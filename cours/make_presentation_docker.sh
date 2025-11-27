#!/bin/bash

workdir=$(readlink -f "$(dirname "$0")")
basedir=$workdir
docker run -it --rm -v "$basedir:$basedir" -w "$workdir" -u $(id -u):$(id -g) pandoc_md2html_ce:latest ./make_presentation.sh 
