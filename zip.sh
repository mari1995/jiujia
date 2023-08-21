#!/bin/bash

# fetch all branches from remote repository
git fetch

# pull changes from remote repository
git pull

# check if git pull was successful
if [ $? -eq 0 ]; then
  # generate timestamp string
  timestamp=$(date +"%Y-%m-%d_%H-%M-%S")

  # create zip archive of ai directory with timestamp in filename and excluding files/directories starting with "."
  zip -r "../jiujia_$timestamp.zip" . -x "./.git*"

  # execute further logic here
  # ...
else
  echo "git pull failed"
fi
