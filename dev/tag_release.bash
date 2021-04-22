#!/bin/bash

# set -o xtrace

declare PATCH=${1:+.$1}

declare VER=$(date +%Y%m%d)${PATCH} TAG=$(date +%Y-%m-%d)${PATCH}

# update package metadata
sed -i -E "s/(version *= *\")(20[0-9]{6}[.0-9]+)/\1${VER}/" setup.py pyproject.toml

declare OLDTAG=$(git tag -l "20??-??-??*" | tail -1)
declare subject="Release ${TAG}" body="$(git log --format="* %s" ${OLDTAG}..)"

git commit -a -m "${subject}" -m "${body}"
git tag -a -m "${subject}" -m "${body}" ${TAG} HEAD
