#!/bin/bash

if [[ $2 = "build_script" ]]; then
    CI_COMMIT_REF_NAME=$CUSTOM_ENV_CI_COMMIT_REF_NAME CI_PROJECT_PATH=$CUSTOM_ENV_CI_PROJECT_PATH python3 executor.py $1
fi
