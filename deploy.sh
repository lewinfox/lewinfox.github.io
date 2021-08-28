#!/bin/sh

# Fail on errors
set -e

printf "\033[0;32mDeploying updates to GitHub...\033[0m\n"

# Build the site
hugo -t hugo-theme-codex

cd public

git add .

MSG="Build site $(date)"

if [ -n "$*" ]; then
  MSG="$*"
fi

git commit -m "${MSG}"

git push origin master

