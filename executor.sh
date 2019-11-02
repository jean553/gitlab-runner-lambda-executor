#!/bin/bash
export PATH=$PATH:/home/ubuntu/.local/bin/

if [[ $2 = "build_script" ]]; then
    python3 executor.py $1
fi
