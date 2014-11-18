#!/bin/sh
reason="Updating Repo"
path="."
while getopts ":p:m:f:" opt; do
  case $opt in
    p)
      path="$OPTARG"
      ;;
    m)
        reason="$OPTARG"
        ;;
    f)
        . "$OPTARG"         
        ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done
echo $path
cd $path
git add .
git commit -m "$reason"
git push
